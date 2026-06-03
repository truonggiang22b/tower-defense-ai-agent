"""Reusable Pygame UI widgets."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional, Tuple

import pygame

from src.ui.theme import Color, Layout, Palette, Radius


def draw_panel(
    surface: pygame.Surface,
    rect: pygame.Rect,
    title: str | None,
    font: pygame.font.Font,
    *,
    fill: Color = Palette.SURFACE,
    border: Color = Palette.LINE_SOFT,
    shadow: bool = True,
    header: bool = True,
) -> None:
    if shadow:
        shadow_rect = rect.move(0, 4)
        pygame.draw.rect(surface, (0, 0, 0), shadow_rect, border_radius=Layout.PANEL_RADIUS)
        shadow_surf = pygame.Surface(rect.size, pygame.SRCALPHA)
        shadow_surf.fill((0, 0, 0, 72))
        surface.blit(shadow_surf, shadow_rect.topleft)

    pygame.draw.rect(surface, fill, rect, border_radius=Layout.PANEL_RADIUS)
    pygame.draw.rect(surface, border, rect, 1, border_radius=Layout.PANEL_RADIUS)
    if title:
        title_rect = pygame.Rect(rect.x, rect.y, rect.w, 30)
        if header:
            pygame.draw.rect(surface, Palette.SURFACE_2, title_rect,
                             border_top_left_radius=Layout.PANEL_RADIUS,
                             border_top_right_radius=Layout.PANEL_RADIUS)
            pygame.draw.line(surface, Palette.LINE_SOFT, (rect.x, rect.y + 30), (rect.right, rect.y + 30))
        txt = font.render(title.upper(), True, Palette.TEXT_MUTED)
        surface.blit(txt, (rect.x + 12, rect.y + 9))


def draw_bar(
    surface: pygame.Surface,
    rect: pygame.Rect,
    ratio: float,
    color: Color,
    *,
    bg: Color = (20, 28, 43),
    border: Color = Palette.LINE_SOFT,
    label: str | None = None,
    font: Optional[pygame.font.Font] = None,
) -> None:
    ratio = max(0.0, min(1.0, ratio))
    pygame.draw.rect(surface, bg, rect, border_radius=Radius.SM)
    if ratio > 0:
        fill_rect = pygame.Rect(rect.x, rect.y, max(2, int(rect.w * ratio)), rect.h)
        pygame.draw.rect(surface, color, fill_rect, border_radius=Radius.SM)
        shine = pygame.Rect(fill_rect.x, fill_rect.y, fill_rect.w, max(1, fill_rect.h // 3))
        pygame.draw.rect(surface, tuple(min(255, c + 35) for c in color), shine,
                         border_radius=Radius.SM)
    pygame.draw.rect(surface, border, rect, 1, border_radius=Radius.SM)
    if label and font:
        txt = font.render(label, True, Palette.TEXT)
        surface.blit(txt, txt.get_rect(center=rect.center))


def draw_text(
    surface: pygame.Surface,
    text: str,
    pos: Tuple[int, int],
    font: pygame.font.Font,
    color: Color = Palette.TEXT,
    *,
    align: str = "left",
) -> pygame.Rect:
    rendered = font.render(text, True, color)
    if align == "center":
        rect = rendered.get_rect(center=pos)
    elif align == "right":
        rect = rendered.get_rect(topright=pos)
    else:
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
    tooltip: str = ""
    disabled_reason: str = ""
    selected: bool = False
    enabled: bool = True
    hovered: bool = False
    pressed: bool = False

    def draw(
        self,
        surface: pygame.Surface,
        font: pygame.font.Font,
        small_font: pygame.font.Font,
    ) -> None:
        draw_rect = self.rect.copy()
        if self.hovered and self.enabled:
            draw_rect = draw_rect.inflate(4, 4)
        if self.pressed and self.enabled:
            draw_rect = draw_rect.inflate(-2, -2).move(0, 1)

        if not self.enabled:
            fill = (18, 26, 39)
            text_color = Palette.TEXT_DIM
            border = (30, 41, 59)
        else:
            fill = self.hover_color if self.hovered else self.color
            text_color = Palette.TEXT
            border = Palette.PRIMARY if self.selected else Palette.LINE

        shadow = draw_rect.move(0, 2)
        pygame.draw.rect(surface, (0, 0, 0), shadow, border_radius=Layout.BUTTON_RADIUS)
        shadow_surf = pygame.Surface(draw_rect.size, pygame.SRCALPHA)
        shadow_surf.fill((0, 0, 0, 42 if self.enabled else 24))
        surface.blit(shadow_surf, shadow.topleft)

        if self.selected and self.enabled:
            glow = draw_rect.inflate(6, 6)
            pygame.draw.rect(surface, Palette.PRIMARY, glow, width=1, border_radius=Layout.BUTTON_RADIUS)

        pygame.draw.rect(surface, fill, draw_rect, border_radius=Layout.BUTTON_RADIUS)
        pygame.draw.rect(surface, border, draw_rect, 2 if self.selected else 1,
                         border_radius=Layout.BUTTON_RADIUS)
        if not self.enabled:
            veil = pygame.Surface(draw_rect.size, pygame.SRCALPHA)
            veil.fill((5, 10, 20, 62))
            surface.blit(veil, draw_rect.topleft)

        label = font.render(self.label, True, text_color)
        label_area_left = draw_rect.x + 10
        if self.icon:
            icon = self.icon.copy()
            if not self.enabled:
                icon.set_alpha(55)
            icon_rect = icon.get_rect(midleft=(draw_rect.x + 8, draw_rect.centery))
            surface.blit(icon, icon_rect)
            label_area_left = icon_rect.right + 6

        if self.sublabel:
            sub_color = Palette.RESOURCE if self.enabled else Palette.TEXT_DIM
            sub = small_font.render(self.sublabel, True, sub_color)
            total_h = label.get_height() + sub.get_height() + 2
            y = draw_rect.centery - total_h // 2
            surface.blit(label, label.get_rect(left=label_area_left, top=y))
            surface.blit(sub, sub.get_rect(right=draw_rect.right - 10, top=y + label.get_height() + 2))
        else:
            if self.icon:
                surface.blit(label, label.get_rect(left=label_area_left, centery=draw_rect.centery))
            else:
                surface.blit(label, label.get_rect(center=draw_rect.center))

    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.pressed = self.rect.collidepoint(event.pos) and self.enabled
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            was_pressed = self.pressed
            self.pressed = False
            if was_pressed and self.rect.collidepoint(event.pos) and self.enabled and self.callback:
                self.callback()
                return True
        return False
