"""
UnitManager - Quản lý sinh quân, di chuyển, cập nhật trạng thái
"""
from __future__ import annotations
from typing import List, Optional

from src.models import GameState, Unit, UnitType, Owner, UNIT_CONFIGS
from src.systems.map_manager import MapManager, LANE_WIDTH_PIXELS, PLAYER_BASE_X, AI_BASE_X


class UnitManager:
    def __init__(self, map_manager: MapManager):
        self.map_manager = map_manager

    def spawn_unit(self, game_state: GameState, owner: Owner,
                   lane_id: int, unit_type: UnitType) -> Unit:
        """Sinh quân mới tại điểm spawn"""
        unit = Unit(
            unit_type=unit_type,
            owner=owner,
            lane_id=lane_id,
            position=0.0,  # tiến trình bắt đầu
        )
        game_state.active_units.append(unit)
        return unit

    def get_spawn_cost(self, unit_type: UnitType) -> int:
        return UNIT_CONFIGS[unit_type]["cost"]

    def update(self, game_state: GameState, delta_time: float):
        """Cập nhật vị trí quân theo delta_time"""
        lane_pixel_length = (AI_BASE_X - 30) - (PLAYER_BASE_X + 30)

        for unit in game_state.active_units:
            # Tính progress tăng thêm (speed = pixels/second)
            progress_delta = unit.speed / lane_pixel_length * delta_time
            unit.position = min(1.0, unit.position + progress_delta)

    def get_screen_pos(self, unit: Unit) -> tuple:
        return self.map_manager.get_unit_position_pixels(
            unit.owner, unit.lane_id, unit.position
        )

    def remove_dead_units(self, game_state: GameState):
        game_state.active_units = [u for u in game_state.active_units if not u.is_dead()]

    def get_units_at_base(self, game_state: GameState) -> List[Unit]:
        """Lấy danh sách quân đã đến căn cứ đối phương (progress >= 1.0)"""
        return [u for u in game_state.active_units if u.position >= 1.0]

    def get_enemy_units_in_lane(self, game_state: GameState,
                                defender_owner: Owner, lane_id: int) -> List[Unit]:
        """Lấy quân địch đang tiến vào base của defender"""
        attacker = Owner.AI if defender_owner == Owner.PLAYER else Owner.PLAYER
        return [u for u in game_state.active_units
                if u.owner == attacker and u.lane_id == lane_id]
