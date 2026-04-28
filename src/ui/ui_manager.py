"""Pygame tactical interface for the tower-defense AI demo."""
from __future__ import annotations

import math
from typing import List, Optional

import pygame

from src.models import (
    Action,
    ActionType,
    GameState,
    LaneSummary,
    Owner,
    TOWER_CONFIGS,
    UNIT_CONFIGS,
    TowerType,
    UnitType,
)
from src.systems.map_manager import (
    AI_BASE_X,
    BASE_Y,
    LANE_Y_POSITIONS,
    NUM_SLOTS_PER_SIDE,
    PLAYER_BASE_X,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    MapManager,
)
from src.ui.assets import AssetManager
from src.ui.theme import Fonts, Layout, Palette, danger_color, lerp_color
from src.ui.widgets import Button, draw_bar, draw_panel, draw_text


PANEL_HEIGHT = Layout.COMMAND_HEIGHT
GAME_AREA_HEIGHT = SCREEN_HEIGHT - PANEL_HEIGHT


class UIManager:
    def __init__(self, game_engine, map_manager: MapManager):
        self.engine = game_engine
        self.map_manager = map_manager

        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tower Defense AI - Tactical Demo")
        self.assets = AssetManager()

        self.fonts = Fonts(
            title=pygame.font.SysFont("Segoe UI", 28, bold=True),
            large=pygame.font.SysFont("Segoe UI", 22, bold=True),
            medium=pygame.font.SysFont("Segoe UI", 16),
            small=pygame.font.SysFont("Segoe UI", 13),
            tiny=pygame.font.SysFont("Segoe UI", 11),
        )

        self.selected_tower_type: Optional[TowerType] = None
        self.selected_unit_type: Optional[UnitType] = None
        self.selected_lane: Optional[int] = None
        self.status_msg = ""
        self.status_timer = 0.0
        self.show_ai_debug = False
        self.mouse_pos = (0, 0)

        self._build_buttons()
        self._attach_button_icons()

    def _build_buttons(self) -> None:
        y0 = GAME_AREA_HEIGHT + 20
        x = 20
        w = 108
        h = 42
        gap = 10

        self.btn_tower_fast = Button(
            pygame.Rect(x, y0 + 28, w, h), "Tháp Nhanh", Palette.PLAYER_DARK,
            (31, 102, 196), lambda: self._select_tower_type(TowerType.FAST),
            sublabel=f"{TOWER_CONFIGS[TowerType.FAST][1]['cost']} vàng",
        )
        self.btn_tower_heavy = Button(
            pygame.Rect(x + (w + gap), y0 + 28, w, h), "Tháp Nặng", Palette.AI_DARK,
            (168, 44, 55), lambda: self._select_tower_type(TowerType.HEAVY),
            sublabel=f"{TOWER_CONFIGS[TowerType.HEAVY][1]['cost']} vàng",
        )
        self.btn_tower_balanced = Button(
            pygame.Rect(x + 2 * (w + gap), y0 + 28, w, h), "Tháp CB", (30, 111, 69),
            (41, 145, 87), lambda: self._select_tower_type(TowerType.BALANCED),
            sublabel=f"{TOWER_CONFIGS[TowerType.BALANCED][1]['cost']} vàng",
        )

        unit_y = y0 + 106
        self.btn_unit_fast = Button(
            pygame.Rect(x, unit_y, w, h), "Quân Nhanh", (138, 108, 16),
            (187, 145, 26), lambda: self._select_unit_type(UnitType.FAST),
            sublabel=f"{UNIT_CONFIGS[UnitType.FAST]['cost']} vàng",
        )
        self.btn_unit_tank = Button(
            pygame.Rect(x + (w + gap), unit_y, w, h), "Quân Trâu", (120, 72, 25),
            (161, 92, 32), lambda: self._select_unit_type(UnitType.TANK),
            sublabel=f"{UNIT_CONFIGS[UnitType.TANK]['cost']} vàng",
        )
        self.btn_unit_swarm = Button(
            pygame.Rect(x + 2 * (w + gap), unit_y, w, h), "Quân Rẻ", (113, 49, 148),
            (149, 69, 189), lambda: self._select_unit_type(UnitType.SWARM),
            sublabel=f"{UNIT_CONFIGS[UnitType.SWARM]['cost']} vàng",
        )

        lane_x = 392
        self.btn_lanes: List[Button] = []
        for i in range(3):
            self.btn_lanes.append(Button(
                pygame.Rect(lane_x + i * 72, y0 + 56, 62, 42),
                f"L{i + 1}", Palette.SURFACE_3, (47, 62, 88),
                lambda lid=i: self._select_lane(lid),
            ))

        action_x = 620
        self.btn_build = Button(
            pygame.Rect(action_x, y0 + 28, 112, 42), "Xây Tháp",
            (37, 76, 145), (49, 104, 191), self._action_build_tower,
        )
        self.btn_send = Button(
            pygame.Rect(action_x + 122, y0 + 28, 112, 42), "Gửi Quân",
            (30, 117, 71), (39, 154, 91), self._action_send_unit,
        )
        self.btn_upgrade = Button(
            pygame.Rect(action_x, y0 + 88, 234, 42), "Nâng Cấp Lane",
            (132, 88, 20), (175, 119, 27), self._action_upgrade,
        )
        self.btn_debug = Button(
            pygame.Rect(SCREEN_WIDTH - 128, y0, 108, 42), "AI Debug",
            Palette.SURFACE_3, (53, 67, 94), self._toggle_debug,
        )

        self.all_buttons = [
            self.btn_tower_fast, self.btn_tower_heavy, self.btn_tower_balanced,
            self.btn_unit_fast, self.btn_unit_tank, self.btn_unit_swarm,
            *self.btn_lanes, self.btn_build, self.btn_send, self.btn_upgrade,
            self.btn_debug,
        ]

    def _attach_button_icons(self) -> None:
        self.btn_tower_fast.icon = self.assets.tower_icon(TowerType.FAST, 24)
        self.btn_tower_heavy.icon = self.assets.tower_icon(TowerType.HEAVY, 24)
        self.btn_tower_balanced.icon = self.assets.tower_icon(TowerType.BALANCED, 24)
        self.btn_unit_fast.icon = self.assets.unit_icon(UnitType.FAST, 23)
        self.btn_unit_tank.icon = self.assets.unit_icon(UnitType.TANK, 23)
        self.btn_unit_swarm.icon = self.assets.unit_icon(UnitType.SWARM, 23)

    def _toggle_debug(self) -> None:
        self.show_ai_debug = not self.show_ai_debug

    def _select_tower_type(self, tt: TowerType) -> None:
        self.selected_tower_type = tt
        self.selected_unit_type = None
        self.set_status(f"Đã chọn tháp {self._tower_label(tt)}")

    def _select_unit_type(self, ut: UnitType) -> None:
        self.selected_unit_type = ut
        self.selected_tower_type = None
        self.set_status(f"Đã chọn quân {self._unit_label(ut)}")

    def _select_lane(self, lane_id: int) -> None:
        self.selected_lane = lane_id
        self.set_status(f"Đã chọn Lane {lane_id + 1}")

    def _action_send_unit(self) -> None:
        if self.selected_unit_type is None:
            self.set_status("Chọn loại quân trước.")
            return
        if self.selected_lane is None:
            self.set_status("Chọn lane để gửi quân.")
            return
        gs = self.engine.get_state()
        if gs is None:
            return
        cost = UNIT_CONFIGS[self.selected_unit_type]["cost"]
        action = Action(ActionType.SEND_UNIT, Owner.PLAYER, self.selected_lane,
                        self.selected_unit_type, cost=cost)
        if self.engine.execute_action(action, Owner.PLAYER):
            self.set_status(f"Gửi {self._unit_label(self.selected_unit_type)} vào Lane {self.selected_lane + 1}")
        else:
            self.set_status("Không đủ tài nguyên để gửi quân.")

    def _action_build_tower(self) -> None:
        if self.selected_tower_type is None:
            self.set_status("Chọn loại tháp trước.")
            return
        if self.selected_lane is None:
            self.set_status("Chọn lane để xây tháp.")
            return
        gs = self.engine.get_state()
        if gs is None:
            return
        free_slots = gs.get_free_build_slots(Owner.PLAYER, self.selected_lane)
        if not free_slots:
            self.set_status("Lane này đã hết slot tháp.")
            return
        cost = TOWER_CONFIGS[self.selected_tower_type][1]["cost"]
        action = Action(
            ActionType.BUILD_TOWER,
            Owner.PLAYER,
            self.selected_lane,
            self.selected_tower_type,
            cost=cost,
            metadata={"slot": free_slots[0]},
        )
        if self.engine.execute_action(action, Owner.PLAYER):
            self.set_status(f"Xây {self._tower_label(self.selected_tower_type)} ở Lane {self.selected_lane + 1}")
        else:
            self.set_status("Không đủ tài nguyên hoặc slot không hợp lệ.")

    def _action_upgrade(self) -> None:
        if self.selected_lane is None:
            self.set_status("Chọn lane trước khi nâng cấp.")
            return
        gs = self.engine.get_state()
        if gs is None:
            return
        towers = gs.get_towers_by_lane(Owner.PLAYER, self.selected_lane)
        upgradable = [t for t in towers if t.can_upgrade() and gs.player_resource >= t.get_upgrade_cost()]
        if not upgradable:
            self.set_status("Không có tháp đủ điều kiện nâng cấp ở lane này.")
            return
        tower = upgradable[0]
        action = Action(
            ActionType.UPGRADE_TOWER,
            Owner.PLAYER,
            self.selected_lane,
            target_tower_id=tower.tower_id,
            cost=tower.get_upgrade_cost(),
        )
        if self.engine.execute_action(action, Owner.PLAYER):
            self.set_status(f"Nâng tháp #{tower.tower_id} lên cấp {tower.level}")
        else:
            self.set_status("Không đủ tài nguyên để nâng cấp.")

    def set_status(self, msg: str, duration: float = 2.8) -> None:
        self.status_msg = msg
        self.status_timer = duration

    def handle_event(self, event) -> bool:
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.MOUSEMOTION:
            self.mouse_pos = event.pos
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
            if event.key == pygame.K_d:
                self._toggle_debug()
            elif event.key == pygame.K_p:
                self.engine.paused = not self.engine.paused

        for btn in self.all_buttons:
            btn.handle_event(event)
        return True

    def update(self, dt: float) -> None:
        if self.status_timer > 0:
            self.status_timer = max(0.0, self.status_timer - dt)

    def render(self, game_state: Optional[GameState], lane_summaries: List[LaneSummary]) -> None:
        surface = self.screen
        self._draw_background(surface)
        if game_state is None:
            self._draw_start_screen(surface)
            pygame.display.flip()
            return

        self._sync_button_state(game_state)
        self._draw_top_hud(surface, game_state)
        self._draw_battlefield(surface, game_state, lane_summaries)
        self._draw_command_deck(surface, game_state)
        self._draw_status(surface)

        if self.show_ai_debug:
            self._draw_ai_debug(surface, game_state, lane_summaries)

        if game_state.is_game_over():
            self._draw_game_over(surface, game_state)

        pygame.display.flip()

    def _sync_button_state(self, gs: GameState) -> None:
        tower_buttons = {
            TowerType.FAST: self.btn_tower_fast,
            TowerType.HEAVY: self.btn_tower_heavy,
            TowerType.BALANCED: self.btn_tower_balanced,
        }
        unit_buttons = {
            UnitType.FAST: self.btn_unit_fast,
            UnitType.TANK: self.btn_unit_tank,
            UnitType.SWARM: self.btn_unit_swarm,
        }
        for tt, btn in tower_buttons.items():
            btn.selected = self.selected_tower_type == tt
            btn.enabled = gs.player_resource >= TOWER_CONFIGS[tt][1]["cost"]
        for ut, btn in unit_buttons.items():
            btn.selected = self.selected_unit_type == ut
            btn.enabled = gs.player_resource >= UNIT_CONFIGS[ut]["cost"]
        for i, btn in enumerate(self.btn_lanes):
            btn.selected = self.selected_lane == i
        self.btn_build.enabled = self.selected_tower_type is not None and self.selected_lane is not None
        self.btn_send.enabled = self.selected_unit_type is not None and self.selected_lane is not None
        self.btn_upgrade.enabled = self.selected_lane is not None
        self.btn_debug.selected = self.show_ai_debug

    def _draw_background(self, surface: pygame.Surface) -> None:
        bg = pygame.transform.smoothscale(self.assets.background, (SCREEN_WIDTH, GAME_AREA_HEIGHT))
        surface.blit(bg, (0, 0))
        pygame.draw.rect(surface, Palette.SURFACE, (0, GAME_AREA_HEIGHT, SCREEN_WIDTH, PANEL_HEIGHT))

    def _draw_start_screen(self, surface: pygame.Surface) -> None:
        txt = self.fonts.title.render("Tower Defense AI", True, Palette.TEXT)
        sub = self.fonts.medium.render("Đang khởi tạo trận đấu...", True, Palette.TEXT_MUTED)
        surface.blit(txt, txt.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 18)))
        surface.blit(sub, sub.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 18)))

    def _draw_top_hud(self, surface: pygame.Surface, gs: GameState) -> None:
        hud = pygame.Rect(16, 12, SCREEN_WIDTH - 32, 50)
        draw_panel(surface, hud, None, self.fonts.small, fill=(12, 18, 30), border=Palette.LINE_SOFT)
        draw_text(surface, "TACTICAL DEFENSE AI", (34, 24), self.fonts.large, Palette.TEXT)
        draw_text(surface, f"AI: {self.engine.ai_agent.name}", (304, 28), self.fonts.small, Palette.TEXT_MUTED)

        timer = f"{int(gs.match_time // 60):02d}:{int(gs.match_time % 60):02d} / {int(gs.max_match_time // 60):02d}:00"
        timer_txt = self.fonts.large.render(timer, True, Palette.RESOURCE)
        surface.blit(timer_txt, timer_txt.get_rect(center=(SCREEN_WIDTH // 2, 37)))

        self._draw_base_hud(surface, "PLAYER", gs.player_base.hp_ratio(), gs.player_base.hp, 760, Palette.PLAYER)
        self._draw_base_hud(surface, "AI", gs.ai_base.hp_ratio(), gs.ai_base.hp, 1015, Palette.AI)

    def _draw_base_hud(self, surface: pygame.Surface, label: str, ratio: float,
                       hp: float, x: int, color) -> None:
        draw_text(surface, label, (x, 22), self.fonts.small, color)
        draw_bar(surface, pygame.Rect(x + 68, 25, 145, 12), ratio, color)
        draw_text(surface, f"{hp:.0f}/500", (x + 68, 39), self.fonts.tiny, Palette.TEXT_MUTED)

    def _draw_battlefield(self, surface: pygame.Surface, gs: GameState,
                          lane_summaries: List[LaneSummary]) -> None:
        battle_rect = pygame.Rect(16, Layout.TOP_HUD_HEIGHT, SCREEN_WIDTH - 32,
                                  GAME_AREA_HEIGHT - Layout.TOP_HUD_HEIGHT - 10)
        pygame.draw.rect(surface, (10, 16, 27), battle_rect, border_radius=10)
        pygame.draw.rect(surface, Palette.LINE_SOFT, battle_rect, 1, border_radius=10)

        for lane in gs.lanes:
            summary = lane_summaries[lane.lane_id] if lane.lane_id < len(lane_summaries) else None
            self._draw_lane(surface, gs, lane.lane_id, summary)

        self._draw_bases(surface, gs)
        self._draw_towers(surface, gs)
        self._draw_units(surface, gs)

    def _draw_lane(self, surface: pygame.Surface, gs: GameState,
                   lane_id: int, summary: Optional[LaneSummary]) -> None:
        lane_y = LANE_Y_POSITIONS[lane_id]
        risk = summary.breakthrough_risk if summary else 0.0
        lane_fill = lerp_color((28, 35, 54), (72, 24, 31), risk)
        lane_rect = pygame.Rect(PLAYER_BASE_X, lane_y - 27, AI_BASE_X - PLAYER_BASE_X, 54)
        pygame.draw.rect(surface, lane_fill, lane_rect, border_radius=8)
        texture = pygame.transform.smoothscale(self.assets.lane_texture, lane_rect.size)
        texture.set_alpha(150)
        surface.blit(texture, lane_rect.topleft)
        pygame.draw.rect(surface, Palette.LINE_SOFT, lane_rect, 1, border_radius=8)
        pygame.draw.line(surface, (68, 82, 108), (PLAYER_BASE_X + 20, lane_y),
                         (AI_BASE_X - 20, lane_y), 1)
        for x in range(PLAYER_BASE_X + 60, AI_BASE_X - 30, 80):
            pygame.draw.line(surface, (47, 58, 79), (x, lane_y - 5), (x + 22, lane_y - 5), 1)
            pygame.draw.line(surface, (47, 58, 79), (x, lane_y + 5), (x + 22, lane_y + 5), 1)

        draw_text(surface, f"LANE {lane_id + 1}", (PLAYER_BASE_X + 10, lane_y - 22),
                  self.fonts.tiny, Palette.TEXT_MUTED)
        self._draw_danger_meter(surface, lane_y, risk)
        self._draw_build_slots(surface, gs, lane_id)

    def _draw_danger_meter(self, surface: pygame.Surface, lane_y: int, risk: float) -> None:
        x = AI_BASE_X - 108
        rect = pygame.Rect(x, lane_y + 17, 78, 7)
        draw_bar(surface, rect, risk, danger_color(risk), bg=(28, 32, 42), border=Palette.LINE_SOFT)
        draw_text(surface, "RISK", (x - 35, lane_y + 12), self.fonts.tiny, Palette.TEXT_DIM)

    def _draw_build_slots(self, surface: pygame.Surface, gs: GameState, lane_id: int) -> None:
        selected_lane = self.selected_lane == lane_id
        for owner in (Owner.PLAYER, Owner.AI):
            free_slots = set(gs.get_free_build_slots(owner, lane_id))
            for s in range(NUM_SLOTS_PER_SIDE):
                pos = self.map_manager.get_build_slot_pos(owner, lane_id, s)
                rect = pygame.Rect(pos[0] - 15, pos[1] - 15, 30, 30)
                free = s in free_slots
                base_col = (40, 57, 83) if owner == Owner.PLAYER else (65, 28, 35)
                col = base_col if free else (15, 18, 27)
                border = Palette.CYAN if selected_lane and owner == Owner.PLAYER and free else Palette.LINE_SOFT
                pygame.draw.rect(surface, col, rect, border_radius=6)
                pygame.draw.rect(surface, border, rect, 2 if selected_lane and free else 1, border_radius=6)
                if free:
                    plus = self.fonts.small.render("+", True, Palette.TEXT_MUTED)
                    surface.blit(plus, plus.get_rect(center=rect.center))

    def _draw_bases(self, surface: pygame.Surface, gs: GameState) -> None:
        self._draw_base(surface, gs.player_base.position[0], BASE_Y, "PLAYER", gs.player_base.hp_ratio(), Palette.PLAYER)
        self._draw_base(surface, gs.ai_base.position[0], BASE_Y, "AI CORE", gs.ai_base.hp_ratio(), Palette.AI)

    def _draw_base(self, surface: pygame.Surface, x: int, y: int, label: str,
                   hp_ratio: float, color) -> None:
        owner_key = "player" if color == Palette.PLAYER else "ai"
        sprite = self.assets.base_icon(owner_key)
        rect = sprite.get_rect(center=(x, y))
        shadow = pygame.Surface((rect.w + 18, rect.h + 18), pygame.SRCALPHA)
        pygame.draw.rect(shadow, (0, 0, 0, 90), shadow.get_rect(), border_radius=18)
        surface.blit(shadow, (rect.x - 9, rect.y - 6))
        surface.blit(sprite, rect)
        draw_text(surface, label, (x - 31, y - 44), self.fonts.small, color)
        draw_bar(surface, pygame.Rect(x - 32, y + 38, 64, 10), hp_ratio, color)

    def _draw_towers(self, surface: pygame.Surface, gs: GameState) -> None:
        hovered = self._hovered_tower(gs)
        for tower in gs.player_towers + gs.ai_towers:
            x, y = tower.position
            col = tower.get_color()
            selected = tower is hovered or self.show_ai_debug
            if selected:
                size = int(tower.range * 2) + 2
                ring = pygame.Surface((size, size), pygame.SRCALPHA)
                ring_col = (*Palette.PLAYER, 55) if tower.owner == Owner.PLAYER else (*Palette.AI, 55)
                pygame.draw.circle(ring, ring_col, (size // 2, size // 2), int(tower.range), 1)
                surface.blit(ring, (x - tower.range, y - tower.range))

            size = 24 + tower.level * 5
            rect = pygame.Rect(x - size // 2, y - size // 2, size, size)
            pygame.draw.circle(surface, (0, 0, 0, 95), (x + 2, y + 3), size // 2 + 4)
            icon = self.assets.tower_icon(tower.tower_type, size)
            surface.blit(icon, rect)
            pygame.draw.circle(surface, col, (x, y), size // 2 + 2, 1)
            label = self.fonts.tiny.render(f"L{tower.level}", True, Palette.TEXT)
            surface.blit(label, label.get_rect(center=(x, y - size // 2 - 9)))

            if tower.attack_cooldown > 0:
                ratio = 1.0 - (tower.attack_cooldown / tower.attack_interval)
                pygame.draw.arc(surface, Palette.RESOURCE, rect.inflate(10, 10),
                                -math.pi / 2, -math.pi / 2 + 2 * math.pi * ratio, 2)

    def _hovered_tower(self, gs: GameState):
        mx, my = self.mouse_pos
        for tower in gs.player_towers + gs.ai_towers:
            x, y = tower.position
            if abs(mx - x) <= 18 and abs(my - y) <= 18:
                return tower
        return None

    def _draw_units(self, surface: pygame.Surface, gs: GameState) -> None:
        for unit in gs.active_units:
            pos = self.map_manager.get_unit_position_pixels(unit.owner, unit.lane_id, unit.position)
            col = unit.get_color()
            r = unit.get_radius() + 2
            trail = pygame.Surface((28, 14), pygame.SRCALPHA)
            trail_col = (*Palette.PLAYER, 45) if unit.owner == Owner.PLAYER else (*Palette.AI, 45)
            pygame.draw.ellipse(trail, trail_col, trail.get_rect())
            offset = -14 if unit.owner == Owner.PLAYER else 0
            surface.blit(trail, (pos[0] + offset, pos[1] - 7))
            icon_size = max(18, r * 3)
            icon = self.assets.unit_icon(unit.unit_type, icon_size)
            if unit.owner == Owner.AI:
                icon = pygame.transform.flip(icon, True, False)
            icon_rect = icon.get_rect(center=pos)
            pygame.draw.circle(surface, (8, 10, 16), pos, max(r + 4, icon_size // 2))
            surface.blit(icon, icon_rect)
            pygame.draw.circle(surface, col, pos, max(r + 2, icon_size // 2), 1)
            draw_bar(surface, pygame.Rect(pos[0] - r - 3, pos[1] - r - 9, (r + 3) * 2, 4),
                     unit.hp_ratio(), Palette.GREEN, bg=(38, 42, 52))

    def _draw_command_deck(self, surface: pygame.Surface, gs: GameState) -> None:
        pygame.draw.rect(surface, (13, 18, 29), (0, GAME_AREA_HEIGHT, SCREEN_WIDTH, PANEL_HEIGHT))
        pygame.draw.line(surface, Palette.LINE, (0, GAME_AREA_HEIGHT), (SCREEN_WIDTH, GAME_AREA_HEIGHT), 2)

        draw_text(surface, "THÁP PHÒNG THỦ", (22, GAME_AREA_HEIGHT + 20), self.fonts.tiny, Palette.TEXT_MUTED)
        draw_text(surface, "ĐƠN VỊ TẤN CÔNG", (22, GAME_AREA_HEIGHT + 98), self.fonts.tiny, Palette.TEXT_MUTED)
        draw_text(surface, "LANE", (394, GAME_AREA_HEIGHT + 42), self.fonts.tiny, Palette.TEXT_MUTED)
        draw_text(surface, "HÀNH ĐỘNG", (622, GAME_AREA_HEIGHT + 20), self.fonts.tiny, Palette.TEXT_MUTED)

        for btn in self.all_buttons:
            btn.draw(surface, self.fonts.small, self.fonts.tiny)

        self._draw_resource_panel(surface, gs)
        self._draw_selection_summary(surface)
        self._draw_stats_panel(surface, gs)

    def _draw_resource_panel(self, surface: pygame.Surface, gs: GameState) -> None:
        rect = pygame.Rect(866, GAME_AREA_HEIGHT + 20, 190, 72)
        draw_panel(surface, rect, "Tài nguyên", self.fonts.tiny, fill=(16, 24, 38))
        draw_text(surface, f"Player: {gs.player_resource:.0f}", (882, GAME_AREA_HEIGHT + 50),
                  self.fonts.large, Palette.RESOURCE)
        draw_text(surface, f"AI: {gs.ai_resource:.0f}", (882, GAME_AREA_HEIGHT + 78),
                  self.fonts.small, Palette.AI)

    def _draw_selection_summary(self, surface: pygame.Surface) -> None:
        rect = pygame.Rect(392, GAME_AREA_HEIGHT + 112, 462, 56)
        draw_panel(surface, rect, "Lệnh hiện tại", self.fonts.tiny, fill=(16, 24, 38))
        parts = []
        if self.selected_tower_type:
            parts.append(f"Tháp: {self._tower_label(self.selected_tower_type)}")
        if self.selected_unit_type:
            parts.append(f"Quân: {self._unit_label(self.selected_unit_type)}")
        if self.selected_lane is not None:
            parts.append(f"Lane: {self.selected_lane + 1}")
        text = " | ".join(parts) if parts else "Chọn tháp/quân và lane để ra lệnh."
        draw_text(surface, text, (408, GAME_AREA_HEIGHT + 140), self.fonts.small,
                  Palette.CYAN if parts else Palette.TEXT_MUTED)

    def _draw_stats_panel(self, surface: pygame.Surface, gs: GameState) -> None:
        rect = pygame.Rect(1068, GAME_AREA_HEIGHT + 78, 194, 90)
        draw_panel(surface, rect, "Trận đấu", self.fonts.tiny, fill=(16, 24, 38))
        draw_text(surface, f"P: Kill {gs.player_kills}  Atk {gs.player_attack_count}  Def {gs.player_defense_count}",
                  (1082, GAME_AREA_HEIGHT + 106), self.fonts.tiny, Palette.PLAYER)
        draw_text(surface, f"AI: Kill {gs.ai_kills}  Atk {gs.ai_attack_count}  Def {gs.ai_defense_count}",
                  (1082, GAME_AREA_HEIGHT + 125), self.fonts.tiny, Palette.AI)
        draw_text(surface, "[P] Pause   [D] Debug   [ESC] Thoát",
                  (1082, GAME_AREA_HEIGHT + 146), self.fonts.tiny, Palette.TEXT_DIM)

    def _draw_status(self, surface: pygame.Surface) -> None:
        if self.status_timer <= 0:
            return
        rect = pygame.Rect(SCREEN_WIDTH // 2 - 230, GAME_AREA_HEIGHT - 42, 460, 30)
        pygame.draw.rect(surface, (12, 18, 30), rect, border_radius=8)
        pygame.draw.rect(surface, Palette.CYAN, rect, 1, border_radius=8)
        txt = self.fonts.small.render(self.status_msg, True, Palette.TEXT)
        surface.blit(txt, txt.get_rect(center=rect.center))

    def _draw_ai_debug(self, surface: pygame.Surface, gs: GameState,
                       lane_summaries: List[LaneSummary]) -> None:
        rect = pygame.Rect(SCREEN_WIDTH // 2 - 260, 82, 520, 190)
        overlay = pygame.Surface(rect.size, pygame.SRCALPHA)
        overlay.fill((8, 12, 24, 232))
        surface.blit(overlay, rect.topleft)
        pygame.draw.rect(surface, Palette.CYAN, rect, 1, border_radius=8)
        draw_text(surface, "AI TACTICAL DEBUG", (rect.x + 16, rect.y + 12), self.fonts.medium, Palette.CYAN)

        action = getattr(self.engine, "last_ai_action", None)
        score = getattr(self.engine, "last_ai_score", 0.0)
        ms = getattr(self.engine, "last_ai_decision_ms", 0.0)
        desc = action.get_description() if action else "No decision yet"
        draw_text(surface, f"Last: {desc}", (rect.x + 16, rect.y + 42), self.fonts.small, Palette.TEXT)
        draw_text(surface, f"Score: {score:.2f}   Decision: {ms:.2f} ms", (rect.x + 16, rect.y + 62),
                  self.fonts.small, Palette.TEXT_MUTED)

        y = rect.y + 94
        for summary in lane_summaries:
            row_y = y + summary.lane_id * 28
            draw_text(surface, f"L{summary.lane_id + 1}", (rect.x + 18, row_y), self.fonts.small, Palette.TEXT)
            draw_bar(surface, pygame.Rect(rect.x + 55, row_y + 3, 120, 8),
                     summary.breakthrough_risk, danger_color(summary.breakthrough_risk))
            draw_text(surface, f"risk {summary.breakthrough_risk:.2f}", (rect.x + 184, row_y - 2),
                      self.fonts.tiny, Palette.TEXT_MUTED)
            draw_bar(surface, pygame.Rect(rect.x + 285, row_y + 3, 120, 8),
                     summary.attack_opportunity, Palette.CYAN)
            draw_text(surface, f"opp {summary.attack_opportunity:.2f}", (rect.x + 414, row_y - 2),
                      self.fonts.tiny, Palette.TEXT_MUTED)

    def _draw_game_over(self, surface: pygame.Surface, gs: GameState) -> None:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 176))
        surface.blit(overlay, (0, 0))
        winner = gs.get_winner()
        if winner == "PLAYER":
            msg, col = "NGƯỜI CHƠI THẮNG", Palette.PLAYER
        elif winner == "AI":
            msg, col = "AI THẮNG", Palette.AI
        else:
            msg, col = "HÒA", Palette.RESOURCE

        rect = pygame.Rect(SCREEN_WIDTH // 2 - 260, SCREEN_HEIGHT // 2 - 95, 520, 190)
        draw_panel(surface, rect, None, self.fonts.small, fill=(12, 18, 30), border=col)
        title = self.fonts.title.render(msg, True, col)
        surface.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, rect.y + 48)))
        draw_text(surface, f"Player HP: {gs.player_base.hp:.0f}   |   AI HP: {gs.ai_base.hp:.0f}",
                  (rect.x + 122, rect.y + 86), self.fonts.medium, Palette.TEXT)
        draw_text(surface, f"Thời gian: {gs.match_time:.0f}s   |   Xem log trong thư mục logs/",
                  (rect.x + 96, rect.y + 118), self.fonts.small, Palette.TEXT_MUTED)
        draw_text(surface, "Nhấn ESC để thoát", (rect.x + 202, rect.y + 148), self.fonts.small, Palette.TEXT_DIM)

    def _draw_hp_bar(self, surface: pygame.Surface, x: int, y: int, w: int, h: int,
                     ratio: float, color) -> None:
        draw_bar(surface, pygame.Rect(x, y, w, h), ratio, color)

    def _tower_label(self, tt: TowerType) -> str:
        return {
            TowerType.FAST: "Nhanh",
            TowerType.HEAVY: "Nặng",
            TowerType.BALANCED: "Cân bằng",
        }[tt]

    def _unit_label(self, ut: UnitType) -> str:
        return {
            UnitType.FAST: "Nhanh",
            UnitType.TANK: "Trâu",
            UnitType.SWARM: "Rẻ",
        }[ut]
