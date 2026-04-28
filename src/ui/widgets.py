"""Reusable Pygame UI widgets."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional, Tuple

import pygame

from src.ui.theme import Color, Layout, Palette


def draw_panel(
    surface: pygame.Surface,
    rect: pygame.Rect,
    title: str | None,
    font: pygame.font.Font,
    *,
    fill: Color = Palette.SURFACE,
    border: Color = Palette.LINE_SOFT,
) -> None:
    pygame.draw.rect(surface, fill, rect, border_radius=Layout.PANEL_RADIUS)
    pygame.draw.rect(surface, border, rect, 1, border_radius=Layout.PANEL_RADIUS)
    if title:
        txt = font.render(title.upper(), True, Palette.TEXT_MUTED)
        surface.blit(txt, (rect.x + 12, rect.y + 8))


def draw_bar(
    surface: pygame.Surface,
    rect: pygame.Rect,
    ratio: float,
    color: Color,
    *,
    bg: Color = (35, 40, 52),
    border: Color = Palette.LINE_SOFT,
) -> None:
    ratio = max(0.0, min(1.0, ratio))
    pygame.draw.rect(surface, bg, rect, border_radius=4)
    if ratio > 0:
        fill_rect = pygame.Rect(rect.x, rect.y, int(rect.w * ratio), rect.h)
        pygame.draw.rect(surface, color, fill_rect, border_radius=4)
    pygame.draw.rect(surface, border, rect, 1, border_radius=4)


def draw_text(
    surface: pygame.Surface,
    text: str,
    pos: Tuple[int, int],
    font: pygame.font.Font,
    color: Color = Palette.TEXT,
) -> pygame.Rect:
    rendered = font.render(text, True, color)
    rect = rendered.get_rect(topleft=pos)
    surface.blit(rendered, rect)
    return rect


@dataclass
class Button:
    rect: pygame.Rect
    label: str
    color: Color
    hover_color: Color
    callback: Optional[Callable[[], None]] = None
    sublabel: str = ""
    icon: Optional[pygame.Surface] = None
    selected: bool = False
    enabled: bool = True
    hovered: bool = False

    def draw(
        self,
        surface: pygame.Surface,
        font: pygame.font.Font,
        small_font: pygame.font.Font,
    ) -> None:
        if not self.enabled:
            fill = Palette.SURFACE_3
            text_color = Palette.TEXT_DIM
            border = Palette.LINE_SOFT
        else:
            fill = self.hover_color if self.hovered else self.color
            text_color = Palette.TEXT
            border = Palette.CYAN if self.selected else Palette.LINE

        if self.selected and self.enabled:
            glow = self.rect.inflate(8, 8)
            pygame.draw.rect(surface, Palette.CYAN, glow, width=1, border_radius=Layout.BUTTON_RADIUS)

        pygame.draw.rect(surface, fill, self.rect, border_radius=Layout.BUTTON_RADIUS)
        pygame.draw.rect(surface, border, self.rect, 2 if self.selected else 1,
                         border_radius=Layout.BUTTON_RADIUS)

        label = font.render(self.label, True, text_color)
        if self.icon:
            icon = self.icon.copy()
            if not self.enabled:
                icon.set_alpha(90)
            icon_rect = icon.get_rect(midleft=(self.rect.x + 8, self.rect.centery))
            surface.blit(icon, icon_rect)
            label_x = icon_rect.right + 5
            if self.sublabel:
                sub = small_font.render(self.sublabel, True, Palette.RESOURCE if self.enabled else Palette.TEXT_DIM)
                total_h = label.get_height() + sub.get_height() + 2
                y = self.rect.centery - total_h // 2
                surface.blit(label, label.get_rect(left=label_x, top=y))
                surface.blit(sub, sub.get_rect(left=label_x, top=y + label.get_height() + 2))
            else:
                surface.blit(label, label.get_rect(left=label_x, centery=self.rect.centery))
            return

        if self.sublabel:
            sub = small_font.render(self.sublabel, True, Palette.RESOURCE if self.enabled else Palette.TEXT_DIM)
            total_h = label.get_height() + sub.get_height() + 2
            y = self.rect.centery - total_h // 2
            surface.blit(label, label.get_rect(centerx=self.rect.centerx, top=y))
            surface.blit(sub, sub.get_rect(centerx=self.rect.centerx, top=y + label.get_height() + 2))
        else:
            surface.blit(label, label.get_rect(center=self.rect.center))

    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos) and self.enabled and self.callback:
                self.callback()
                return True
        return False
