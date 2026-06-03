"""UI-only battle feedback helpers."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

import pygame

from src.ui.theme import Color, Palette, lerp_color
from src.ui.widgets import draw_text


@dataclass
class FloatingText:
    text: str
    pos: Tuple[float, float]
    color: Color
    ttl: float = 0.85
    age: float = 0.0

    def update(self, dt: float) -> bool:
        self.age += dt
        self.pos = (self.pos[0], self.pos[1] - 34 * dt)
        return self.age < self.ttl

    def draw(self, surface: pygame.Surface, font: pygame.font.Font) -> None:
        alpha = max(0, min(255, int(255 * (1.0 - self.age / self.ttl))))
        text_surf = font.render(self.text, True, self.color)
        text_surf.set_alpha(alpha)
        surface.blit(text_surf, text_surf.get_rect(center=(int(self.pos[0]), int(self.pos[1]))))


@dataclass
class ProjectileEffect:
    start: Tuple[float, float]
    end: Tuple[float, float]
    color: Color
    ttl: float = 0.22
    age: float = 0.0

    def update(self, dt: float) -> bool:
        self.age += dt
        return self.age < self.ttl

    def draw(self, surface: pygame.Surface) -> None:
        t = max(0.0, min(1.0, self.age / self.ttl))
        x = self.start[0] + (self.end[0] - self.start[0]) * t
        y = self.start[1] + (self.end[1] - self.start[1]) * t
        pygame.draw.line(surface, self.color, self.start, (x, y), 2)
        pygame.draw.circle(surface, self.color, (int(x), int(y)), 4)


@dataclass
class FlashEffect:
    pos: Tuple[float, float]
    color: Color
    radius: int = 22
    ttl: float = 0.18
    age: float = 0.0

    def update(self, dt: float) -> bool:
        self.age += dt
        return self.age < self.ttl

    def draw(self, surface: pygame.Surface) -> None:
        alpha = max(0, min(160, int(160 * (1.0 - self.age / self.ttl))))
        size = self.radius * 2 + 8
        surf = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(surf, (*self.color, alpha), (size // 2, size // 2), self.radius)
        surface.blit(surf, (self.pos[0] - size // 2, self.pos[1] - size // 2))


class EffectManager:
    def __init__(self):
        self.floating_texts: List[FloatingText] = []
        self.projectiles: List[ProjectileEffect] = []
        self.flashes: List[FlashEffect] = []
        self.feed: List[Dict] = []

    def consume_events(self, events: List[Dict]) -> None:
        for event in events:
            kind = event.get("kind", "system")
            color = event_color(kind)
            text = event.get("text", "")
            pos = event.get("pos") or event.get("target_pos")
            if text:
                self.feed.insert(0, {"kind": kind, "text": text, "age": 0.0})
                self.feed = self.feed[:8]
            if kind == "damage" and pos:
                amount = event.get("amount", 0)
                self.floating_texts.append(FloatingText(f"-{amount:.0f}", pos, Palette.DANGER_HIGH))
            if kind in {"damage", "base_damage"}:
                start = event.get("source_pos")
                end = event.get("target_pos") or pos
                if start and end:
                    self.projectiles.append(ProjectileEffect(start, end, color))
                if end:
                    self.flashes.append(FlashEffect(end, color))
            elif pos and kind in {"build", "spawn", "upgrade", "reward"}:
                self.flashes.append(FlashEffect(pos, color, radius=18))

    def update(self, dt: float) -> None:
        self.floating_texts = [e for e in self.floating_texts if e.update(dt)]
        self.projectiles = [e for e in self.projectiles if e.update(dt)]
        self.flashes = [e for e in self.flashes if e.update(dt)]
        for entry in self.feed:
            entry["age"] += dt

    def draw_battle_effects(self, surface: pygame.Surface, font: pygame.font.Font) -> None:
        for projectile in self.projectiles:
            projectile.draw(surface)
        for flash in self.flashes:
            flash.draw(surface)
        for floating_text in self.floating_texts:
            floating_text.draw(surface, font)


def event_color(kind: str) -> Color:
    return {
        "damage": Palette.DANGER_HIGH,
        "base_damage": Palette.AI,
        "resource": Palette.RESOURCE,
        "reward": Palette.GREEN,
        "ai": Palette.PRIMARY,
        "build": Palette.PLAYER,
        "spawn": Palette.GREEN,
        "upgrade": Palette.RESOURCE,
        "system": Palette.TEXT_MUTED,
    }.get(kind, Palette.TEXT_MUTED)


def draw_event_feed(
    surface: pygame.Surface,
    rect: pygame.Rect,
    entries: List[Dict],
    font: pygame.font.Font,
    tiny_font: pygame.font.Font,
) -> None:
    if not entries:
        draw_text(surface, "Chưa có sự kiện.", (rect.x + 16, rect.y + 44), font, Palette.TEXT_DIM)
        return
    y = rect.y + 36
    for i, entry in enumerate(entries[:4]):
        kind = entry.get("kind", "system")
        color = event_color(kind)
        row = pygame.Rect(rect.x + 12, y - 3, rect.w - 24, 17)
        if i == 0:
            pygame.draw.rect(surface, (18, 48, 66), row, border_radius=5)
        tag_rect = pygame.Rect(row.x + 6, row.y + 3, 86, 11)
        pygame.draw.rect(surface, lerp_color(color, Palette.SURFACE_2, 0.55), tag_rect, border_radius=4)
        pygame.draw.rect(surface, color, tag_rect, 1, border_radius=4)
        draw_text(surface, event_label(kind), tag_rect.center, tiny_font, Palette.TEXT, align="center")
        content_x = row.x + 102
        draw_text(surface, entry.get("text", ""), (content_x, row.y + 1), font, Palette.TEXT)
        y += 18


def event_label(kind: str) -> str:
    return {
        "damage": "SÁT THƯƠNG",
        "base_damage": "CĂN CỨ",
        "resource": "TÀI NGUYÊN",
        "reward": "THƯỞNG",
        "ai": "AI",
        "build": "XÂY",
        "spawn": "GỬI",
        "upgrade": "NÂNG",
        "system": "HỆ THỐNG",
    }.get(kind, "SỰ KIỆN")


def fit_text(text: str, font: pygame.font.Font, max_width: int) -> str:
    if font.size(text)[0] <= max_width:
        return text
    suffix = "..."
    clipped = text
    while clipped and font.size(clipped + suffix)[0] > max_width:
        clipped = clipped[:-1]
    return clipped + suffix if clipped else suffix
