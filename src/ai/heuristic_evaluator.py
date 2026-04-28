"""
HeuristicEvaluator - scores candidate AI actions with a weighted utility function.

The implementation intentionally stays explainable for the Intro to AI report:
lane summary -> candidate action -> utility score -> greedy best action.
"""
from __future__ import annotations

from typing import Dict, List

from src.models import (
    Action,
    ActionType,
    GameState,
    LaneSummary,
    Owner,
    TowerType,
    UnitType,
)


PROFILES: Dict[str, Dict[str, float]] = {
    "defensive": {
        "w1": 2.0,  # projected damage to player base
        "w2": 5.0,  # AI base safety
        "w3": 4.0,  # enemy unit pressure / kills
        "w4": 2.0,  # pressure on player
        "w5": 2.0,  # resource penalty
        "w6": 5.0,  # danger to AI base penalty
        "w7": 1.0,  # idle penalty
    },
    "aggressive": {
        "w1": 5.4,
        "w2": 1.8,
        "w3": 2.0,
        "w4": 5.6,
        "w5": 0.8,
        "w6": 2.6,
        "w7": 3.2,
    },
    "balanced": {
        "w1": 4.4,
        "w2": 3.6,
        "w3": 3.0,
        "w4": 3.5,
        "w5": 1.6,
        "w6": 3.8,
        "w7": 2.0,
    },
}


class HeuristicEvaluator:
    """Compute lane summaries and score actions for HeuristicAI."""

    def __init__(self, profile: str = "balanced"):
        self.profile = profile
        self.weights = PROFILES.get(profile, PROFILES["balanced"])
        self.thresholds = {
            "danger_high": 0.7,
            "danger_medium": 0.4,
            "opportunity_high": 0.6,
            "resource_rich": 200,
            "resource_low": 80,
            "base_hp_critical": 0.3,
            "base_hp_safe": 0.7,
        }

    def compute_lane_summaries(self, game_state: GameState) -> List[LaneSummary]:
        summaries: List[LaneSummary] = []
        for lane in game_state.lanes:
            lane_id = lane.lane_id

            enemy_units = [
                unit for unit in game_state.active_units
                if unit.owner == Owner.PLAYER and unit.lane_id == lane_id
            ]
            friendly_units = [
                unit for unit in game_state.active_units
                if unit.owner == Owner.AI and unit.lane_id == lane_id
            ]

            enemy_pressure = self._calc_unit_pressure(enemy_units)
            friendly_pressure = self._calc_unit_pressure(friendly_units)
            enemy_tower_strength = self._calc_tower_strength(
                game_state.get_towers_by_lane(Owner.PLAYER, lane_id)
            )
            friendly_tower_strength = self._calc_tower_strength(
                game_state.get_towers_by_lane(Owner.AI, lane_id)
            )

            breakthrough_risk = min(
                1.0,
                enemy_pressure * 0.7 + max(0.0, 0.5 - friendly_tower_strength) * 0.3,
            )
            attack_opportunity = min(
                1.0,
                (1.0 - enemy_tower_strength) * 0.6 + friendly_pressure * 0.4,
            )

            summary = LaneSummary(
                lane_id=lane_id,
                enemy_unit_pressure=enemy_pressure,
                friendly_unit_pressure=friendly_pressure,
                enemy_tower_strength=enemy_tower_strength,
                friendly_tower_strength=friendly_tower_strength,
                breakthrough_risk=breakthrough_risk,
                attack_opportunity=attack_opportunity,
                num_build_slots_free=len(game_state.get_free_build_slots(Owner.AI, lane_id)),
            )
            summaries.append(summary)
            lane.danger_score = breakthrough_risk

        return summaries

    def _calc_unit_pressure(self, units) -> float:
        if not units:
            return 0.0
        pressure = sum(unit.hp * (0.5 + unit.position * 0.5) for unit in units) / 500.0
        return min(1.0, pressure)

    def _calc_tower_strength(self, towers) -> float:
        if not towers:
            return 0.0
        strength = sum(tower.damage * tower.level / tower.attack_interval for tower in towers) / 300.0
        return min(1.0, strength)

    def score(
        self,
        action: Action,
        game_state: GameState,
        lane_summaries: List[LaneSummary],
    ) -> float:
        weights = self.weights
        ai_hp_ratio = game_state.ai_base.hp_ratio()
        player_hp_ratio = game_state.player_base.hp_ratio()

        if action.action_type == ActionType.NO_ACTION:
            return 0.0

        if action.action_type == ActionType.SAVE_RESOURCE:
            idle_penalty = 0.0
            if game_state.ai_resource > self.thresholds["resource_rich"]:
                idle_penalty = weights["w7"] * 0.3
            if player_hp_ratio < 0.5:
                idle_penalty += weights["w7"] * 0.2
            return max(0.0, 0.5 - idle_penalty)

        summary = None
        if action.target_lane is not None and 0 <= action.target_lane < len(lane_summaries):
            summary = lane_summaries[action.target_lane]

        score = 0.0
        if action.action_type == ActionType.BUILD_TOWER:
            score = self._score_build_tower(action, summary, ai_hp_ratio)
        elif action.action_type == ActionType.UPGRADE_TOWER:
            score = self._score_upgrade_tower(summary, ai_hp_ratio)
        elif action.action_type == ActionType.SEND_UNIT:
            score = self._score_send_unit(action, game_state, summary, player_hp_ratio)

        score -= self._resource_penalty(action)
        return max(0.0, score)

    def _resource_penalty(self, action: Action) -> float:
        if action.action_type == ActionType.SEND_UNIT:
            return self.weights["w5"] * (action.cost / 220.0)
        return self.weights["w5"] * (action.cost / 150.0)

    def _score_build_tower(self, action: Action, summary: LaneSummary, ai_hp_ratio: float) -> float:
        weights = self.weights
        if summary is None:
            return 0.1

        score = 0.0
        score += weights["w2"] * summary.breakthrough_risk * 0.8
        score += weights["w3"] * summary.enemy_unit_pressure * 0.5

        if summary.friendly_tower_strength <= 0.05:
            score += weights["w2"] * 0.8

        if summary.breakthrough_risk > self.thresholds["danger_medium"]:
            score += weights["w2"] * 1.1
        if ai_hp_ratio < self.thresholds["base_hp_safe"]:
            score += weights["w2"] * (1.0 - ai_hp_ratio) * 0.9
        if self.profile == "balanced" and ai_hp_ratio < 0.8:
            score += weights["w2"] * (0.8 - ai_hp_ratio) * 2.2
        elif self.profile == "aggressive" and ai_hp_ratio < 0.45:
            score += weights["w2"] * (0.45 - ai_hp_ratio) * 2.0

        score -= weights["w6"] * summary.friendly_tower_strength * 0.4

        if ai_hp_ratio > self.thresholds["base_hp_safe"] and summary.breakthrough_risk < 0.3:
            score -= 0.5

        if action.entity_type == TowerType.HEAVY and summary.enemy_unit_pressure > 0.5:
            score += 0.5
        elif action.entity_type == TowerType.FAST and summary.enemy_unit_pressure > 0.3:
            score += 0.3
        elif action.entity_type == TowerType.BALANCED and summary.breakthrough_risk > 0.25:
            score += 0.4

        return score

    def _score_upgrade_tower(self, summary: LaneSummary, ai_hp_ratio: float) -> float:
        weights = self.weights
        if summary is None:
            return 0.2

        score = 0.0
        score += weights["w2"] * summary.breakthrough_risk * 0.6
        score += weights["w3"] * summary.friendly_tower_strength * 0.5
        if summary.friendly_tower_strength > 0.3:
            score += 0.4
        if summary.breakthrough_risk > self.thresholds["danger_medium"]:
            score += weights["w2"] * 0.8
        if ai_hp_ratio < self.thresholds["base_hp_safe"]:
            score += weights["w2"] * (1.0 - ai_hp_ratio) * 0.7
        if self.profile == "balanced" and ai_hp_ratio < 0.8:
            score += weights["w2"] * (0.8 - ai_hp_ratio) * 1.8
        elif self.profile == "aggressive" and ai_hp_ratio < 0.45:
            score += weights["w2"] * (0.45 - ai_hp_ratio) * 1.5
        return score

    def _score_send_unit(
        self,
        action: Action,
        game_state: GameState,
        summary: LaneSummary,
        player_hp_ratio: float,
    ) -> float:
        weights = self.weights
        if summary is None:
            return 0.2

        score = 0.0
        score += weights["w1"] * (1.0 - summary.enemy_tower_strength) * 0.9
        score += weights["w4"] * summary.attack_opportunity * 0.8
        score += weights["w4"] * summary.friendly_unit_pressure * 0.7
        score += self._weakest_player_lane_bonus(action, game_state)

        score += weights["w1"] * (1.0 - player_hp_ratio) * 0.8
        if game_state.ai_resource > self.thresholds["resource_rich"]:
            score += weights["w4"] * 0.25

        ai_hp_ratio = game_state.ai_base.hp_ratio()
        if ai_hp_ratio < self.thresholds["base_hp_critical"]:
            score -= weights["w6"] * 0.8
        if self.profile == "defensive":
            score *= 0.65
            if ai_hp_ratio > 0.85 and game_state.ai_resource > self.thresholds["resource_rich"]:
                score += 0.6
        elif self.profile == "balanced":
            if ai_hp_ratio < 0.55:
                score *= 0.45
            elif ai_hp_ratio < 0.8 and summary.breakthrough_risk > 0.15:
                score *= 0.52
            elif ai_hp_ratio < 0.72 and summary.breakthrough_risk > 0.25:
                score *= 0.6
            elif summary.breakthrough_risk > self.thresholds["danger_medium"]:
                score *= 0.7
        elif self.profile == "aggressive":
            if ai_hp_ratio < 0.45 and summary.breakthrough_risk > 0.25:
                score *= 0.55
            score += weights["w4"] * 0.25

        if (
            action.entity_type == UnitType.FAST
            and summary.enemy_tower_strength > 0
            and self._has_slow_towers(game_state, Owner.PLAYER, action.target_lane)
        ):
            score += 1.0
        if action.entity_type == UnitType.FAST:
            # Fast units are the best practical base-damage tool in the current lane MVP.
            if summary.enemy_tower_strength < 0.45:
                score += 1.4
            if summary.attack_opportunity > 0.45:
                score += 0.8

        if action.entity_type == UnitType.TANK:
            if summary.enemy_tower_strength >= 0.25:
                score += 2.4
            elif game_state.ai_resource > self.thresholds["resource_rich"]:
                score += 0.9

        if action.entity_type == UnitType.SWARM:
            if summary.enemy_tower_strength < 0.35:
                score += 0.3
            else:
                score -= 2.2
            if summary.friendly_unit_pressure > 0.2:
                score += 0.4

        if action.entity_type == UnitType.FAST and summary.enemy_tower_strength < 0.2:
            score += 0.9

        quantity = int(action.metadata.get("quantity", 1))
        if quantity > 1:
            if self.profile == "defensive":
                score *= 1.0 + 0.08 * (quantity - 1)
            elif self.profile == "balanced":
                score *= 1.0 + 0.26 * (quantity - 1)
            else:
                score *= 1.0 + 0.34 * (quantity - 1)
            if summary.attack_opportunity > 0.45 or game_state.ai_resource > self.thresholds["resource_rich"]:
                score += 0.35 * quantity
            if self.profile == "aggressive" and quantity >= 3:
                score += 0.25 * quantity
            if action.entity_type == UnitType.FAST:
                score += 0.45 * quantity
            elif action.entity_type == UnitType.SWARM:
                score -= 0.2 * quantity

        return score

    def _weakest_player_lane_bonus(self, action: Action, game_state: GameState) -> float:
        if action.target_lane is None:
            return 0.0

        lane_scores = []
        for lane_id in range(len(game_state.lanes)):
            towers = game_state.get_towers_by_lane(Owner.PLAYER, lane_id)
            tower_strength = self._calc_tower_strength(towers)
            active_ai_units = sum(
                1
                for unit in game_state.active_units
                if unit.owner == Owner.AI and unit.lane_id == lane_id
            )
            lane_scores.append((tower_strength, -active_ai_units, lane_id))

        lane_scores.sort()
        weakest_lane = lane_scores[0][2] if lane_scores else None
        return 0.7 if action.target_lane == weakest_lane else 0.0

    def _has_slow_towers(self, game_state: GameState, owner: Owner, lane_id) -> bool:
        if lane_id is None:
            return False
        towers = game_state.get_towers_by_lane(owner, lane_id)
        return any(tower.tower_type == TowerType.HEAVY for tower in towers)

    def estimate_danger(self, lane_summary: LaneSummary) -> str:
        if lane_summary.breakthrough_risk > self.thresholds["danger_high"]:
            return "HIGH"
        if lane_summary.breakthrough_risk > self.thresholds["danger_medium"]:
            return "MEDIUM"
        return "LOW"
