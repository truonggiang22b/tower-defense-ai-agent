"""Design tokens for the Pygame tactical UI."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


Color = Tuple[int, int, int]


class Palette:
    BG: Color = (11, 18, 32)
    BG_DEEP: Color = (5, 10, 20)
    BG_GRID: Color = (18, 30, 49)
    SURFACE: Color = (17, 27, 44)
    SURFACE_2: Color = (24, 36, 57)
    SURFACE_3: Color = (34, 49, 73)
    SURFACE_GLOW: Color = (7, 89, 120)
    LINE: Color = (55, 72, 98)
    LINE_SOFT: Color = (34, 47, 69)

    TEXT: Color = (239, 246, 255)
    TEXT_MUTED: Color = (176, 190, 211)
    TEXT_DIM: Color = (121, 138, 164)

    PRIMARY: Color = (56, 189, 248)
    PRIMARY_DARK: Color = (2, 132, 199)
    PLAYER: Color = (56, 189, 248)
    PLAYER_DARK: Color = (12, 74, 110)
    AI: Color = (248, 113, 113)
    AI_DARK: Color = (127, 29, 29)
    RESOURCE: Color = (245, 158, 11)
    CYAN: Color = PRIMARY
    GREEN: Color = (34, 197, 94)
    ORANGE: Color = RESOURCE
    PURPLE: Color = (168, 85, 247)

    DANGER_LOW: Color = GREEN
    DANGER_MED: Color = RESOURCE
    DANGER_HIGH: Color = (239, 68, 68)


class Spacing:
    XS = 4
    SM = 8
    MD = 12
    LG = 16
    XL = 24


class Radius:
    SM = 5
    MD = 8
    LG = 12


class FontSize:
    TINY = 12
    SMALL = 14
    MEDIUM = 17
    LARGE = 22
    TITLE = 28


class Layout:
    TOP_BAR_HEIGHT = 64
    LEFT_PANEL_WIDTH = 236
    RIGHT_PANEL_WIDTH = 236
    BOTTOM_LOG_HEIGHT = 110
    SCREEN_PAD = 14
    BATTLE_TOP = TOP_BAR_HEIGHT + SCREEN_PAD
    BUTTON_RADIUS = Radius.MD
    PANEL_RADIUS = Radius.MD
    COMMAND_HEIGHT = 190


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


def hp_color(ratio: float) -> Color:
    if ratio < 0.30:
        return Palette.DANGER_HIGH
    if ratio < 0.60:
        return Palette.DANGER_MED
    return Palette.GREEN


def lerp_color(a: Color, b: Color, t: float) -> Color:
    t = max(0.0, min(1.0, t))
    return (
        int(a[0] + (b[0] - a[0]) * t),
        int(a[1] + (b[1] - a[1]) * t),
        int(a[2] + (b[2] - a[2]) * t),
    )


def with_alpha(color: Color, alpha: int) -> Tuple[int, int, int, int]:
    return (color[0], color[1], color[2], alpha)
