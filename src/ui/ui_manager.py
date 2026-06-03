"""Pygame tactical interface for the tower-defense AI demo."""
from __future__ import annotations

import math
from typing import List, Optional, Tuple

import pygame

from src.models import (
    Action,
    ActionType,
    GameState,
    LaneSummary,
    Owner,
    TOWER_CONFIGS,
    UNIT_CONFIGS,
    Tower,
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
from src.ui.effects import EffectManager, draw_event_feed
from src.ui.theme import (
    FontSize,
    Fonts,
    Layout,
    Palette,
    danger_color,
    hp_color,
    lerp_color,
)
from src.ui.widgets import Button, draw_bar, draw_panel, draw_text


class UIManager:
    def __init__(self, game_engine, map_manager: MapManager):
        self.engine = game_engine
        self.map_manager = map_manager

        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Phòng Thủ Chiến Thuật AI")
        self.assets = AssetManager()
        self.effects = EffectManager()

        self.fonts = Fonts(
            title=pygame.font.SysFont("Segoe UI", FontSize.TITLE, bold=True),
            large=pygame.font.SysFont("Segoe UI", FontSize.LARGE, bold=True),
            medium=pygame.font.SysFont("Segoe UI", FontSize.MEDIUM),
            small=pygame.font.SysFont("Segoe UI", FontSize.SMALL),
            tiny=pygame.font.SysFont("Segoe UI", FontSize.TINY),
        )

        self.left_rect = pygame.Rect(Layout.SCREEN_PAD, 78, Layout.LEFT_PANEL_WIDTH, 504)
        self.right_rect = pygame.Rect(
            SCREEN_WIDTH - Layout.RIGHT_PANEL_WIDTH - Layout.SCREEN_PAD,
            78,
            Layout.RIGHT_PANEL_WIDTH,
            504,
        )
        self.battle_rect = pygame.Rect(
            self.left_rect.right + Layout.SCREEN_PAD,
            78,
            self.right_rect.left - self.left_rect.right - Layout.SCREEN_PAD * 2,
            504,
        )
        self.log_rect = pygame.Rect(
            Layout.SCREEN_PAD,
            SCREEN_HEIGHT - Layout.BOTTOM_LOG_HEIGHT - Layout.SCREEN_PAD,
            SCREEN_WIDTH - Layout.SCREEN_PAD * 2,
            Layout.BOTTOM_LOG_HEIGHT,
        )

        self.selected_tower_type: Optional[TowerType] = None
        self.selected_unit_type: Optional[UnitType] = None
        self.selected_lane: Optional[int] = None
        self.status_msg = ""
        self.status_timer = 0.0
        self.show_ai_debug = False
        self.mouse_pos = (0, 0)
        self.current_lane_summaries: List[LaneSummary] = []

        self._build_buttons()
        self._attach_button_icons()

    def _build_buttons(self) -> None:
        x = self.left_rect.x + 14
        w = 98
        h = 40
        gap = 8
        y = self.left_rect.y + 158

        self.btn_tower_fast = Button(
            pygame.Rect(x, y, w, h), "Nhanh", Palette.SURFACE_2, Palette.SURFACE_3,
            lambda: self._select_tower_type(TowerType.FAST),
            sublabel=f"{TOWER_CONFIGS[TowerType.FAST][1]['cost']}g",
            tooltip="Tháp nhanh. Sát thương thấp, tốc độ bắn cao.",
        )
        self.btn_tower_heavy = Button(
            pygame.Rect(x + w + gap, y, w, h), "Nặng", Palette.SURFACE_2, Palette.SURFACE_3,
            lambda: self._select_tower_type(TowerType.HEAVY),
            sublabel=f"{TOWER_CONFIGS[TowerType.HEAVY][1]['cost']}g",
            tooltip="Tháp nặng. Sát thương lớn, tốc độ bắn chậm.",
        )
        self.btn_tower_balanced = Button(
            pygame.Rect(x, y + h + gap, w * 2 + gap, h), "Tháp Cân Bằng",
            Palette.SURFACE_2, Palette.SURFACE_3, lambda: self._select_tower_type(TowerType.BALANCED),
            sublabel=f"{TOWER_CONFIGS[TowerType.BALANCED][1]['cost']}g",
            tooltip="Tháp cân bằng. Tầm bắn và sát thương ổn định.",
        )

        unit_y = y + 106
        self.btn_unit_fast = Button(
            pygame.Rect(x, unit_y, w, h), "Nhanh", Palette.SURFACE_2, Palette.SURFACE_3,
            lambda: self._select_unit_type(UnitType.FAST),
            sublabel=f"{UNIT_CONFIGS[UnitType.FAST]['cost']}g",
            tooltip="Quân nhanh. Áp sát căn cứ rất nhanh.",
        )
        self.btn_unit_tank = Button(
            pygame.Rect(x + w + gap, unit_y, w, h), "Trâu", Palette.SURFACE_2, Palette.SURFACE_3,
            lambda: self._select_unit_type(UnitType.TANK),
            sublabel=f"{UNIT_CONFIGS[UnitType.TANK]['cost']}g",
            tooltip="Quân trâu. Di chuyển chậm nhưng rất bền.",
        )
        self.btn_unit_swarm = Button(
            pygame.Rect(x, unit_y + h + gap, w * 2 + gap, h), "Quân Rẻ",
            Palette.SURFACE_2, Palette.SURFACE_3, lambda: self._select_unit_type(UnitType.SWARM),
            sublabel=f"{UNIT_CONFIGS[UnitType.SWARM]['cost']}g",
            tooltip="Quân rẻ. Dùng để tạo áp lực liên tục.",
        )

        lane_y = unit_y + 106
        self.btn_lanes: List[Button] = []
        for i in range(3):
            self.btn_lanes.append(Button(
                pygame.Rect(x + i * 70, lane_y, 62, h),
                f"L{i + 1}", Palette.SURFACE_3, (69, 85, 108),
                lambda lid=i: self._select_lane(lid),
            tooltip=f"Chọn tuyến {i + 1}.",
            ))

        action_y = lane_y + 56
        self.btn_build = Button(
            pygame.Rect(x, action_y, w, h), "Xây", Palette.PRIMARY_DARK, (14, 116, 144),
            self._action_build_tower,
            tooltip="Xây tháp đã chọn trên tuyến đã chọn.",
        )
        self.btn_send = Button(
            pygame.Rect(x + w + gap, action_y, w, h), "Gửi", (20, 83, 55), (27, 120, 77),
            self._action_send_unit,
            tooltip="Gửi quân đã chọn vào tuyến đã chọn.",
        )
        self.btn_upgrade = Button(
            pygame.Rect(x, action_y + h + gap, w * 2 + gap, h), "Nâng Cấp Tuyến",
            Palette.SURFACE_2, Palette.SURFACE_3, self._action_upgrade,
            tooltip="Nâng cấp tháp hợp lệ đầu tiên trên tuyến đã chọn.",
        )
        self.btn_debug = Button(
            pygame.Rect(self.right_rect.x + 14, self.right_rect.bottom - 54, self.right_rect.w - 28, 38),
            "Gỡ Lỗi AI", Palette.SURFACE_3, (69, 85, 108), self._toggle_debug,
            tooltip="Bật/tắt bảng phân tích chiến thuật AI mở rộng.",
        )

        self.all_buttons = [
            self.btn_tower_fast, self.btn_tower_heavy, self.btn_tower_balanced,
            self.btn_unit_fast, self.btn_unit_tank, self.btn_unit_swarm,
            *self.btn_lanes, self.btn_build, self.btn_send, self.btn_upgrade,
            self.btn_debug,
        ]

    def _attach_button_icons(self) -> None:
        self.btn_tower_fast.icon = self.assets.tower_icon(TowerType.FAST, 22)
        self.btn_tower_heavy.icon = self.assets.tower_icon(TowerType.HEAVY, 22)
        self.btn_tower_balanced.icon = self.assets.tower_icon(TowerType.BALANCED, 22)
        self.btn_unit_fast.icon = self.assets.unit_icon(UnitType.FAST, 21)
        self.btn_unit_tank.icon = self.assets.unit_icon(UnitType.TANK, 21)
        self.btn_unit_swarm.icon = self.assets.unit_icon(UnitType.SWARM, 21)

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
        self.set_status(f"Đã chọn tuyến {lane_id + 1}")

    def _action_send_unit(self) -> None:
        if self.selected_unit_type is None:
            self.set_status("Hãy chọn loại quân trước.")
            return
        if self.selected_lane is None:
            self.set_status("Hãy chọn tuyến trước.")
            return
        gs = self.engine.get_state()
        if gs is None:
            return
        cost = UNIT_CONFIGS[self.selected_unit_type]["cost"]
        action = Action(ActionType.SEND_UNIT, Owner.PLAYER, self.selected_lane,
                        self.selected_unit_type, cost=cost)
        if self.engine.execute_action(action, Owner.PLAYER):
            self.set_status(f"Đã gửi quân {self._unit_label(self.selected_unit_type)} vào tuyến {self.selected_lane + 1}")
        else:
            self.set_status("Không đủ vàng để gửi quân.")

    def _action_build_tower(self) -> None:
        if self.selected_tower_type is None:
            self.set_status("Hãy chọn loại tháp trước.")
            return
        if self.selected_lane is None:
            self.set_status("Hãy chọn tuyến trước.")
            return
        gs = self.engine.get_state()
        if gs is None:
            return
        free_slots = gs.get_free_build_slots(Owner.PLAYER, self.selected_lane)
        if not free_slots:
            self.set_status("Tuyến này đã hết ô xây tháp.")
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
            self.set_status(f"Đã xây tháp {self._tower_label(self.selected_tower_type)}")
        else:
            self.set_status("Không đủ vàng hoặc ô xây không hợp lệ.")

    def _action_upgrade(self) -> None:
        if self.selected_lane is None:
            self.set_status("Hãy chọn tuyến trước.")
            return
        gs = self.engine.get_state()
        if gs is None:
            return
        towers = gs.get_towers_by_lane(Owner.PLAYER, self.selected_lane)
        upgradable = [t for t in towers if t.can_upgrade() and gs.player_resource >= t.get_upgrade_cost()]
        if not upgradable:
            self.set_status("Không có tháp đủ điều kiện nâng cấp trên tuyến này.")
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
            self.set_status(f"Tháp #{tower.tower_id} đã lên cấp {tower.level}")
        else:
            self.set_status("Không đủ vàng để nâng cấp.")

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

        lane = self._hovered_lane()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and lane is not None:
            self._select_lane(lane)

        for btn in self.all_buttons:
            btn.handle_event(event)
        return True

    def update(self, dt: float) -> None:
        if self.status_timer > 0:
            self.status_timer = max(0.0, self.status_timer - dt)
        events = self.engine.drain_ui_events() if hasattr(self.engine, "drain_ui_events") else []
        self.effects.consume_events([self._event_to_view(e) for e in events])
        self.effects.update(dt)

    def render(self, game_state: Optional[GameState], lane_summaries: List[LaneSummary]) -> None:
        surface = self.screen
        self.current_lane_summaries = lane_summaries
        self._draw_background(surface)
        if game_state is None:
            self._draw_start_screen(surface)
            pygame.display.flip()
            return

        self._sync_button_state(game_state)
        self._draw_top_bar(surface, game_state)
        self._draw_left_panel(surface, game_state)
        self._draw_battlefield(surface, game_state, lane_summaries)
        self._draw_right_panel(surface, game_state, lane_summaries)
        self._draw_event_log(surface)
        self._draw_status(surface)
        self._draw_tooltip(surface)

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
            cost = TOWER_CONFIGS[tt][1]["cost"]
            btn.selected = self.selected_tower_type == tt
            btn.enabled = gs.player_resource >= cost
            btn.disabled_reason = f"Cần {cost} vàng"
        for ut, btn in unit_buttons.items():
            cost = UNIT_CONFIGS[ut]["cost"]
            btn.selected = self.selected_unit_type == ut
            btn.enabled = gs.player_resource >= cost
            btn.disabled_reason = f"Cần {cost} vàng"
        for i, btn in enumerate(self.btn_lanes):
            btn.selected = self.selected_lane == i
        self.btn_build.enabled = self.selected_tower_type is not None and self.selected_lane is not None
        self.btn_send.enabled = self.selected_unit_type is not None and self.selected_lane is not None
        self.btn_upgrade.enabled = self.selected_lane is not None
        self.btn_debug.selected = self.show_ai_debug

    def _draw_background(self, surface: pygame.Surface) -> None:
        surface.fill(Palette.BG_DEEP)
        bg = pygame.transform.smoothscale(self.assets.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        bg.set_alpha(190)
        surface.blit(bg, (0, 0))
        for x in range(0, SCREEN_WIDTH, 40):
            pygame.draw.line(surface, Palette.BG_GRID, (x, 0), (x, SCREEN_HEIGHT), 1)
        for y in range(0, SCREEN_HEIGHT, 40):
            pygame.draw.line(surface, Palette.BG_GRID, (0, y), (SCREEN_WIDTH, y), 1)

    def _draw_start_screen(self, surface: pygame.Surface) -> None:
        draw_text(surface, "PHÒNG THỦ CHIẾN THUẬT AI", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 18),
                  self.fonts.title, Palette.TEXT, align="center")
        draw_text(surface, "Đang khởi tạo trận đấu...", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 18),
                  self.fonts.medium, Palette.TEXT_MUTED, align="center")

    def _draw_top_bar(self, surface: pygame.Surface, gs: GameState) -> None:
        rect = pygame.Rect(Layout.SCREEN_PAD, 14, SCREEN_WIDTH - Layout.SCREEN_PAD * 2, 50)
        draw_panel(surface, rect, None, self.fonts.tiny, fill=(13, 23, 41), border=Palette.LINE)
        draw_text(surface, "PHÒNG THỦ CHIẾN THUẬT AI", (rect.x + 18, rect.y + 12), self.fonts.large, Palette.TEXT)
        timer = f"{int(gs.match_time // 60):02d}:{int(gs.match_time % 60):02d}"
        max_timer = f"{int(gs.max_match_time // 60):02d}:00"
        chip_x = rect.x + 430
        chip_y = rect.y + 9
        self._draw_chip(surface, pygame.Rect(chip_x, chip_y, 132, 32), "Vàng", f"{gs.player_resource:.0f}", Palette.RESOURCE)
        self._draw_chip(surface, pygame.Rect(chip_x + 144, chip_y, 144, 32), "Thời gian", f"{timer}/{max_timer}", Palette.PRIMARY)
        self._draw_chip(surface, pygame.Rect(chip_x + 300, chip_y, 112, 32), "Vàng AI", f"{gs.ai_resource:.0f}", Palette.AI)
        self._draw_chip(surface, pygame.Rect(rect.right - 252, chip_y, 224, 32), "AI", self._ai_label(), Palette.PRIMARY)

    def _draw_chip(self, surface: pygame.Surface, rect: pygame.Rect,
                   label: str, value: str, color) -> None:
        pygame.draw.rect(surface, (11, 22, 38), rect, border_radius=8)
        pygame.draw.rect(surface, Palette.LINE_SOFT, rect, 1, border_radius=8)
        pygame.draw.circle(surface, color, (rect.x + 13, rect.centery), 4)
        draw_text(surface, label.upper(), (rect.x + 24, rect.y + 4), self.fonts.tiny, Palette.TEXT_DIM)
        draw_text(surface, value, (rect.x + 24, rect.y + 15), self.fonts.small, color)

    def _draw_metric(self, surface: pygame.Surface, rect: pygame.Rect,
                     label: str, value: str, color) -> None:
        pygame.draw.rect(surface, (12, 23, 39), rect, border_radius=8)
        pygame.draw.rect(surface, Palette.LINE_SOFT, rect, 1, border_radius=8)
        draw_text(surface, label.upper(), (rect.x + 9, rect.y + 5), self.fonts.tiny, Palette.TEXT_MUTED)
        draw_text(surface, value, (rect.x + 9, rect.y + 19), self.fonts.large, color)

    def _draw_left_panel(self, surface: pygame.Surface, gs: GameState) -> None:
        draw_panel(surface, self.left_rect, "Lệnh Người Chơi", self.fonts.tiny, fill=Palette.SURFACE)
        hp_rect = pygame.Rect(self.left_rect.x + 14, self.left_rect.y + 46, self.left_rect.w - 28, 14)
        draw_text(surface, "MÁU CĂN CỨ", (hp_rect.x, hp_rect.y - 18), self.fonts.tiny, Palette.TEXT_MUTED)
        draw_bar(surface, hp_rect, gs.player_base.hp_ratio(), hp_color(gs.player_base.hp_ratio()),
                 label=f"{gs.player_base.hp:.0f}/500", font=self.fonts.tiny)
        self._draw_metric(surface, pygame.Rect(self.left_rect.x + 14, self.left_rect.y + 74, 96, 44),
                          "Vàng", f"{gs.player_resource:.0f}", Palette.RESOURCE)
        self._draw_metric(surface, pygame.Rect(self.left_rect.x + 120, self.left_rect.y + 74, 102, 44),
                          "Hạ", f"{gs.player_kills}", Palette.GREEN)
        draw_text(surface, f"Tấn công {gs.player_attack_count}  |  Phòng thủ {gs.player_defense_count}",
                  (self.left_rect.x + 14, self.left_rect.y + 124), self.fonts.tiny, Palette.TEXT_MUTED)
        draw_text(surface, "THÁP", (self.left_rect.x + 14, self.left_rect.y + 140),
                  self.fonts.tiny, Palette.TEXT_MUTED)
        draw_text(surface, "QUÂN", (self.left_rect.x + 14, self.left_rect.y + 244),
                  self.fonts.tiny, Palette.TEXT_MUTED)
        draw_text(surface, "TUYẾN", (self.left_rect.x + 14, self.left_rect.y + 350),
                  self.fonts.tiny, Palette.TEXT_MUTED)
        draw_text(surface, "HÀNH ĐỘNG", (self.left_rect.x + 14, self.left_rect.y + 438),
                  self.fonts.tiny, Palette.TEXT_MUTED)
        for btn in self.all_buttons:
            if btn is not self.btn_debug:
                btn.draw(surface, self.fonts.small, self.fonts.tiny)

    def _draw_battlefield(self, surface: pygame.Surface, gs: GameState,
                          lane_summaries: List[LaneSummary]) -> None:
        draw_panel(surface, self.battle_rect, "Chiến Trường", self.fonts.tiny,
                   fill=(11, 18, 33), border=Palette.LINE)
        inner = self.battle_rect.inflate(-18, -48)
        inner.y += 28
        pygame.draw.rect(surface, (9, 15, 28), inner, border_radius=8)
        pygame.draw.rect(surface, Palette.LINE_SOFT, inner, 1, border_radius=8)

        for lane in gs.lanes:
            summary = lane_summaries[lane.lane_id] if lane.lane_id < len(lane_summaries) else None
            self._draw_lane(surface, gs, lane.lane_id, summary)

        self._draw_bases(surface, gs)
        self._draw_towers(surface, gs)
        self._draw_units(surface, gs)
        self.effects.draw_battle_effects(surface, self.fonts.small)

    def _draw_lane(self, surface: pygame.Surface, gs: GameState,
                   lane_id: int, summary: Optional[LaneSummary]) -> None:
        lane_y = LANE_Y_POSITIONS[lane_id]
        risk = self._lane_risk(gs, lane_id, summary)
        lane_rect = pygame.Rect(self.battle_rect.x + 16, lane_y - 30, self.battle_rect.w - 32, 60)
        fill = lerp_color((18, 29, 49), (81, 31, 39), risk)
        hovered = self._hovered_lane() == lane_id
        selected = self.selected_lane == lane_id
        if hovered or selected:
            fill = lerp_color(fill, Palette.PRIMARY_DARK, 0.28)
        pygame.draw.rect(surface, fill, lane_rect, border_radius=8)
        texture = pygame.transform.smoothscale(self.assets.lane_texture, lane_rect.size)
        texture.set_alpha(78)
        surface.blit(texture, lane_rect.topleft)
        for sy in range(lane_rect.y + 12, lane_rect.bottom - 8, 12):
            pygame.draw.line(surface, (31, 45, 65), (lane_rect.x + 12, sy), (lane_rect.right - 12, sy), 1)
        for cx in range(lane_rect.x + 96, lane_rect.right - 88, 108):
            col = Palette.PLAYER if cx < lane_rect.centerx else Palette.AI
            alpha_line = pygame.Surface((30, 16), pygame.SRCALPHA)
            points = [(4, 4), (16, 8), (4, 12)] if cx < lane_rect.centerx else [(26, 4), (14, 8), (26, 12)]
            pygame.draw.lines(alpha_line, (*col, 55), False, points, 2)
            surface.blit(alpha_line, (cx, lane_rect.centery - 8))
        border = Palette.PRIMARY if selected else Palette.LINE_SOFT
        pygame.draw.rect(surface, border, lane_rect, 2 if selected else 1, border_radius=8)

        start = self._to_view_pos((PLAYER_BASE_X + 38, lane_y))
        end = self._to_view_pos((AI_BASE_X - 38, lane_y))
        pygame.draw.line(surface, (84, 104, 135), start, end, 1)
        for x in range(int(start[0]) + 32, int(end[0]) - 20, 58):
            pygame.draw.line(surface, (55, 71, 98), (x, lane_y - 6), (x + 22, lane_y - 6), 1)
            pygame.draw.line(surface, (55, 71, 98), (x, lane_y + 6), (x + 22, lane_y + 6), 1)

        draw_text(surface, f"TUYẾN {lane_id + 1}", (lane_rect.x + 10, lane_rect.y + 8),
                  self.fonts.tiny, Palette.TEXT_MUTED)
        risk_label, risk_col = self._risk_label(risk)
        draw_text(surface, risk_label, (lane_rect.right - 18, lane_rect.y + 8),
                  self.fonts.tiny, risk_col, align="right")
        self._draw_danger_meter(surface, lane_rect, risk)
        self._draw_build_slots(surface, gs, lane_id)

    def _draw_danger_meter(self, surface: pygame.Surface, lane_rect: pygame.Rect, risk: float) -> None:
        rect = pygame.Rect(lane_rect.right - 102, lane_rect.y + 42, 84, 7)
        draw_bar(surface, rect, risk, danger_color(risk), bg=(20, 28, 43), border=Palette.LINE_SOFT)
        draw_text(surface, "NGUY", (rect.x - 34, rect.y - 4), self.fonts.tiny, Palette.TEXT_DIM)

    def _draw_build_slots(self, surface: pygame.Surface, gs: GameState, lane_id: int) -> None:
        selected_lane = self.selected_lane == lane_id
        can_build = self.selected_tower_type is not None and (
            gs.player_resource >= TOWER_CONFIGS[self.selected_tower_type][1]["cost"]
        )
        for owner in (Owner.PLAYER, Owner.AI):
            free_slots = set(gs.get_free_build_slots(owner, lane_id))
            for s in range(NUM_SLOTS_PER_SIDE):
                pos = self._to_view_pos(self.map_manager.get_build_slot_pos(owner, lane_id, s))
                rect = pygame.Rect(int(pos[0]) - 13, int(pos[1]) - 13, 26, 26)
                free = s in free_slots
                hover = rect.collidepoint(self.mouse_pos)
                team_col = Palette.PLAYER if owner == Owner.PLAYER else Palette.AI
                if free:
                    fill = (11, 20, 34) if can_build or owner == Owner.AI else (8, 13, 23)
                    border = Palette.PRIMARY if selected_lane and owner == Owner.PLAYER and can_build else Palette.LINE_SOFT
                    if hover and owner == Owner.PLAYER:
                        border = Palette.PRIMARY
                    pygame.draw.rect(surface, fill, rect, border_radius=6)
                    self._draw_corner_box(surface, rect, border, 2 if selected_lane and owner == Owner.PLAYER else 1)
                    draw_text(surface, "+", rect.center, self.fonts.tiny,
                              team_col if can_build or owner == Owner.AI else Palette.TEXT_DIM, align="center")
                else:
                    pygame.draw.rect(surface, (8, 12, 20), rect, border_radius=6)
                    pygame.draw.rect(surface, (24, 33, 48), rect, 1, border_radius=6)

    def _draw_bases(self, surface: pygame.Surface, gs: GameState) -> None:
        self._draw_base(surface, self._to_view_pos((PLAYER_BASE_X, BASE_Y)), "NGƯỜI CHƠI",
                        gs.player_base.hp_ratio(), gs.player_base.hp, Palette.PLAYER)
        self._draw_base(surface, self._to_view_pos((AI_BASE_X, BASE_Y)), "LÕI AI",
                        gs.ai_base.hp_ratio(), gs.ai_base.hp, Palette.AI)

    def _draw_base(self, surface: pygame.Surface, pos: Tuple[float, float], label: str,
                   hp_ratio: float, hp: float, color) -> None:
        owner_key = "player" if color == Palette.PLAYER else "ai"
        sprite = self.assets.base_icon(owner_key, (72, 102))
        rect = sprite.get_rect(center=(int(pos[0]), int(pos[1])))
        pygame.draw.rect(surface, (0, 0, 0), rect.inflate(12, 12).move(0, 5), border_radius=14)
        if hp_ratio < 0.30:
            warning = pygame.Surface((rect.w + 34, rect.h + 34), pygame.SRCALPHA)
            pygame.draw.rect(warning, (*Palette.DANGER_HIGH, 50), warning.get_rect(), border_radius=18)
            surface.blit(warning, (rect.x - 17, rect.y - 17))
        surface.blit(sprite, rect)
        draw_text(surface, label, (int(pos[0]), int(pos[1]) - 66), self.fonts.tiny, color, align="center")
        draw_bar(surface, pygame.Rect(int(pos[0]) - 46, int(pos[1]) + 58, 92, 12),
                 hp_ratio, hp_color(hp_ratio), label=f"{hp:.0f}", font=self.fonts.tiny)

    def _draw_towers(self, surface: pygame.Surface, gs: GameState) -> None:
        hovered = self._hovered_tower(gs)
        for tower in gs.player_towers + gs.ai_towers:
            x, y = self._to_view_pos(tower.position)
            col = tower.get_color()
            selected = tower is hovered
            if selected:
                radius = max(34, int(tower.range * self._scale_x()))
                ring = pygame.Surface((radius * 2 + 4, radius * 2 + 4), pygame.SRCALPHA)
                ring_col = (*Palette.PLAYER, 58) if tower.owner == Owner.PLAYER else (*Palette.AI, 58)
                pygame.draw.circle(ring, ring_col, (radius + 2, radius + 2), radius, 1)
                surface.blit(ring, (x - radius - 2, y - radius - 2))

            size = 22 + tower.level * 4
            rect = pygame.Rect(int(x) - size // 2, int(y) - size // 2, size, size)
            pygame.draw.circle(surface, (0, 0, 0), (int(x) + 2, int(y) + 3), size // 2 + 4)
            icon = self.assets.tower_icon(tower.tower_type, size)
            surface.blit(icon, rect)
            pygame.draw.circle(surface, col, (int(x), int(y)), size // 2 + 2, 1)
            badge = pygame.Rect(int(x) - 12, int(y) - size // 2 - 20, 24, 14)
            pygame.draw.rect(surface, Palette.SURFACE_2, badge, border_radius=4)
            pygame.draw.rect(surface, Palette.LINE_SOFT, badge, 1, border_radius=4)
            draw_text(surface, f"C{tower.level}", badge.center, self.fonts.tiny, Palette.TEXT, align="center")

            if tower.attack_cooldown > 0:
                ratio = 1.0 - (tower.attack_cooldown / tower.attack_interval)
                pygame.draw.arc(surface, Palette.RESOURCE, rect.inflate(10, 10),
                                -math.pi / 2, -math.pi / 2 + 2 * math.pi * ratio, 2)

    def _draw_units(self, surface: pygame.Surface, gs: GameState) -> None:
        stack_counts = {}
        for unit in gs.active_units:
            raw_pos = self.map_manager.get_unit_position_pixels(unit.owner, unit.lane_id, unit.position)
            pos = self._to_view_pos(raw_pos)
            stack_key = (unit.owner, unit.lane_id, int(pos[0] // 28))
            stack_index = stack_counts.get(stack_key, 0)
            stack_counts[stack_key] = stack_index + 1
            pos = (
                pos[0] + ((stack_index % 2) * 2 - 1) * min(stack_index, 2) * 5,
                pos[1] + ((stack_index % 3) - 1) * 7,
            )
            col = unit.get_color()
            r = unit.get_radius() + 2
            trail = pygame.Surface((28, 14), pygame.SRCALPHA)
            trail_col = (*Palette.PLAYER, 45) if unit.owner == Owner.PLAYER else (*Palette.AI, 45)
            pygame.draw.ellipse(trail, trail_col, trail.get_rect())
            offset = -14 if unit.owner == Owner.PLAYER else 0
            surface.blit(trail, (pos[0] + offset, pos[1] - 7))
            icon_size = max(17, r * 3)
            icon = self.assets.unit_icon(unit.unit_type, icon_size)
            if unit.owner == Owner.AI:
                icon = pygame.transform.flip(icon, True, False)
            icon_rect = icon.get_rect(center=(int(pos[0]), int(pos[1])))
            pygame.draw.circle(surface, (8, 10, 16), (int(pos[0]), int(pos[1])), max(r + 4, icon_size // 2))
            surface.blit(icon, icon_rect)
            outline = Palette.PLAYER if unit.owner == Owner.PLAYER else Palette.AI
            pygame.draw.circle(surface, outline, (int(pos[0]), int(pos[1])), max(r + 2, icon_size // 2), 1)
            arrow = [(int(pos[0]) + 11, int(pos[1])), (int(pos[0]) + 5, int(pos[1]) - 4), (int(pos[0]) + 5, int(pos[1]) + 4)]
            if unit.owner == Owner.AI:
                arrow = [(int(pos[0]) - 11, int(pos[1])), (int(pos[0]) - 5, int(pos[1]) - 4), (int(pos[0]) - 5, int(pos[1]) + 4)]
            pygame.draw.polygon(surface, outline, arrow)
            draw_bar(surface, pygame.Rect(int(pos[0]) - r - 9, int(pos[1]) - r - 14, (r + 9) * 2, 5),
                     unit.hp_ratio(), hp_color(unit.hp_ratio()), bg=(12, 18, 28), border=Palette.LINE_SOFT)

    def _draw_right_panel(self, surface: pygame.Surface, gs: GameState,
                          lane_summaries: List[LaneSummary]) -> None:
        draw_panel(surface, self.right_rect, "Quyết Định AI", self.fonts.tiny, fill=Palette.SURFACE)
        action = getattr(self.engine, "last_ai_action", None)
        score = getattr(self.engine, "last_ai_score", 0.0)
        ms = getattr(self.engine, "last_ai_decision_ms", 0.0)
        desc = self._action_description(action) if action else "Đang chờ quyết định đầu tiên"
        draw_text(surface, "HỒ SƠ", (self.right_rect.x + 14, self.right_rect.y + 46),
                  self.fonts.tiny, Palette.TEXT_MUTED)
        profile_rect = pygame.Rect(self.right_rect.x + 14, self.right_rect.y + 64, self.right_rect.w - 28, 30)
        pygame.draw.rect(surface, (9, 30, 47), profile_rect, border_radius=8)
        pygame.draw.rect(surface, Palette.PRIMARY, profile_rect, 1, border_radius=8)
        draw_text(surface, self._ai_label(), profile_rect.center, self.fonts.small, Palette.PRIMARY, align="center")
        draw_text(surface, "HÀNH ĐỘNG GẦN NHẤT", (self.right_rect.x + 14, self.right_rect.y + 104),
                  self.fonts.tiny, Palette.TEXT_MUTED)
        action_rect = pygame.Rect(self.right_rect.x + 14, self.right_rect.y + 122, self.right_rect.w - 28, 58)
        pygame.draw.rect(surface, (12, 23, 39), action_rect, border_radius=8)
        pygame.draw.rect(surface, Palette.LINE_SOFT, action_rect, 1, border_radius=8)
        self._draw_wrapped(surface, desc, action_rect.x + 10, action_rect.y + 9,
                           action_rect.w - 20, self.fonts.tiny, Palette.TEXT)
        self._draw_metric(surface, pygame.Rect(self.right_rect.x + 14, self.right_rect.y + 190, 96, 44),
                          "Điểm", f"{score:.2f}", Palette.RESOURCE)
        self._draw_metric(surface, pygame.Rect(self.right_rect.x + 120, self.right_rect.y + 190, 102, 44),
                          "Thời gian", f"{ms:.2f}ms", Palette.PRIMARY)

        y = self.right_rect.y + 252
        draw_text(surface, "PHÂN TÍCH TUYẾN", (self.right_rect.x + 14, y), self.fonts.tiny, Palette.TEXT_MUTED)
        if not lane_summaries:
            draw_text(surface, "AI này không có dữ liệu heuristic.", (self.right_rect.x + 14, y + 24),
                      self.fonts.tiny, Palette.TEXT_DIM)
        for summary in lane_summaries[:3]:
            row_y = y + 26 + summary.lane_id * 50
            row_rect = pygame.Rect(self.right_rect.x + 14, row_y - 7, self.right_rect.w - 28, 42)
            pygame.draw.rect(surface, (12, 23, 39), row_rect, border_radius=7)
            draw_text(surface, f"T{summary.lane_id + 1}", (self.right_rect.x + 14, row_y),
                      self.fonts.small, Palette.TEXT)
            draw_bar(surface, pygame.Rect(self.right_rect.x + 44, row_y + 4, 78, 7),
                     summary.breakthrough_risk, danger_color(summary.breakthrough_risk))
            draw_text(surface, f"nguy {summary.breakthrough_risk * 100:.0f}%",
                      (self.right_rect.x + 132, row_y - 2), self.fonts.tiny, Palette.TEXT_MUTED)
            draw_bar(surface, pygame.Rect(self.right_rect.x + 44, row_y + 24, 78, 7),
                     summary.attack_opportunity, Palette.PRIMARY)
            draw_text(surface, f"cơ hội {summary.attack_opportunity * 100:.0f}%",
                      (self.right_rect.x + 132, row_y + 18), self.fonts.tiny, Palette.TEXT_MUTED)
        self.btn_debug.draw(surface, self.fonts.small, self.fonts.tiny)

    def _draw_event_log(self, surface: pygame.Surface) -> None:
        draw_panel(surface, self.log_rect, "Nhật Ký Sự Kiện", self.fonts.tiny, fill=Palette.SURFACE)
        draw_event_feed(surface, self.log_rect, self.effects.feed, self.fonts.small, self.fonts.tiny)

    def _draw_status(self, surface: pygame.Surface) -> None:
        if self.status_timer <= 0:
            return
        rect = pygame.Rect(SCREEN_WIDTH // 2 - 210, self.log_rect.y - 42, 420, 30)
        pygame.draw.rect(surface, (11, 18, 33), rect, border_radius=8)
        pygame.draw.rect(surface, Palette.PRIMARY, rect, 1, border_radius=8)
        draw_text(surface, self.status_msg, rect.center, self.fonts.small, Palette.TEXT, align="center")

    def _draw_tooltip(self, surface: pygame.Surface) -> None:
        hovered = next((btn for btn in self.all_buttons if btn.hovered), None)
        tower = self._hovered_tower(self.engine.get_state()) if self.engine.get_state() else None
        lane = self._hovered_lane()
        text = ""
        if hovered:
            text = hovered.tooltip if hovered.enabled else (hovered.disabled_reason or hovered.tooltip)
        elif tower:
            text = f"{self._owner_label(tower.owner)} | Tháp {self._tower_label(tower.tower_type)} | Cấp {tower.level} | Sát thương {tower.damage:.0f} | Tầm {tower.range:.0f}"
        elif lane is not None:
            summary = self.current_lane_summaries[lane] if lane < len(self.current_lane_summaries) else None
            risk = summary.breakthrough_risk if summary else 0.0
            opportunity = summary.attack_opportunity if summary else 0.0
            text = f"Tuyến {lane + 1} | Nguy cơ {risk * 100:.0f}% | Cơ hội {opportunity * 100:.0f}%"
        if not text:
            return
        mx, my = self.mouse_pos
        txt = self.fonts.tiny.render(text, True, Palette.TEXT)
        rect = txt.get_rect(topleft=(mx + 14, my + 14)).inflate(16, 10)
        rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.draw.rect(surface, (9, 15, 28), rect, border_radius=6)
        pygame.draw.rect(surface, Palette.PRIMARY, rect, 1, border_radius=6)
        surface.blit(txt, txt.get_rect(center=rect.center))

    def _draw_ai_debug(self, surface: pygame.Surface, gs: GameState,
                       lane_summaries: List[LaneSummary]) -> None:
        if not lane_summaries:
            return
        rect = pygame.Rect(self.battle_rect.right - 274, self.battle_rect.y + 42, 254, 106)
        overlay = pygame.Surface(rect.size, pygame.SRCALPHA)
        overlay.fill((8, 13, 26, 204))
        surface.blit(overlay, rect.topleft)
        pygame.draw.rect(surface, Palette.PRIMARY, rect, 1, border_radius=8)
        draw_text(surface, "GỠ LỖI AI", (rect.x + 12, rect.y + 10), self.fonts.tiny, Palette.PRIMARY)
        draw_text(surface, "Nguy cơ", (rect.x + 52, rect.y + 28), self.fonts.tiny, Palette.TEXT_DIM)
        draw_text(surface, "Cơ hội", (rect.x + 150, rect.y + 28), self.fonts.tiny, Palette.TEXT_DIM)
        for summary in lane_summaries[:3]:
            row_y = rect.y + 48 + summary.lane_id * 17
            draw_text(surface, f"T{summary.lane_id + 1}", (rect.x + 14, row_y - 2), self.fonts.tiny, Palette.TEXT)
            draw_bar(surface, pygame.Rect(rect.x + 52, row_y + 2, 72, 6),
                     summary.breakthrough_risk, danger_color(summary.breakthrough_risk))
            draw_text(surface, f"{summary.breakthrough_risk * 100:.0f}%", (rect.x + 128, row_y - 3),
                      self.fonts.tiny, Palette.TEXT_MUTED)
            draw_bar(surface, pygame.Rect(rect.x + 166, row_y + 2, 56, 6),
                     summary.attack_opportunity, Palette.PRIMARY)
            draw_text(surface, f"{summary.attack_opportunity * 100:.0f}%", (rect.x + 226, row_y - 3),
                      self.fonts.tiny, Palette.TEXT_MUTED)

    def _draw_game_over(self, surface: pygame.Surface, gs: GameState) -> None:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 176))
        surface.blit(overlay, (0, 0))
        winner = gs.get_winner()
        if winner == "PLAYER":
            msg, col = "CHIẾN THẮNG", Palette.PLAYER
        elif winner == "AI":
            msg, col = "THẤT BẠI", Palette.AI
        else:
            msg, col = "HÒA", Palette.RESOURCE

        rect = pygame.Rect(SCREEN_WIDTH // 2 - 260, SCREEN_HEIGHT // 2 - 96, 520, 192)
        draw_panel(surface, rect, None, self.fonts.small, fill=(12, 18, 30), border=col)
        draw_text(surface, msg, (SCREEN_WIDTH // 2, rect.y + 48), self.fonts.title, col, align="center")
        draw_text(surface, f"Máu người chơi {gs.player_base.hp:.0f}  |  Máu AI {gs.ai_base.hp:.0f}",
                  (SCREEN_WIDTH // 2, rect.y + 88), self.fonts.medium, Palette.TEXT, align="center")
        draw_text(surface, f"Thời gian {gs.match_time:.0f}s  |  Log đã lưu trong logs/",
                  (SCREEN_WIDTH // 2, rect.y + 120), self.fonts.small, Palette.TEXT_MUTED, align="center")
        draw_text(surface, "Nhấn ESC để thoát", (SCREEN_WIDTH // 2, rect.y + 150),
                  self.fonts.small, Palette.TEXT_DIM, align="center")

    def _hovered_tower(self, gs: Optional[GameState]):
        if gs is None:
            return None
        mx, my = self.mouse_pos
        for tower in gs.player_towers + gs.ai_towers:
            x, y = self._to_view_pos(tower.position)
            if abs(mx - x) <= 18 and abs(my - y) <= 18:
                return tower
        return None

    def _hovered_lane(self) -> Optional[int]:
        mx, my = self.mouse_pos
        if not self.battle_rect.collidepoint(mx, my):
            return None
        for lane_id, lane_y in enumerate(LANE_Y_POSITIONS):
            lane_rect = pygame.Rect(self.battle_rect.x + 16, lane_y - 30, self.battle_rect.w - 32, 60)
            if lane_rect.collidepoint(mx, my):
                return lane_id
        return None

    def _lane_risk(self, gs: GameState, lane_id: int, summary: Optional[LaneSummary]) -> float:
        if summary is not None:
            return summary.breakthrough_risk
        pressure = sum(1 for u in gs.active_units if u.owner == Owner.AI and u.lane_id == lane_id)
        return min(1.0, pressure * 0.18)

    def _risk_label(self, risk: float):
        if risk >= 0.70:
            return "NGUY HIỂM", Palette.DANGER_HIGH
        if risk >= 0.40:
            return "CÂN BẰNG", Palette.RESOURCE
        return "AN TOÀN", Palette.GREEN

    def _draw_corner_box(self, surface: pygame.Surface, rect: pygame.Rect, color, width: int = 1) -> None:
        l = 8
        points = [
            ((rect.left, rect.top + l), (rect.left, rect.top), (rect.left + l, rect.top)),
            ((rect.right - l, rect.top), (rect.right, rect.top), (rect.right, rect.top + l)),
            ((rect.right, rect.bottom - l), (rect.right, rect.bottom), (rect.right - l, rect.bottom)),
            ((rect.left + l, rect.bottom), (rect.left, rect.bottom), (rect.left, rect.bottom - l)),
        ]
        for a, b, c in points:
            pygame.draw.line(surface, color, a, b, width)
            pygame.draw.line(surface, color, b, c, width)

    def _scale_x(self) -> float:
        domain_w = (AI_BASE_X + 70) - (PLAYER_BASE_X - 70)
        return self.battle_rect.w / domain_w

    def _to_view_pos(self, pos: Tuple[float, float]) -> Tuple[float, float]:
        min_x = PLAYER_BASE_X - 70
        max_x = AI_BASE_X + 70
        x, y = pos
        t = (x - min_x) / max(1, max_x - min_x)
        view_x = self.battle_rect.x + t * self.battle_rect.w
        return (view_x, y)

    def _event_to_view(self, event: dict) -> dict:
        mapped = dict(event)
        for key in ("pos", "source_pos", "target_pos"):
            if mapped.get(key):
                mapped[key] = self._to_view_pos(mapped[key])
        return mapped

    def _owner_label(self, owner: Owner) -> str:
        return "Người chơi" if owner == Owner.PLAYER else "AI"

    def _ai_label(self) -> str:
        name = self.engine.ai_agent.name
        return {
            "random": "Ngẫu nhiên",
            "rule_based": "Theo luật",
            "heuristic_defensive": "Đánh giá phòng thủ",
            "heuristic_aggressive": "Đánh giá tấn công",
            "heuristic_balanced": "Đánh giá cân bằng",
        }.get(name, name.replace("_", " "))

    def _action_description(self, action: Optional[Action]) -> str:
        if action is None:
            return "Chưa có hành động"
        lane = f"tuyến {action.target_lane + 1}" if action.target_lane is not None else "không rõ tuyến"
        if action.action_type == ActionType.BUILD_TOWER:
            return f"Xây tháp {self._tower_label(action.entity_type)} - {lane}"
        if action.action_type == ActionType.UPGRADE_TOWER:
            return f"Nâng cấp tháp #{action.target_tower_id} - {lane}"
        if action.action_type == ActionType.SEND_UNIT:
            quantity = action.metadata.get("quantity", 1)
            return f"Gửi x{quantity} quân {self._unit_label(action.entity_type)} - {lane}"
        if action.action_type == ActionType.SAVE_RESOURCE:
            return "Tích lũy tài nguyên"
        return "Không hành động"

    def _draw_wrapped(self, surface, text: str, x: int, y: int, width: int,
                      font: pygame.font.Font, color) -> int:
        words = text.split()
        line = ""
        for word in words:
            trial = f"{line} {word}".strip()
            if font.size(trial)[0] <= width:
                line = trial
            else:
                draw_text(surface, line, (x, y), font, color)
                y += font.get_height() + 2
                line = word
        if line:
            draw_text(surface, line, (x, y), font, color)
            y += font.get_height() + 2
        return y

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
