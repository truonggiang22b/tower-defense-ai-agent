"""
AIAgent - Ba loại AI:
  1. RandomAI     - chọn hành động ngẫu nhiên
  2. RuleBasedAI  - dùng luật đơn giản
  3. HeuristicAI  - dùng HeuristicEvaluator + greedy

Theo tài liệu 02 và 03.
"""
from __future__ import annotations
import random
import time
from typing import List, Optional, Tuple

from src.models import (
    GameState, Action, ActionType, Owner, TowerType, UnitType,
    LaneSummary, TOWER_CONFIGS, UNIT_CONFIGS
)
from src.ai.heuristic_evaluator import HeuristicEvaluator
from src.systems.map_manager import NUM_SLOTS_PER_SIDE


# Cooldown giữa các lần AI quyết định (giây)
AI_DECISION_INTERVAL = 2.5


def _get_first_free_slot(game_state: GameState, lane_id: int) -> Optional[int]:
    """Lấy slot đầu tiên còn trống phía AI"""
    slots = game_state.get_free_build_slots(Owner.AI, lane_id)
    return slots[0] if slots else None


def _can_build_tower(game_state: GameState, tower_type: TowerType, lane_id: int) -> bool:
    cost = TOWER_CONFIGS[tower_type][1]["cost"]
    if game_state.ai_resource < cost:
        return False
    slots = game_state.get_free_build_slots(Owner.AI, lane_id)
    return len(slots) > 0


def _can_send_unit(game_state: GameState, unit_type: UnitType) -> bool:
    cost = UNIT_CONFIGS[unit_type]["cost"]
    return game_state.ai_resource >= cost


def _generate_candidate_actions(game_state: GameState) -> List[Action]:
    """
    Sinh danh sách hành động ứng viên theo tài liệu 02 - section 7.
    Chỉ xét 1-2 lane nguy hiểm nhất và lane yếu nhất của đối phương.
    """
    candidates: List[Action] = []
    resource = game_state.ai_resource

    # SAVE_RESOURCE luôn là ứng viên
    candidates.append(Action(
        action_type=ActionType.SAVE_RESOURCE,
        actor=Owner.AI,
        cost=0,
    ))

    num_lanes = len(game_state.lanes)

    for lane_id in range(num_lanes):
        # BUILD TOWER candidates
        if resource >= TOWER_CONFIGS[TowerType.FAST][1]["cost"]:
            if len(game_state.get_free_build_slots(Owner.AI, lane_id)) > 0:
                for tt in [TowerType.FAST, TowerType.HEAVY, TowerType.BALANCED]:
                    if resource >= TOWER_CONFIGS[tt][1]["cost"]:
                        slot = _get_first_free_slot(game_state, lane_id)
                        if slot is not None:
                            cost = TOWER_CONFIGS[tt][1]["cost"]
                            candidates.append(Action(
                                action_type=ActionType.BUILD_TOWER,
                                actor=Owner.AI,
                                target_lane=lane_id,
                                entity_type=tt,
                                cost=cost,
                                metadata={"slot": slot},
                            ))

        # UPGRADE TOWER candidates
        ai_towers_in_lane = game_state.get_towers_by_lane(Owner.AI, lane_id)
        for t in ai_towers_in_lane:
            if t.can_upgrade():
                upgrade_cost = t.get_upgrade_cost()
                if resource >= upgrade_cost:
                    candidates.append(Action(
                        action_type=ActionType.UPGRADE_TOWER,
                        actor=Owner.AI,
                        target_lane=lane_id,
                        target_tower_id=t.tower_id,
                        cost=upgrade_cost,
                    ))

        # SEND UNIT candidates
        for ut in [UnitType.FAST, UnitType.TANK, UnitType.SWARM]:
            if _can_send_unit(game_state, ut):
                cost = UNIT_CONFIGS[ut]["cost"]
                candidates.append(Action(
                    action_type=ActionType.SEND_UNIT,
                    actor=Owner.AI,
                    target_lane=lane_id,
                    entity_type=ut,
                    cost=cost,
                ))
                for quantity in (2, 3, 4):
                    wave_cost = cost * quantity
                    if game_state.ai_resource >= wave_cost and ut in (UnitType.FAST, UnitType.SWARM):
                        candidates.append(Action(
                            action_type=ActionType.SEND_UNIT,
                            actor=Owner.AI,
                            target_lane=lane_id,
                            entity_type=ut,
                            cost=wave_cost,
                            metadata={"quantity": quantity},
                        ))
                if ut == UnitType.TANK and game_state.ai_resource >= cost * 2:
                    candidates.append(Action(
                        action_type=ActionType.SEND_UNIT,
                        actor=Owner.AI,
                        target_lane=lane_id,
                        entity_type=ut,
                        cost=cost * 2,
                        metadata={"quantity": 2},
                    ))

    return candidates


# ============================================================
# Base class
# ============================================================

class AIAgent:
    def __init__(self, name: str):
        self.name = name
        self.decision_cooldown = 0.0
        self.last_score = 0.0

    def decide_action(self, game_state: GameState) -> Tuple[Action, float]:
        """Trả về (Action, score)"""
        raise NotImplementedError

    def update(self, delta_time: float):
        self.decision_cooldown = max(0.0, self.decision_cooldown - delta_time)

    def should_decide(self) -> bool:
        return self.decision_cooldown <= 0

    def reset_cooldown(self):
        self.decision_cooldown = AI_DECISION_INTERVAL


# ============================================================
# 1. Random AI
# ============================================================

class RandomAI(AIAgent):
    """Chọn hành động ngẫu nhiên trong tập hợp hợp lệ - baseline thấp nhất"""

    def __init__(self):
        super().__init__("random")

    def decide_action(self, game_state: GameState) -> Tuple[Action, float]:
        candidates = _generate_candidate_actions(game_state)
        # Lọc bỏ những action quá tốn tiền
        valid = [a for a in candidates
                 if a.cost <= game_state.ai_resource]
        if not valid:
            return Action(action_type=ActionType.NO_ACTION, actor=Owner.AI), 0.0

        chosen = random.choice(valid)
        return chosen, 0.0


# ============================================================
# 2. Rule-based AI
# ============================================================

class RuleBasedAI(AIAgent):
    """
    Dùng luật đơn giản, không chấm utility sâu.
    Tài liệu: 02 - section 12
    """

    def __init__(self):
        super().__init__("rule_based")

    def decide_action(self, game_state: GameState) -> Tuple[Action, float]:
        resource = game_state.ai_resource
        ai_hp_ratio = game_state.ai_base.hp_ratio()
        player_hp_ratio = game_state.player_base.hp_ratio()
        num_lanes = len(game_state.lanes)

        # === Luật 1: Nếu AI đang bị ép mạnh ở lane nào, xây hoặc nâng cấp tháp ===
        for lane_id in range(num_lanes):
            enemy_units = [u for u in game_state.active_units
                           if u.owner == Owner.PLAYER and u.lane_id == lane_id]
            if len(enemy_units) >= 2 and ai_hp_ratio < 0.7:
                # Ưu tiên nâng cấp tháp hiện có
                ai_towers = game_state.get_towers_by_lane(Owner.AI, lane_id)
                for t in ai_towers:
                    if t.can_upgrade() and resource >= t.get_upgrade_cost():
                        action = Action(
                            action_type=ActionType.UPGRADE_TOWER,
                            actor=Owner.AI,
                            target_lane=lane_id,
                            target_tower_id=t.tower_id,
                            cost=t.get_upgrade_cost(),
                        )
                        return action, 2.0

                # Xây tháp nặng nếu lane chưa có
                if not ai_towers and resource >= TOWER_CONFIGS[TowerType.HEAVY][1]["cost"]:
                    slot = _get_first_free_slot(game_state, lane_id)
                    if slot is not None:
                        cost = TOWER_CONFIGS[TowerType.HEAVY][1]["cost"]
                        return Action(
                            action_type=ActionType.BUILD_TOWER,
                            actor=Owner.AI,
                            target_lane=lane_id,
                            entity_type=TowerType.HEAVY,
                            cost=cost,
                            metadata={"slot": slot},
                        ), 2.5

        # === Luật 2: Nếu căn cứ AI còn ổn và có tài nguyên, tấn công lane yếu nhất ===
        if ai_hp_ratio > 0.5 and resource >= UNIT_CONFIGS[UnitType.FAST]["cost"]:
            weakest_lane = self._find_weakest_player_lane(game_state)
            if weakest_lane is not None:
                # Nếu player base yếu, gửi quân trâu
                if player_hp_ratio < 0.5 and resource >= UNIT_CONFIGS[UnitType.TANK]["cost"]:
                    return Action(
                        action_type=ActionType.SEND_UNIT,
                        actor=Owner.AI,
                        target_lane=weakest_lane,
                        entity_type=UnitType.TANK,
                        cost=UNIT_CONFIGS[UnitType.TANK]["cost"],
                    ), 1.8
                else:
                    return Action(
                        action_type=ActionType.SEND_UNIT,
                        actor=Owner.AI,
                        target_lane=weakest_lane,
                        entity_type=UnitType.FAST,
                        cost=UNIT_CONFIGS[UnitType.FAST]["cost"],
                    ), 1.5

        # === Luật 3: Nếu không có gì cấp bách, xây tháp ở lane chưa có tháp ===
        for lane_id in range(num_lanes):
            ai_towers = game_state.get_towers_by_lane(Owner.AI, lane_id)
            if not ai_towers and resource >= TOWER_CONFIGS[TowerType.BALANCED][1]["cost"]:
                slot = _get_first_free_slot(game_state, lane_id)
                if slot is not None:
                    cost = TOWER_CONFIGS[TowerType.BALANCED][1]["cost"]
                    return Action(
                        action_type=ActionType.BUILD_TOWER,
                        actor=Owner.AI,
                        target_lane=lane_id,
                        entity_type=TowerType.BALANCED,
                        cost=cost,
                        metadata={"slot": slot},
                    ), 1.2

        # === Luật 4: Tiết kiệm ===
        return Action(action_type=ActionType.SAVE_RESOURCE, actor=Owner.AI, cost=0), 0.5

    def _find_weakest_player_lane(self, game_state: GameState) -> Optional[int]:
        """Tìm lane phòng thủ yếu nhất của player (ít tháp nhất)"""
        scores = []
        for lane_id in range(len(game_state.lanes)):
            tower_count = len(game_state.get_towers_by_lane(Owner.PLAYER, lane_id))
            scores.append((tower_count, lane_id))
        scores.sort()
        return scores[0][1] if scores else None


# ============================================================
# 3. Heuristic AI
# ============================================================

class HeuristicAI(AIAgent):
    """
    Dùng HeuristicEvaluator để chấm điểm candidate actions, greedy chọn tốt nhất.
    Tài liệu: 02 - section 11 (pipeline), 03 - section 3.1, 3.2
    """

    def __init__(self, profile: str = "balanced"):
        super().__init__(f"heuristic_{profile}")
        self.evaluator = HeuristicEvaluator(profile=profile)

    def decide_action(self, game_state: GameState) -> Tuple[Action, float]:
        # Bước 1: Tính lane summaries (quan sát trạng thái)
        lane_summaries = self.evaluator.compute_lane_summaries(game_state)

        # Bước 2: Sinh candidate actions
        candidates = _generate_candidate_actions(game_state)

        # Bước 3: Filter candidates đủ tiền
        valid = [a for a in candidates if a.cost <= game_state.ai_resource]

        if not valid:
            return Action(action_type=ActionType.NO_ACTION, actor=Owner.AI), 0.0

        # Bước 4: Chấm điểm từng action
        scored: List[Tuple[float, Action]] = []
        for action in valid:
            score = self.evaluator.score(action, game_state, lane_summaries)
            scored.append((score, action))

        # Bước 5: Greedy - chọn action điểm cao nhất
        scored.sort(key=lambda x: x[0], reverse=True)
        best_score, best_action = scored[0]

        return best_action, best_score

    def get_lane_summaries(self, game_state: GameState) -> List[LaneSummary]:
        return self.evaluator.compute_lane_summaries(game_state)


# ============================================================
# Factory
# ============================================================

def create_ai(ai_type: str, profile: str = "balanced") -> AIAgent:
    """
    Factory tạo AI agent.
    ai_type: "random" | "rule_based" | "heuristic"
    profile (chỉ dùng với heuristic): "defensive" | "aggressive" | "balanced"
    """
    if ai_type == "random":
        return RandomAI()
    elif ai_type == "rule_based":
        return RuleBasedAI()
    elif ai_type == "heuristic":
        return HeuristicAI(profile=profile)
    else:
        raise ValueError(f"Unknown AI type: {ai_type}")
