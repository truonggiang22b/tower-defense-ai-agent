"""
MapManager - Quản lý bản đồ lane cố định
Tạo cấu trúc 3 lane, build slots, spawn points
"""
from __future__ import annotations
from typing import List, Tuple
from src.models import Lane, Owner


# Kích thước màn hình mặc định (pixels)
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 760

# Vị trí căn cứ
PLAYER_BASE_X = 88
AI_BASE_X = SCREEN_WIDTH - 80
BASE_Y = 315

# Số lane
NUM_LANES = 3
LANE_Y_POSITIONS = [155, 315, 475]   # y tọa độ mỗi lane

# Slot xây tháp  
# Phía player: từ left sang
# Phía AI: từ right sang
# Mỗi lane có 4 slot mỗi phía (8 tổng)
TOWER_SLOT_SPACING = 118
NUM_SLOTS_PER_SIDE = 3

# Vùng "middle" lane (không xây được)
LANE_WIDTH_PIXELS = AI_BASE_X - PLAYER_BASE_X


def create_fixed_lanes() -> List[Lane]:
    """
    Tạo 3 lane cố định theo chiều ngang màn hình.
    Mỗi lane có:
      - build_slots cho cả 2 phía (player và AI)
      - spawn points cho mỗi bên
    """
    lanes = []
    lane_length = LANE_WIDTH_PIXELS  # pixels

    for i, lane_y in enumerate(LANE_Y_POSITIONS):
        # Player build slots: các slot gần base player (phía bên trái)
        player_slots = []
        for s in range(NUM_SLOTS_PER_SIDE):
            sx = PLAYER_BASE_X + 120 + s * TOWER_SLOT_SPACING
            player_slots.append((sx, lane_y))

        # AI build slots: các slot gần base AI (phía bên phải)  
        ai_slots = []
        for s in range(NUM_SLOTS_PER_SIDE):
            sx = AI_BASE_X - 120 - s * TOWER_SLOT_SPACING
            ai_slots.append((sx, lane_y))

        # Ghép: player slots trước, AI slots sau
        all_slots = player_slots + ai_slots

        lane = Lane(
            lane_id=i,
            length=float(lane_length),
            build_slots=all_slots,
            player_spawn=(PLAYER_BASE_X + 30, lane_y),
            ai_spawn=(AI_BASE_X - 30, lane_y),
            player_base_end=(PLAYER_BASE_X, lane_y),
            ai_base_end=(AI_BASE_X, lane_y),
        )
        lanes.append(lane)

    return lanes


class MapManager:
    """Quản lý bản đồ lane cố định"""

    def __init__(self):
        self.lanes: List[Lane] = create_fixed_lanes()
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.player_base_pos = (PLAYER_BASE_X, BASE_Y)
        self.ai_base_pos = (AI_BASE_X, BASE_Y)

    def get_lane(self, lane_id: int) -> Lane:
        return self.lanes[lane_id]

    def get_build_slot_pos(self, owner: Owner, lane_id: int, slot_index: int) -> tuple:
        """
        Lấy tọa độ pixel của slot xây tháp.
        Player dùng slot 0..NUM_SLOTS_PER_SIDE-1
        AI dùng slot NUM_SLOTS_PER_SIDE..2*NUM_SLOTS_PER_SIDE-1
        """
        lane = self.lanes[lane_id]
        if owner == Owner.PLAYER:
            return lane.build_slots[slot_index]
        else:
            return lane.build_slots[NUM_SLOTS_PER_SIDE + slot_index]

    def get_num_slots_per_side(self) -> int:
        return NUM_SLOTS_PER_SIDE

    def get_unit_position_pixels(self, owner: Owner, lane_id: int, progress: float) -> Tuple[int, int]:
        """
        Chuyển progress (0.0-1.0) thành tọa độ pixel trên lane.
        progress=0 là điểm spawn, progress=1 là base đối phương.
        """
        lane = self.lanes[lane_id]
        lane_y = LANE_Y_POSITIONS[lane_id]

        if owner == Owner.PLAYER:
            # Di chuyển từ trái (player spawn) sang phải (AI base)
            x = PLAYER_BASE_X + 30 + int((LANE_WIDTH_PIXELS - 60) * progress)
        else:
            # Di chuyển từ phải (AI spawn) sang trái (player base)
            x = AI_BASE_X - 30 - int((LANE_WIDTH_PIXELS - 60) * progress)

        return (x, lane_y)
