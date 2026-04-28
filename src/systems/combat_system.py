"""
CombatSystem - Xử lý tháp bắn quân, quân vào base, tiêu diệt đơn vị
"""
from __future__ import annotations
from typing import List, Tuple, Callable, Optional
import math

from src.models import GameState, Tower, Unit, Owner


class CombatSystem:
    def __init__(self, unit_manager, resource_manager):
        self.unit_manager = unit_manager
        self.resource_manager = resource_manager

    def update(self, game_state: GameState, delta_time: float):
        """
        1. Tháp chọn và bắn mục tiêu
        2. Quân đã đến base gây damage
        3. Xử lý quân chết
        """
        # --- Tháp bắn ---
        all_towers = game_state.player_towers + game_state.ai_towers
        for tower in all_towers:
            if tower.attack_cooldown > 0:
                continue
            # Chọn mục tiêu: quân địch gần nhất trong tầm
            target = self._select_target_for_tower(tower, game_state)
            if target is not None:
                self._tower_attack(tower, target, game_state)

        # --- Quân vào base ---
        units_at_base = [u for u in game_state.active_units if u.position >= 1.0]
        for unit in units_at_base:
            self._unit_attack_base(unit, game_state)

        # Xóa quân chết và quân đã qua base
        dead_and_done = set()
        for unit in game_state.active_units:
            if unit.is_dead() or unit.position >= 1.0:
                dead_and_done.add(unit.unit_id)

        game_state.active_units = [u for u in game_state.active_units
                                    if u.unit_id not in dead_and_done]

    def _select_target_for_tower(self, tower: Tower, game_state: GameState) -> Optional[Unit]:
        """Chọn quân địch tiến xa nhất trong tầm bắn"""
        enemy_owner = Owner.AI if tower.owner == Owner.PLAYER else Owner.PLAYER
        enemies_in_lane = [u for u in game_state.active_units
                           if u.owner == enemy_owner and u.lane_id == tower.lane_id]

        in_range = []
        for u in enemies_in_lane:
            # Tính vị trí pixel để check range
            unit_screen = self.unit_manager.get_screen_pos(u)
            tx, ty = tower.position
            dist = math.sqrt((unit_screen[0] - tx)**2 + (unit_screen[1] - ty)**2)
            if dist <= tower.range:
                in_range.append((u.position, u))  # sort by progress

        if not in_range:
            return None
        # Ưu tiên quân gần base nhất (progress cao nhất)
        in_range.sort(key=lambda x: x[0], reverse=True)
        return in_range[0][1]

    def _tower_attack(self, tower: Tower, target: Unit, game_state: GameState):
        """Tháp tấn công quân mục tiêu"""
        is_dead = target.take_damage(tower.damage)
        tower.attack_cooldown = tower.attack_interval

        # Ghi thống kê damage
        if tower.owner == Owner.PLAYER:
            game_state.player_unit_damage_dealt += tower.damage
            game_state.player_damage_dealt += tower.damage
        else:
            game_state.ai_unit_damage_dealt += tower.damage
            game_state.ai_damage_dealt += tower.damage

        # Nếu quân chết - thưởng tài nguyên
        if is_dead:
            killer = tower.owner
            reward = target.reward
            self.resource_manager.add_kill_reward(game_state, killer, reward)
            if killer == Owner.PLAYER:
                game_state.player_kills += 1
            else:
                game_state.ai_kills += 1

    def _unit_attack_base(self, unit: Unit, game_state: GameState):
        """Quân đến base gây damage và bị loại"""
        if unit.owner == Owner.PLAYER:
            # Player unit tấn công AI base
            actual = game_state.ai_base.take_damage(unit.damage_to_base)
            game_state.player_base_damage_dealt += actual
            game_state.player_base_damage_by_lane[unit.lane_id] = (
                game_state.player_base_damage_by_lane.get(unit.lane_id, 0.0) + actual
            )
            game_state.player_damage_dealt += actual
        else:
            # AI unit tấn công Player base
            actual = game_state.player_base.take_damage(unit.damage_to_base)
            game_state.ai_base_damage_dealt += actual
            game_state.ai_base_damage_by_lane[unit.lane_id] = (
                game_state.ai_base_damage_by_lane.get(unit.lane_id, 0.0) + actual
            )
            game_state.ai_damage_dealt += actual
