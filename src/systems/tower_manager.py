"""
TowerManager - Quản lý tháp: xây, nâng cấp, chọn mục tiêu
"""
from __future__ import annotations
from typing import List, Optional
import math

from src.models import (
    GameState, Tower, Unit, TowerType, Owner,
    Action, ActionType, TOWER_CONFIGS
)
from src.systems.map_manager import MapManager, NUM_SLOTS_PER_SIDE


class TowerManager:
    def __init__(self, map_manager: MapManager):
        self.map_manager = map_manager

    def build_tower(self, game_state: GameState, owner: Owner,
                    lane_id: int, tower_type: TowerType, slot_index: int) -> Optional[Tower]:
        """Xây tháp mới tại slot. Không kiểm tra tài nguyên ở đây (GameEngine lo)."""
        pos = self.map_manager.get_build_slot_pos(owner, lane_id, slot_index)
        tower_id = game_state.next_tower_id()
        tower = Tower(
            tower_id=tower_id,
            tower_type=tower_type,
            level=1,
            owner=owner,
            lane_id=lane_id,
            slot_index=slot_index,
            position=pos,
            hp=100.0,
        )
        if owner == Owner.PLAYER:
            game_state.player_towers.append(tower)
        else:
            game_state.ai_towers.append(tower)
        return tower

    def upgrade_tower(self, game_state: GameState, tower: Tower) -> bool:
        """Nâng cấp tháp. Trả về True nếu thành công."""
        if not tower.can_upgrade():
            return False
        tower.upgrade()
        return True

    def get_tower_by_id(self, game_state: GameState, tower_id: int) -> Optional[Tower]:
        for t in game_state.player_towers + game_state.ai_towers:
            if t.tower_id == tower_id:
                return t
        return None

    def update(self, game_state: GameState, delta_time: float):
        """Giảm cooldown cho tất cả tháp"""
        for tower in game_state.player_towers + game_state.ai_towers:
            if tower.attack_cooldown > 0:
                tower.attack_cooldown = max(0.0, tower.attack_cooldown - delta_time)

    def select_target(self, tower: Tower, units: List[Unit]) -> Optional[Unit]:
        """Chọn mục tiêu: quân địch gần nhất trong tầm bắn"""
        enemies = [u for u in units if u.owner != tower.owner]
        in_range = []
        for u in enemies:
            px, py = u.screen_pos if hasattr(u, 'screen_pos') else u.position  # type: ignore
            tx, ty = tower.position
            dist = math.sqrt((px - tx)**2 + (py - ty)**2)
            if dist <= tower.range:
                in_range.append((dist, u))
        if not in_range:
            return None
        # Ưu tiên quân có progress cao nhất (gần base nhất) - nguy hiểm nhất
        in_range.sort(key=lambda x: x[1].position, reverse=True)
        return in_range[0][1]

    def get_build_cost(self, tower_type: TowerType) -> int:
        return TOWER_CONFIGS[tower_type][1]["cost"]

    def get_valid_build_slots(self, game_state: GameState, owner: Owner, lane_id: int) -> List[int]:
        return game_state.get_free_build_slots(owner, lane_id)

    def get_upgradeable_towers(self, game_state: GameState, owner: Owner) -> List[Tower]:
        towers = game_state.player_towers if owner == Owner.PLAYER else game_state.ai_towers
        return [t for t in towers if t.can_upgrade()]
