"""
Headless simulation and AI experiment utilities.

This module is used for measurable AI evaluation, not visual gameplay.
"""
from __future__ import annotations

import csv
import json
import os
import random
from typing import Dict, List, Optional, Tuple

from src.ai.ai_agent import create_ai
from src.engine.game_engine import GameEngine
from src.models import (
    Action,
    ActionType,
    Owner,
    TowerType,
    UnitType,
    TOWER_CONFIGS,
    UNIT_CONFIGS,
)
from src.systems.game_logger import GameLogger, MatchRecord


AI_CONFIGS: List[Tuple[str, str]] = [
    ("random", "balanced"),
    ("rule_based", "balanced"),
    ("heuristic", "defensive"),
    ("heuristic", "balanced"),
    ("heuristic", "aggressive"),
]


class AutoPlayer:
    """Scripted player opponent used to keep experiments reproducible."""

    def __init__(self, strategy: str = "balanced"):
        self.strategy = strategy
        self.cooldown = 0.0

    def update(self, dt: float):
        self.cooldown = max(0.0, self.cooldown - dt)

    def decide(self, engine: GameEngine) -> None:
        if self.cooldown > 0:
            return

        gs = engine.get_state()
        if gs is None:
            return

        if self.strategy == "early_attacker":
            self.cooldown = random.uniform(2.0, 3.5)
            self._send_affordable_unit(engine, preferred=[UnitType.SWARM, UnitType.FAST, UnitType.TANK])
        elif self.strategy == "defensive":
            self.cooldown = random.uniform(3.0, 5.0)
            if not self._build_or_upgrade_defense(engine):
                self._send_affordable_unit(engine, preferred=[UnitType.SWARM, UnitType.FAST])
        elif self.strategy == "random":
            self.cooldown = random.uniform(3.0, 6.0)
            if random.random() < 0.65:
                self._send_affordable_unit(engine, preferred=random.sample(list(UnitType), len(UnitType)))
            else:
                self._build_affordable_tower(engine)
        else:
            self.cooldown = random.uniform(2.8, 4.8)
            self._balanced_action(engine)

    def _balanced_action(self, engine: GameEngine) -> bool:
        gs = engine.get_state()
        if gs is None:
            return False

        if gs.ai_base.hp_ratio() < 0.3:
            if self._send_affordable_unit(engine, preferred=[UnitType.TANK, UnitType.FAST, UnitType.SWARM]):
                return True

        weakest_lane = min(
            range(len(gs.lanes)),
            key=lambda lane: len(gs.get_towers_by_lane(Owner.PLAYER, lane)),
        )
        if len(gs.get_towers_by_lane(Owner.PLAYER, weakest_lane)) == 0:
            if self._build_tower(engine, weakest_lane, TowerType.BALANCED):
                return True

        if random.random() < 0.7:
            return self._send_affordable_unit(engine, preferred=[UnitType.SWARM, UnitType.FAST, UnitType.TANK])
        return self._build_or_upgrade_defense(engine)

    def _build_or_upgrade_defense(self, engine: GameEngine) -> bool:
        gs = engine.get_state()
        if gs is None:
            return False

        # Upgrade the first affordable player tower before filling new slots.
        for tower in gs.player_towers:
            cost = tower.get_upgrade_cost()
            if tower.can_upgrade() and gs.player_resource >= cost:
                return engine.execute_action(
                    Action(
                        action_type=ActionType.UPGRADE_TOWER,
                        actor=Owner.PLAYER,
                        target_lane=tower.lane_id,
                        target_tower_id=tower.tower_id,
                        cost=cost,
                    ),
                    Owner.PLAYER,
                )

        lanes_by_pressure = sorted(
            range(len(gs.lanes)),
            key=lambda lane: sum(
                unit.hp * (0.5 + unit.position)
                for unit in gs.active_units
                if unit.owner == Owner.AI and unit.lane_id == lane
            ),
            reverse=True,
        )
        for lane in lanes_by_pressure:
            if self._build_tower(engine, lane, TowerType.BALANCED):
                return True
        return False

    def _build_affordable_tower(self, engine: GameEngine) -> bool:
        lanes = list(range(len(engine.get_state().lanes)))
        random.shuffle(lanes)
        tower_types = [TowerType.BALANCED, TowerType.FAST, TowerType.HEAVY]
        random.shuffle(tower_types)
        for lane in lanes:
            for tower_type in tower_types:
                if self._build_tower(engine, lane, tower_type):
                    return True
        return False

    def _build_tower(self, engine: GameEngine, lane: int, tower_type: TowerType) -> bool:
        gs = engine.get_state()
        if gs is None:
            return False
        free_slots = gs.get_free_build_slots(Owner.PLAYER, lane)
        cost = TOWER_CONFIGS[tower_type][1]["cost"]
        if not free_slots or gs.player_resource < cost:
            return False
        return engine.execute_action(
            Action(
                action_type=ActionType.BUILD_TOWER,
                actor=Owner.PLAYER,
                target_lane=lane,
                entity_type=tower_type,
                cost=cost,
                metadata={"slot": free_slots[0]},
            ),
            Owner.PLAYER,
        )

    def _send_affordable_unit(self, engine: GameEngine, preferred: List[UnitType]) -> bool:
        gs = engine.get_state()
        if gs is None:
            return False

        lanes = list(range(len(gs.lanes)))
        random.shuffle(lanes)
        for unit_type in preferred:
            cost = UNIT_CONFIGS[unit_type]["cost"]
            if gs.player_resource < cost:
                continue
            lane = self._choose_attack_lane(gs, lanes)
            return engine.execute_action(
                Action(
                    action_type=ActionType.SEND_UNIT,
                    actor=Owner.PLAYER,
                    target_lane=lane,
                    entity_type=unit_type,
                    cost=cost,
                ),
                Owner.PLAYER,
            )
        return False

    def _choose_attack_lane(self, gs, lanes: List[int]) -> int:
        if self.strategy in ("balanced", "early_attacker"):
            return min(lanes, key=lambda lane: len(gs.get_towers_by_lane(Owner.AI, lane)))
        return lanes[0]


def run_simulation(
    ai_type: str,
    profile: str = "balanced",
    num_matches: int = 10,
    seed: int = 42,
    verbose: bool = True,
    player_strategy: str = "balanced",
    log_dir: str = "logs",
) -> GameLogger:
    """
    Run N headless matches and return a logger containing all records.
    """
    ai_agent = create_ai(ai_type, profile)
    engine = GameEngine(ai_agent, headless=True)
    engine.logger = GameLogger(log_dir=log_dir, verbose=verbose)
    shared_logger = engine.logger
    player = AutoPlayer(strategy=player_strategy)

    if verbose:
        print(f"\n[Simulation] AI={ai_agent.name} | Player={player_strategy} | {num_matches} matches")
        print("-" * 70)

    sim_dt = 0.1
    max_ticks = 3500

    for match_idx in range(num_matches):
        random.seed(seed + match_idx)
        player.cooldown = 0.0
        match_id = f"sim_{ai_agent.name}_{player_strategy}_{match_idx:03d}"
        engine.start_match(match_id)

        tick = 0
        while engine.running and tick < max_ticks:
            player.update(sim_dt)
            player.decide(engine)
            engine.update(sim_dt)
            tick += 1

        if engine.running:
            engine.end_match()

        if verbose and (match_idx + 1) % 5 == 0:
            print(f"  Completed {match_idx + 1}/{num_matches}")

    if verbose:
        shared_logger.print_batch_stats()
        shared_logger.save_batch_summary(f"batch_{ai_agent.name}_{player_strategy}.json")

    return shared_logger


def run_comparison(num_matches: int = 10, seed: int = 42, player_strategy: str = "balanced"):
    """Compare all project AI profiles under the same player policy."""
    print("\n" + "=" * 78)
    print("  BATCH SIMULATION - AI COMPARISON")
    print("=" * 78)

    rows = []
    for ai_type, profile in AI_CONFIGS:
        logger = run_simulation(
            ai_type,
            profile,
            num_matches=num_matches,
            seed=seed,
            verbose=False,
            player_strategy=player_strategy,
        )
        rows.append(_summarize_records(f"{ai_type}_{profile}", logger.all_records))

    _print_summary_table(rows)


def run_experiment_suite(
    num_matches: int = 30,
    seed: int = 42,
    player_strategy: str = "balanced",
    output_dir: str = "logs/experiments",
) -> Dict:
    """Run the formal comparison suite and export JSON, CSV and Markdown."""
    os.makedirs(output_dir, exist_ok=True)
    match_log_dir = os.path.join(output_dir, "matches")
    os.makedirs(match_log_dir, exist_ok=True)

    rows = []
    for ai_type, profile in AI_CONFIGS:
        label = f"{ai_type}_{profile}"
        logger = run_simulation(
            ai_type,
            profile,
            num_matches=num_matches,
            seed=seed,
            verbose=False,
            player_strategy=player_strategy,
            log_dir=match_log_dir,
        )
        rows.append(_summarize_records(label, logger.all_records))

    result = {
        "metadata": {
            "num_matches_per_ai": num_matches,
            "seed": seed,
            "player_strategy": player_strategy,
            "map_type": "fixed_lane",
            "ai_configs": [f"{ai_type}_{profile}" for ai_type, profile in AI_CONFIGS],
        },
        "summary": rows,
    }

    base_name = f"ai_comparison_{player_strategy}_{num_matches}"
    _write_json(os.path.join(output_dir, f"{base_name}.json"), result)
    _write_csv(os.path.join(output_dir, f"{base_name}.csv"), rows)
    _write_markdown(os.path.join(output_dir, f"{base_name}.md"), result)

    _print_summary_table(rows)
    print(f"\nSaved experiment outputs to: {output_dir}")
    return result


def _summarize_records(label: str, records: List[MatchRecord]) -> Dict:
    n = len(records)
    if n == 0:
        return {"ai_profile": label, "matches": 0}

    wins = sum(1 for r in records if r.winner == "AI")
    draws = sum(1 for r in records if r.winner == "DRAW")
    lane_counts = _sum_mapping(r.ai_attack_lane_counts for r in records)
    unit_counts = _sum_mapping(r.ai_unit_type_counts for r in records)
    lane_damage = _sum_mapping(r.ai_base_damage_by_lane for r in records)
    return {
        "ai_profile": label,
        "matches": n,
        "ai_win_rate_pct": round(wins / n * 100, 2),
        "draw_rate_pct": round(draws / n * 100, 2),
        "avg_match_duration_s": round(sum(r.match_duration for r in records) / n, 2),
        "avg_ai_base_hp_end": round(sum(r.ai_base_hp_end for r in records) / n, 2),
        "avg_player_base_hp_end": round(sum(r.player_base_hp_end for r in records) / n, 2),
        "avg_damage_to_player_base": round(sum(r.damage_to_player_base for r in records) / n, 2),
        "avg_damage_to_ai_base": round(sum(r.damage_to_ai_base for r in records) / n, 2),
        "avg_damage_to_player_units": round(sum(r.damage_to_player_units for r in records) / n, 2),
        "avg_ai_kills": round(sum(r.ai_kills for r in records) / n, 2),
        "avg_resource_spent_ai": round(sum(r.resource_spent_ai for r in records) / n, 2),
        "avg_resource_efficiency_ai": round(sum(r.resource_efficiency_ai() for r in records) / n, 4),
        "avg_ai_attack_count": round(sum(r.ai_attack_count for r in records) / n, 2),
        "avg_ai_defense_count": round(sum(r.ai_defense_count for r in records) / n, 2),
        "avg_ai_economy_count": round(sum(r.ai_economy_count for r in records) / n, 2),
        "dominant_ai_attack_lane": _dominant_key(lane_counts),
        "most_effective_ai_damage_lane": _dominant_key(lane_damage),
        "ai_attack_lane_counts": lane_counts,
        "ai_unit_type_counts": unit_counts,
        "ai_base_damage_by_lane": {str(k): round(v, 2) for k, v in lane_damage.items()},
        "avg_decision_time_ms": round(sum(r.decision_time_avg() for r in records) / n, 4),
        "max_decision_time_ms": round(max(r.decision_time_max() for r in records), 4),
    }


def _sum_mapping(maps) -> Dict:
    total: Dict = {}
    for data in maps:
        for key, value in data.items():
            total[key] = total.get(key, 0) + value
    return total


def _dominant_key(data: Dict):
    if not data:
        return None
    key = max(data, key=data.get)
    try:
        return int(key)
    except (TypeError, ValueError):
        return key


def _print_summary_table(rows: List[Dict]):
    print(
        f"\n{'AI Profile':28s} | {'N':>3s} | {'Win%':>7s} | {'AI HP':>7s} | "
        f"{'DmgBase':>8s} | {'Eff':>7s} | {'Atk':>6s} | {'Def':>6s} | {'Lane':>5s} | {'ms':>7s}"
    )
    print("-" * 102)
    for row in rows:
        print(
            f"{row['ai_profile']:28s} | {row['matches']:3d} | "
            f"{row['ai_win_rate_pct']:7.1f} | {row['avg_ai_base_hp_end']:7.1f} | "
            f"{row['avg_damage_to_player_base']:8.1f} | {row['avg_resource_efficiency_ai']:7.3f} | "
            f"{row['avg_ai_attack_count']:6.1f} | {row['avg_ai_defense_count']:6.1f} | "
            f"{str(row['dominant_ai_attack_lane']):>5s} | "
            f"{row['avg_decision_time_ms']:7.4f}"
        )
    print("-" * 102)


def _write_json(path: str, data: Dict):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _write_csv(path: str, rows: List[Dict]):
    if not rows:
        return
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _write_markdown(path: str, result: Dict):
    rows = result["summary"]
    metadata = result["metadata"]
    lines = [
        "# AI Experiment Summary",
        "",
        f"- Matches per AI: {metadata['num_matches_per_ai']}",
        f"- Seed: {metadata['seed']}",
        f"- Player strategy: `{metadata['player_strategy']}`",
        f"- Map: `{metadata['map_type']}`",
        "",
        "| AI Profile | Win % | AI HP Avg | Damage to Player Base | Resource Eff | Attack Avg | Defense Avg | Main Lane | Decision ms Avg |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            f"| {row['ai_profile']} | {row['ai_win_rate_pct']:.1f} | "
            f"{row['avg_ai_base_hp_end']:.1f} | {row['avg_damage_to_player_base']:.1f} | "
            f"{row['avg_resource_efficiency_ai']:.3f} | {row['avg_ai_attack_count']:.1f} | "
            f"{row['avg_ai_defense_count']:.1f} | {row['dominant_ai_attack_lane']} | "
            f"{row['avg_decision_time_ms']:.4f} |"
        )
    lines.extend(
        [
            "",
            "## Notes",
            "",
            "- `Damage to Player Base` only counts base damage after metric cleanup.",
            "- `Resource Eff` = AI base damage dealt / AI resource spent.",
            "- The scripted player is a controlled test opponent, not a human-level player.",
        ]
    )
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
