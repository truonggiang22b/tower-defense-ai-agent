"""
GameLogger - Ghi log, thống kê trận đấu
Bắt buộc theo tài liệu, ghi từ sớm
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import json
import time
import os

from src.models import GameState, Action, Owner


@dataclass
class MatchRecord:
    """Thống kê một trận đấu"""
    match_id: str
    ai_profile: str
    map_type: str = "fixed_lane"
    start_time: float = 0.0
    end_time: float = 0.0

    # Kết quả
    winner: str = ""
    match_duration: float = 0.0

    # HP cuối
    player_base_hp_end: float = 0.0
    ai_base_hp_end: float = 0.0

    # Damage
    damage_to_player_base: float = 0.0
    damage_to_ai_base: float = 0.0
    damage_to_player_units: float = 0.0
    damage_to_ai_units: float = 0.0
    total_damage_by_player: float = 0.0
    total_damage_by_ai: float = 0.0

    # Kills
    player_kills: int = 0
    ai_kills: int = 0

    # Resource
    resource_spent_player: float = 0.0
    resource_spent_ai: float = 0.0

    # Action counts
    player_attack_count: int = 0
    player_defense_count: int = 0
    ai_attack_count: int = 0
    ai_defense_count: int = 0
    ai_economy_count: int = 0
    ai_attack_lane_counts: Dict[int, int] = field(default_factory=dict)
    ai_unit_type_counts: Dict[str, int] = field(default_factory=dict)
    ai_base_damage_by_lane: Dict[int, float] = field(default_factory=dict)
    dominant_ai_attack_lane: Optional[int] = None
    most_effective_ai_damage_lane: Optional[int] = None

    # Decision timing
    decision_times_ms: List[float] = field(default_factory=list)

    # Action log
    action_log: List[Dict] = field(default_factory=list)

    def decision_time_avg(self) -> float:
        if not self.decision_times_ms:
            return 0.0
        return sum(self.decision_times_ms) / len(self.decision_times_ms)

    def decision_time_max(self) -> float:
        return max(self.decision_times_ms) if self.decision_times_ms else 0.0

    def resource_efficiency_ai(self) -> float:
        """damage_to_player_base / resource_spent_ai"""
        if self.resource_spent_ai <= 0:
            return 0.0
        return self.damage_to_player_base / self.resource_spent_ai

    def to_dict(self) -> Dict:
        return {
            "match_id": self.match_id,
            "ai_profile": self.ai_profile,
            "map_type": self.map_type,
            "winner": self.winner,
            "match_duration_s": round(self.match_duration, 2),
            "player_base_hp_end": round(self.player_base_hp_end, 1),
            "ai_base_hp_end": round(self.ai_base_hp_end, 1),
            "damage_to_player_base": round(self.damage_to_player_base, 1),
            "damage_to_ai_base": round(self.damage_to_ai_base, 1),
            "damage_to_player_units": round(self.damage_to_player_units, 1),
            "damage_to_ai_units": round(self.damage_to_ai_units, 1),
            "total_damage_by_player": round(self.total_damage_by_player, 1),
            "total_damage_by_ai": round(self.total_damage_by_ai, 1),
            "player_kills": self.player_kills,
            "ai_kills": self.ai_kills,
            "resource_spent_player": round(self.resource_spent_player, 1),
            "resource_spent_ai": round(self.resource_spent_ai, 1),
            "player_attack_count": self.player_attack_count,
            "player_defense_count": self.player_defense_count,
            "ai_attack_count": self.ai_attack_count,
            "ai_defense_count": self.ai_defense_count,
            "ai_economy_count": self.ai_economy_count,
            "ai_attack_lane_counts": self.ai_attack_lane_counts,
            "ai_unit_type_counts": self.ai_unit_type_counts,
            "ai_base_damage_by_lane": {str(k): round(v, 1) for k, v in self.ai_base_damage_by_lane.items()},
            "dominant_ai_attack_lane": self.dominant_ai_attack_lane,
            "most_effective_ai_damage_lane": self.most_effective_ai_damage_lane,
            "ai_decision_time_avg_ms": round(self.decision_time_avg(), 3),
            "ai_decision_time_max_ms": round(self.decision_time_max(), 3),
            "resource_efficiency_ai": round(self.resource_efficiency_ai(), 4),
        }

    def summary_str(self) -> str:
        lines = [
            "=" * 55,
            "  MATCH RESULT",
            "=" * 55,
            f"  Match:         {self.match_id}",
            f"  AI Profile:    {self.ai_profile}",
            f"  Winner:        {self.winner}",
            f"  Duration:      {self.match_duration:.1f}s",
            "-" * 55,
            f"  Base HP:",
            f"    Player:      {self.player_base_hp_end:.0f}",
            f"    AI:          {self.ai_base_hp_end:.0f}",
            "-" * 55,
            f"  Damage dealt:",
            f"    To Player base:   {self.damage_to_player_base:.0f}",
            f"    To AI base:       {self.damage_to_ai_base:.0f}",
            f"    To Player units:  {self.damage_to_player_units:.0f}",
            f"    To AI units:      {self.damage_to_ai_units:.0f}",
            "-" * 55,
            f"  Units killed:",
            f"    Player kills:     {self.player_kills}",
            f"    AI kills:         {self.ai_kills}",
            "-" * 55,
            f"  Resources spent:",
            f"    Player:           {self.resource_spent_player:.0f}",
            f"    AI:               {self.resource_spent_ai:.0f}",
            "-" * 55,
            f"  AI Actions:",
            f"    Attack:           {self.ai_attack_count}",
            f"    Defense:          {self.ai_defense_count}",
            f"    Economy:          {self.ai_economy_count}",
            f"  AI Decision time:",
            f"    Avg: {self.decision_time_avg():.2f} ms",
            f"    Max: {self.decision_time_max():.2f} ms",
            f"  Res efficiency:    {self.resource_efficiency_ai():.4f}",
            "=" * 55,
        ]
        return "\n".join(lines)


class GameLogger:
    """Logger cho từng trận và batch"""

    def __init__(self, log_dir: str = "logs", verbose: bool = True):
        self.log_dir = log_dir
        self.verbose = verbose
        os.makedirs(log_dir, exist_ok=True)
        self.current_record: Optional[MatchRecord] = None
        self.all_records: List[MatchRecord] = []

    def start_match(self, match_id: str, ai_profile: str):
        self.current_record = MatchRecord(
            match_id=match_id,
            ai_profile=ai_profile,
            start_time=time.time()
        )
        if self.verbose:
            print(f"[Logger] Match {match_id} | AI: {ai_profile}")

    def log_ai_action(self, action: Action, score: float, decision_time_ms: float):
        """Ghi log hành động AI"""
        if not self.current_record:
            return
        self.current_record.decision_times_ms.append(decision_time_ms)
        entry = {
            "action_type": action.action_type.value,
            "actor": action.actor.value,
            "lane": action.target_lane,
            "entity": action.entity_type.value if action.entity_type else None,
            "cost": action.cost,
            "quantity": action.metadata.get("quantity", 1),
            "score": round(score, 4),
            "decision_time_ms": round(decision_time_ms, 3),
        }
        self.current_record.action_log.append(entry)

    def log_player_action(self, action: Action):
        """Ghi log hành động người chơi"""
        if not self.current_record:
            return

    def end_match(self, game_state: GameState):
        """Kết thúc và ghi thống kê"""
        if not self.current_record:
            return
        r = self.current_record
        r.end_time = time.time()
        r.match_duration = game_state.match_time
        r.winner = game_state.get_winner() or "?"
        r.player_base_hp_end = game_state.player_base.hp
        r.ai_base_hp_end = game_state.ai_base.hp
        r.damage_to_player_base = game_state.ai_base_damage_dealt
        r.damage_to_ai_base = game_state.player_base_damage_dealt
        r.damage_to_player_units = game_state.ai_unit_damage_dealt
        r.damage_to_ai_units = game_state.player_unit_damage_dealt
        r.total_damage_by_player = game_state.player_damage_dealt
        r.total_damage_by_ai = game_state.ai_damage_dealt
        r.player_kills = game_state.player_kills
        r.ai_kills = game_state.ai_kills
        r.resource_spent_player = game_state.player_resource_spent
        r.resource_spent_ai = game_state.ai_resource_spent
        r.player_attack_count = game_state.player_attack_count
        r.player_defense_count = game_state.player_defense_count
        r.ai_attack_count = game_state.ai_attack_count
        r.ai_defense_count = game_state.ai_defense_count
        r.ai_economy_count = game_state.ai_economy_count
        r.ai_attack_lane_counts = dict(game_state.ai_attack_lane_counts)
        r.ai_unit_type_counts = dict(game_state.ai_unit_type_counts)
        r.ai_base_damage_by_lane = dict(game_state.ai_base_damage_by_lane)
        r.dominant_ai_attack_lane = self._dominant_key(r.ai_attack_lane_counts)
        r.most_effective_ai_damage_lane = self._dominant_key(r.ai_base_damage_by_lane)

        self.all_records.append(r)

        # Print summary
        if self.verbose:
            print(r.summary_str())

        # Ghi file JSON
        self._save_record(r)
        self.current_record = None

    def _save_record(self, record: MatchRecord):
        path = os.path.join(self.log_dir, f"{record.match_id}.json")
        with open(path, "w", encoding="utf-8") as f:
            data = record.to_dict()
            data["action_log"] = record.action_log
            json.dump(data, f, ensure_ascii=False, indent=2)

    def save_batch_summary(self, filename: str = "batch_summary.json"):
        """Save batch summary to JSON"""
        path = os.path.join(self.log_dir, filename)
        data = [r.to_dict() for r in self.all_records]
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=True, indent=2)
        if self.verbose:
            print(f"[Logger] Saved batch summary: {path}")

    def _dominant_key(self, data: Dict) -> Optional[int]:
        if not data:
            return None
        key = max(data, key=data.get)
        try:
            return int(key)
        except (TypeError, ValueError):
            return key

    def print_batch_stats(self):
        """Print batch summary stats"""
        if not self.all_records or not self.verbose:
            return
        profiles = {}
        for r in self.all_records:
            if r.ai_profile not in profiles:
                profiles[r.ai_profile] = []
            profiles[r.ai_profile].append(r)

        print("\n" + "=" * 60)
        print("  BATCH STATS")
        print("=" * 60)
        for profile, records in profiles.items():
            wins = sum(1 for r in records if r.winner == "AI")
            n = len(records)
            avg_dur = sum(r.match_duration for r in records) / n
            avg_hp = sum(r.ai_base_hp_end for r in records) / n
            avg_eff = sum(r.resource_efficiency_ai() for r in records) / n
            print(f"  {profile:20s} | {n:3d} matches | Win: {wins/n*100:.0f}% "
                  f"| AI HP avg: {avg_hp:.0f} | Eff: {avg_eff:.4f} | Dur: {avg_dur:.0f}s")
        print("=" * 60)
