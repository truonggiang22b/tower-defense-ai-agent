"""
GameEngine - Bộ điều phối trung tâm của game loop
Theo tài liệu 04 - section 3.1
"""
from __future__ import annotations
import time
from typing import Optional

from src.models import (
    GameState, Base, Owner, Action, ActionType,
    TowerType, UnitType, TOWER_CONFIGS, UNIT_CONFIGS
)
from src.systems.map_manager import MapManager, PLAYER_BASE_X, AI_BASE_X, BASE_Y
from src.systems.resource_manager import ResourceManager, INCOME_RATE
from src.systems.tower_manager import TowerManager
from src.systems.unit_manager import UnitManager
from src.systems.combat_system import CombatSystem
from src.systems.game_logger import GameLogger
from src.ai.ai_agent import AIAgent, AI_DECISION_INTERVAL


INITIAL_HP = 500.0
INITIAL_RESOURCE = 100.0


def build_initial_state(map_manager: MapManager) -> GameState:
    """Tạo GameState mới từ đầu"""
    return GameState(
        player_base=Base(
            owner=Owner.PLAYER,
            hp=INITIAL_HP,
            max_hp=INITIAL_HP,
            position=(PLAYER_BASE_X, BASE_Y),
        ),
        ai_base=Base(
            owner=Owner.AI,
            hp=INITIAL_HP,
            max_hp=INITIAL_HP,
            position=(AI_BASE_X, BASE_Y),
        ),
        player_resource=INITIAL_RESOURCE,
        ai_resource=INITIAL_RESOURCE,
        resource_income_rate=INCOME_RATE,
        lanes=map_manager.lanes,
        max_match_time=300.0,
    )


class GameEngine:
    """
    Điều phối game loop:
    1. Update thời gian
    2. Cộng tài nguyên
    3. Player action
    4. AI decide + execute
    5. Unit movement
    6. Combat
    7. Check win
    8. Log
    """

    def __init__(self, ai_agent: AIAgent, headless: bool = False):
        self.map_manager = MapManager()
        self.resource_manager = ResourceManager()
        self.tower_manager = TowerManager(self.map_manager)
        self.unit_manager = UnitManager(self.map_manager)
        self.logger = GameLogger()
        self.combat_system = CombatSystem(self.unit_manager, self.resource_manager)

        self.ai_agent = ai_agent
        self.headless = headless

        self.game_state: Optional[GameState] = None
        self.running = False
        self.paused = False

        # AI cooldown tracking
        self.ai_cooldown = 0.0

        # Lane summaries (cache for UI display)
        self.lane_summaries = []
        self.last_ai_action: Optional[Action] = None
        self.last_ai_score = 0.0
        self.last_ai_decision_ms = 0.0

    def start_match(self, match_id: str = "match_001"):
        """Khởi tạo trận đấu mới"""
        from src.models.game_state import _unit_id_counter
        import src.models.game_state as gs_module
        gs_module._unit_id_counter = 0

        self.game_state = build_initial_state(self.map_manager)
        self.ai_cooldown = 0.0
        self.running = True
        self.paused = False
        self.logger.start_match(match_id, self.ai_agent.name)
        self.lane_summaries = []
        self.last_ai_action = None
        self.last_ai_score = 0.0
        self.last_ai_decision_ms = 0.0

    def update(self, delta_time: float) -> bool:
        """
        Update một tick của game.
        Trả về True nếu game vẫn đang chạy.
        """
        if not self.running or self.paused:
            return self.running
        if self.game_state is None:
            return False

        gs = self.game_state

        # 1. Tăng thời gian
        gs.match_time += delta_time

        # 2. Cộng tài nguyên
        self.resource_manager.update(gs, delta_time)

        # 3. Cập nhật cooldown tháp
        self.tower_manager.update(gs, delta_time)

        # 4. AI quyết định
        self.ai_cooldown = max(0.0, self.ai_cooldown - delta_time)
        if self.ai_cooldown <= 0:
            self._ai_step()
            self.ai_cooldown = AI_DECISION_INTERVAL

        # 5. Di chuyển quân
        self.unit_manager.update(gs, delta_time)

        # 6. Combat
        self.combat_system.update(gs, delta_time)

        # 7. Kiểm tra kết thúc
        if gs.is_game_over():
            self.running = False
            self.logger.end_match(gs)
            return False

        return True

    def _ai_step(self):
        """Thực hiện một bước quyết định AI"""
        gs = self.game_state
        t_start = time.perf_counter()
        action, score = self.ai_agent.decide_action(gs)
        t_end = time.perf_counter()
        decision_ms = (t_end - t_start) * 1000.0
        self.last_ai_action = action
        self.last_ai_score = score
        self.last_ai_decision_ms = decision_ms

        # Cập nhật lane summaries nếu là heuristic
        if hasattr(self.ai_agent, 'get_lane_summaries'):
            self.lane_summaries = self.ai_agent.get_lane_summaries(gs)

        self.logger.log_ai_action(action, score, decision_ms)
        self.execute_action(action, Owner.AI)

    def execute_action(self, action: Action, owner: Owner) -> bool:
        """
        Thực thi hành động cho player hoặc AI.
        Trả về True nếu thành công.
        """
        gs = self.game_state
        if gs is None:
            return False

        if action.action_type == ActionType.NO_ACTION:
            return True

        if action.action_type == ActionType.SAVE_RESOURCE:
            if owner == Owner.AI:
                gs.ai_economy_count += 1
            return True

        # Kiểm tra tài nguyên
        if not self.resource_manager.can_afford(gs, owner, action.cost):
            return False

        if action.action_type == ActionType.BUILD_TOWER:
            return self._execute_build_tower(action, owner)

        elif action.action_type == ActionType.UPGRADE_TOWER:
            return self._execute_upgrade_tower(action, owner)

        elif action.action_type == ActionType.SEND_UNIT:
            return self._execute_send_unit(action, owner)

        return False

    def _execute_build_tower(self, action: Action, owner: Owner) -> bool:
        gs = self.game_state
        lane_id = action.target_lane
        tower_type = action.entity_type
        slot = action.metadata.get("slot")

        if lane_id is None or tower_type is None or slot is None:
            return False

        # Kiểm tra slot còn trống
        free_slots = gs.get_free_build_slots(owner, lane_id)
        if slot not in free_slots:
            # Tìm slot khả dụng khác
            if not free_slots:
                return False
            slot = free_slots[0]

        cost = action.cost
        if not self.resource_manager.can_afford(gs, owner, cost):
            return False

        self.tower_manager.build_tower(gs, owner, lane_id, tower_type, slot)
        self.resource_manager.spend(gs, owner, cost)

        # Ghi thống kê
        if owner == Owner.PLAYER:
            gs.player_defense_count += 1
        else:
            gs.ai_defense_count += 1

        return True

    def _execute_upgrade_tower(self, action: Action, owner: Owner) -> bool:
        gs = self.game_state
        tower_id = action.target_tower_id

        if tower_id is None:
            return False

        tower = self.tower_manager.get_tower_by_id(gs, tower_id)
        if tower is None or tower.owner != owner:
            return False

        upgrade_cost = tower.get_upgrade_cost()
        if not self.resource_manager.can_afford(gs, owner, upgrade_cost):
            return False
        if not tower.can_upgrade():
            return False

        self.tower_manager.upgrade_tower(gs, tower)
        self.resource_manager.spend(gs, owner, upgrade_cost)

        if owner == Owner.PLAYER:
            gs.player_defense_count += 1
        else:
            gs.ai_defense_count += 1

        return True

    def _execute_send_unit(self, action: Action, owner: Owner) -> bool:
        gs = self.game_state
        lane_id = action.target_lane
        unit_type = action.entity_type

        if lane_id is None or unit_type is None:
            return False

        cost = action.cost
        if not self.resource_manager.can_afford(gs, owner, cost):
            return False

        quantity = int(action.metadata.get("quantity", 1))
        quantity = max(1, quantity)
        for _ in range(quantity):
            self.unit_manager.spawn_unit(gs, owner, lane_id, unit_type)
        self.resource_manager.spend(gs, owner, cost)

        if owner == Owner.PLAYER:
            gs.player_attack_count += 1
            gs.player_attack_lane_counts[lane_id] = gs.player_attack_lane_counts.get(lane_id, 0) + quantity
            gs.player_unit_type_counts[unit_type.value] = gs.player_unit_type_counts.get(unit_type.value, 0) + quantity
        else:
            gs.ai_attack_count += 1
            gs.ai_attack_lane_counts[lane_id] = gs.ai_attack_lane_counts.get(lane_id, 0) + quantity
            gs.ai_unit_type_counts[unit_type.value] = gs.ai_unit_type_counts.get(unit_type.value, 0) + quantity

        return True

    def get_state(self) -> Optional[GameState]:
        return self.game_state

    def end_match(self):
        """Kết thúc trận thủ công"""
        if self.running and self.game_state:
            self.running = False
            self.logger.end_match(self.game_state)
