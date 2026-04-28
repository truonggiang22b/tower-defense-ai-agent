"""Visual tokens for the Pygame tactical UI."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


Color = Tuple[int, int, int]


class Palette:
    BG: Color = (8, 12, 20)
    BG_GRID: Color = (16, 24, 36)
    SURFACE: Color = (17, 23, 34)
    SURFACE_2: Color = (24, 32, 48)
    SURFACE_3: Color = (33, 43, 61)
    LINE: Color = (71, 87, 113)
    LINE_SOFT: Color = (43, 55, 76)

    TEXT: Color = (237, 244, 255)
    TEXT_MUTED: Color = (157, 169, 189)
    TEXT_DIM: Color = (91, 102, 124)

    PLAYER: Color = (59, 154, 255)
    PLAYER_DARK: Color = (20, 71, 151)
    AI: Color = (236, 72, 86)
    AI_DARK: Color = (132, 29, 39)
    RESOURCE: Color = (252, 207, 72)
    CYAN: Color = (73, 218, 227)
    GREEN: Color = (76, 205, 131)
    ORANGE: Color = (245, 151, 57)
    PURPLE: Color = (166, 105, 255)

    DANGER_LOW: Color = (76, 205, 131)
    DANGER_MED: Color = (245, 180, 62)
    DANGER_HIGH: Color = (239, 68, 68)


class Layout:
    TOP_HUD_HEIGHT = 72
    COMMAND_HEIGHT = 190
    BUTTON_RADIUS = 7
    PANEL_RADIUS = 8


@dataclass(frozen=True)
class Fonts:
    title: object
    large: object
    medium: object
    small: object
    tiny: object


def danger_color(value: float) -> Color:
    if value >= 0.70:
        return Palette.DANGER_HIGH
    if value >= 0.40:
        return Palette.DANGER_MED
    return Palette.DANGER_LOW


def lerp_color(a: Color, b: Color, t: float) -> Color:
    t = max(0.0, min(1.0, t))
    return (
        int(a[0] + (b[0] - a[0]) * t),
        int(a[1] + (b[1] - a[1]) * t),
        int(a[2] + (b[2] - a[2]) * t),
    )
