"""Combat system: towers attack units, units damage bases, dead units are removed."""
from __future__ import annotations

from typing import Optional
import math

from src.models import GameState, Tower, Unit, Owner


class CombatSystem:
    def __init__(self, unit_manager, resource_manager):
        self.unit_manager = unit_manager
        self.resource_manager = resource_manager
        self.event_sink = None

    def update(self, game_state: GameState, delta_time: float):
        all_towers = game_state.player_towers + game_state.ai_towers
        for tower in all_towers:
            if tower.attack_cooldown > 0:
                continue
            target = self._select_target_for_tower(tower, game_state)
            if target is not None:
                self._tower_attack(tower, target, game_state)

        units_at_base = [u for u in game_state.active_units if u.position >= 1.0]
        for unit in units_at_base:
            self._unit_attack_base(unit, game_state)

        dead_and_done = set()
        for unit in game_state.active_units:
            if unit.is_dead() or unit.position >= 1.0:
                dead_and_done.add(unit.unit_id)

        game_state.active_units = [
            u for u in game_state.active_units if u.unit_id not in dead_and_done
        ]

    def _select_target_for_tower(self, tower: Tower, game_state: GameState) -> Optional[Unit]:
        enemy_owner = Owner.AI if tower.owner == Owner.PLAYER else Owner.PLAYER
        enemies_in_lane = [
            u for u in game_state.active_units
            if u.owner == enemy_owner and u.lane_id == tower.lane_id
        ]

        in_range = []
        for unit in enemies_in_lane:
            unit_screen = self.unit_manager.get_screen_pos(unit)
            tx, ty = tower.position
            dist = math.sqrt((unit_screen[0] - tx) ** 2 + (unit_screen[1] - ty) ** 2)
            if dist <= tower.range:
                in_range.append((unit.position, unit))

        if not in_range:
            return None
        in_range.sort(key=lambda x: x[0], reverse=True)
        return in_range[0][1]

    def _tower_attack(self, tower: Tower, target: Unit, game_state: GameState):
        source_pos = tower.position
        target_pos = self.unit_manager.get_screen_pos(target)
        is_dead = target.take_damage(tower.damage)
        tower.attack_cooldown = tower.attack_interval

        actor = self._owner_label_vi(tower.owner)
        self._emit(
            "damage",
            f"Tháp của {actor} bắn tuyến {target.lane_id + 1}, gây {tower.damage:.0f} sát thương",
            amount=tower.damage,
            source_pos=source_pos,
            target_pos=target_pos,
            lane=target.lane_id,
        )

        if tower.owner == Owner.PLAYER:
            game_state.player_unit_damage_dealt += tower.damage
            game_state.player_damage_dealt += tower.damage
        else:
            game_state.ai_unit_damage_dealt += tower.damage
            game_state.ai_damage_dealt += tower.damage

        if is_dead:
            killer = tower.owner
            reward = target.reward
            self.resource_manager.add_kill_reward(game_state, killer, reward)
            self._emit(
                "reward",
                f"{actor} hạ một quân, +{reward} vàng",
                pos=target_pos,
                lane=target.lane_id,
            )
            if killer == Owner.PLAYER:
                game_state.player_kills += 1
            else:
                game_state.ai_kills += 1

    def _unit_attack_base(self, unit: Unit, game_state: GameState):
        source_pos = self.unit_manager.get_screen_pos(unit)
        target_pos = game_state.lanes[unit.lane_id].get_base_target(unit.owner)
        if unit.owner == Owner.PLAYER:
            actual = game_state.ai_base.take_damage(unit.damage_to_base)
            game_state.player_base_damage_dealt += actual
            game_state.player_base_damage_by_lane[unit.lane_id] = (
                game_state.player_base_damage_by_lane.get(unit.lane_id, 0.0) + actual
            )
            game_state.player_damage_dealt += actual
        else:
            actual = game_state.player_base.take_damage(unit.damage_to_base)
            game_state.ai_base_damage_dealt += actual
            game_state.ai_base_damage_by_lane[unit.lane_id] = (
                game_state.ai_base_damage_by_lane.get(unit.lane_id, 0.0) + actual
            )
            game_state.ai_damage_dealt += actual

        actor = self._owner_label_vi(unit.owner)
        self._emit(
            "base_damage",
            f"Quân của {actor} xuyên thủng tuyến {unit.lane_id + 1}, gây {actual:.0f} sát thương căn cứ",
            amount=actual,
            source_pos=source_pos,
            target_pos=target_pos,
            lane=unit.lane_id,
        )

    def _emit(self, kind: str, text: str, **payload):
        if self.event_sink:
            self.event_sink(kind, text, **payload)

    def _owner_label_vi(self, owner: Owner) -> str:
        return "Người chơi" if owner == Owner.PLAYER else "AI"
