"""Runtime asset loader with procedural fallbacks for the tactical UI."""
from __future__ import annotations

from pathlib import Path
from typing import Dict, Tuple

import pygame

from src.models import TowerType, UnitType
from src.ui.theme import Palette


ASSET_ROOT = Path(__file__).resolve().parents[2] / "assets"


class AssetManager:
    """Loads project images and creates deterministic fallback sprites."""

    def __init__(self):
        self.cache: Dict[Tuple[str, Tuple[int, int]], pygame.Surface] = {}
        self.background = self._make_background((1280, 570))
        self.lane_texture = self._make_lane_texture((256, 54))

    def tower_icon(self, tower_type: TowerType, size: int = 34) -> pygame.Surface:
        key = f"icons/tower_{tower_type.value}.png"
        return self._load_or_make(key, (size, size), lambda: self._make_tower_icon(tower_type, size))

    def unit_icon(self, unit_type: UnitType, size: int = 30) -> pygame.Surface:
        key = f"icons/unit_{unit_type.value}.png"
        return self._load_or_make(key, (size, size), lambda: self._make_unit_icon(unit_type, size))

    def base_icon(self, owner: str, size: Tuple[int, int] = (92, 132)) -> pygame.Surface:
        key = f"bases/{owner}_base.png"
        return self._load_or_make(key, size, lambda: self._make_base_icon(owner, size))

    def _load_or_make(self, relative_path: str, size: Tuple[int, int], fallback):
        cache_key = (relative_path, size)
        if cache_key in self.cache:
            return self.cache[cache_key]

        path = ASSET_ROOT / relative_path
        surface = None
        if path.exists():
            try:
                surface = pygame.image.load(str(path)).convert_alpha()
                surface = pygame.transform.smoothscale(surface, size)
            except pygame.error:
                surface = None
        if surface is None:
            surface = fallback()
        self.cache[cache_key] = surface
        return surface

    def _make_background(self, size: Tuple[int, int]) -> pygame.Surface:
        w, h = size
        surf = pygame.Surface(size).convert()
        surf.fill(Palette.BG)
        for y in range(h):
            shade = int(10 + 16 * (y / max(1, h)))
            pygame.draw.line(surf, (8, shade, 22 + shade // 2), (0, y), (w, y))
        for x in range(0, w, 40):
            pygame.draw.line(surf, Palette.BG_GRID, (x, 0), (x, h), 1)
        for y in range(0, h, 40):
            pygame.draw.line(surf, Palette.BG_GRID, (0, y), (w, y), 1)
        return surf

    def _make_lane_texture(self, size: Tuple[int, int]) -> pygame.Surface:
        surf = pygame.Surface(size, pygame.SRCALPHA)
        surf.fill((30, 38, 59, 220))
        w, h = size
        for x in range(8, w, 40):
            pygame.draw.line(surf, (78, 93, 122, 95), (x, h // 2 - 5), (x + 22, h // 2 - 5), 1)
            pygame.draw.line(surf, (78, 93, 122, 95), (x, h // 2 + 5), (x + 22, h // 2 + 5), 1)
        pygame.draw.line(surf, (108, 126, 158, 80), (0, h // 2), (w, h // 2), 1)
        return surf

    def _make_tower_icon(self, tower_type: TowerType, size: int) -> pygame.Surface:
        surf = pygame.Surface((size, size), pygame.SRCALPHA)
        center = size // 2
        if tower_type == TowerType.FAST:
            color = (78, 183, 255)
            pygame.draw.polygon(surf, color, [(center, 4), (size - 7, size - 10), (7, size - 10)])
            pygame.draw.circle(surf, Palette.CYAN, (center, center), 5)
        elif tower_type == TowerType.HEAVY:
            color = (235, 95, 76)
            pygame.draw.rect(surf, color, (7, 7, size - 14, size - 12), border_radius=5)
            pygame.draw.rect(surf, (110, 24, 22), (center - 5, 3, 10, size - 6), border_radius=3)
        else:
            color = (91, 205, 126)
            pygame.draw.polygon(surf, color, [(center, 4), (size - 5, center), (center, size - 5), (5, center)])
            pygame.draw.rect(surf, (18, 63, 42), (center - 5, center - 5, 10, 10), border_radius=2)
        pygame.draw.circle(surf, (8, 10, 16), (center, center), center - 2, 2)
        pygame.draw.circle(surf, (238, 245, 255), (center, center), center - 3, 1)
        return surf

    def _make_unit_icon(self, unit_type: UnitType, size: int) -> pygame.Surface:
        surf = pygame.Surface((size, size), pygame.SRCALPHA)
        center = size // 2
        if unit_type == UnitType.FAST:
            color = (255, 210, 59)
            pygame.draw.polygon(surf, color, [(4, center), (size - 5, 5), (size - 10, center), (size - 5, size - 5)])
        elif unit_type == UnitType.TANK:
            color = (205, 132, 63)
            pygame.draw.rect(surf, color, (5, 8, size - 10, size - 16), border_radius=8)
            pygame.draw.circle(surf, (91, 52, 24), (center, center), center // 2)
        else:
            color = (218, 134, 238)
            for dx, dy in [(-5, -5), (5, -4), (-4, 5), (6, 6)]:
                pygame.draw.circle(surf, color, (center + dx, center + dy), 5)
        pygame.draw.circle(surf, (238, 245, 255), (center, center), center - 3, 1)
        return surf

    def _make_base_icon(self, owner: str, size: Tuple[int, int]) -> pygame.Surface:
        w, h = size
        surf = pygame.Surface(size, pygame.SRCALPHA)
        color = Palette.PLAYER if owner == "player" else Palette.AI
        dark = Palette.PLAYER_DARK if owner == "player" else Palette.AI_DARK
        body = pygame.Rect(8, 8, w - 16, h - 16)
        pygame.draw.rect(surf, dark, body, border_radius=15)
        pygame.draw.rect(surf, color, body, 5, border_radius=15)
        core = body.inflate(-24, -36)
        pygame.draw.rect(surf, (15, 24, 42), core, border_radius=9)
        pygame.draw.line(surf, color, (core.left + 8, core.bottom - 12), (core.right - 8, core.bottom - 12), 6)
        pygame.draw.circle(surf, color, (w // 2, core.y + 20), 9, 2)
        return surf
