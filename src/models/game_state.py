"""
Core data models: GameState, Base, Tower, Unit, Lane, Action
Theo thiết kế trong tài liệu 04 - Kiến trúc hệ thống và mô hình dữ liệu.md
"""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Dict, Optional, Tuple, Any
import time


# ============================================================
# Enums
# ============================================================

class Owner(Enum):
    PLAYER = "player"
    AI = "ai"


class TowerType(Enum):
    FAST = "fast"      # Tháp nhanh: sát thương thấp, tốc độ bắn cao
    HEAVY = "heavy"    # Tháp nặng: sát thương cao, tốc độ bắn chậm
    BALANCED = "balanced"  # Tháp cân bằng: chỉ số trung bình


class UnitType(Enum):
    FAST = "fast"      # Quân nhanh: máu thấp, tốc độ cao
    TANK = "tank"      # Quân trâu: máu cao, tốc độ thấp
    SWARM = "swarm"    # Quân rẻ: chi phí thấp, số lượng cao


class ActionType(Enum):
    BUILD_TOWER = "build_tower"
    UPGRADE_TOWER = "upgrade_tower"
    SEND_UNIT = "send_unit"
    SAVE_RESOURCE = "save_resource"
    NO_ACTION = "no_action"


# ============================================================
# Tower config - dữ liệu cấu hình tháp theo loại và cấp
# ============================================================

TOWER_CONFIGS = {
    TowerType.FAST: {
        1: {"damage": 10, "range": 150, "attack_interval": 0.4, "cost": 80, "upgrade_cost": 60, "color": (100, 200, 255)},
        2: {"damage": 16, "range": 165, "attack_interval": 0.35, "cost": 80, "upgrade_cost": 80, "color": (50, 160, 230)},
        3: {"damage": 24, "range": 180, "attack_interval": 0.30, "cost": 80, "upgrade_cost": 0,  "color": (20, 120, 200)},
    },
    TowerType.HEAVY: {
        1: {"damage": 40, "range": 130, "attack_interval": 1.5, "cost": 130, "upgrade_cost": 100, "color": (220, 100, 80)},
        2: {"damage": 65, "range": 145, "attack_interval": 1.3, "cost": 130, "upgrade_cost": 120, "color": (200, 60, 40)},
        3: {"damage": 95, "range": 160, "attack_interval": 1.1, "cost": 130, "upgrade_cost": 0,  "color": (170, 30, 10)},
    },
    TowerType.BALANCED: {
        1: {"damage": 22, "range": 140, "attack_interval": 0.9, "cost": 100, "upgrade_cost": 75, "color": (120, 200, 120)},
        2: {"damage": 35, "range": 155, "attack_interval": 0.8, "cost": 100, "upgrade_cost": 90, "color": (80, 170, 80)},
        3: {"damage": 52, "range": 170, "attack_interval": 0.7, "cost": 100, "upgrade_cost": 0,  "color": (40, 140, 40)},
    },
}

# ============================================================
# Unit config
# ============================================================

UNIT_CONFIGS = {
    UnitType.FAST: {
        "hp": 50, "damage_to_base": 8, "speed": 90,  "cost": 50,
        "reward": 10, "color": (255, 200, 50), "radius": 7
    },
    UnitType.TANK: {
        "hp": 200, "damage_to_base": 20, "speed": 35, "cost": 120,
        "reward": 25, "color": (180, 120, 60), "radius": 12
    },
    UnitType.SWARM: {
        "hp": 25, "damage_to_base": 5, "speed": 65, "cost": 30,
        "reward": 5,  "color": (220, 180, 220), "radius": 5
    },
}

MAX_TOWER_LEVEL = 3


# ============================================================
# Base
# ============================================================

@dataclass
class Base:
    owner: Owner
    hp: float
    max_hp: float
    position: Tuple[int, int]   # tọa độ trung tâm trên màn hình

    def take_damage(self, amount: float) -> float:
        actual = min(amount, self.hp)
        self.hp = max(0.0, self.hp - amount)
        return actual

    def is_destroyed(self) -> bool:
        return self.hp <= 0

    def hp_ratio(self) -> float:
        return self.hp / self.max_hp if self.max_hp > 0 else 0.0


# ============================================================
# Tower
# ============================================================

@dataclass
class Tower:
    tower_id: int
    tower_type: TowerType
    level: int
    owner: Owner
    lane_id: int
    slot_index: int
    position: Tuple[int, int]

    # Chỉ số tính toán từ config
    damage: float = 0.0
    range: float = 0.0
    attack_interval: float = 1.0
    upgrade_cost: int = 0

    # Trạng thái
    attack_cooldown: float = 0.0   # giây còn lại
    hp: float = 100.0

    def __post_init__(self):
        self._apply_config()

    def _apply_config(self):
        cfg = TOWER_CONFIGS[self.tower_type][self.level]
        self.damage = cfg["damage"]
        self.range = cfg["range"]
        self.attack_interval = cfg["attack_interval"]
        self.upgrade_cost = cfg["upgrade_cost"]

    def can_attack(self, target: 'Unit') -> bool:
        if self.attack_cooldown > 0:
            return False
        tx, ty = target.position
        sx, sy = self.position
        dist = ((tx - sx)**2 + (ty - sy)**2) ** 0.5
        return dist <= self.range

    def can_upgrade(self) -> bool:
        return self.level < MAX_TOWER_LEVEL

    def upgrade(self):
        if self.can_upgrade():
            self.level += 1
            self._apply_config()

    def get_color(self):
        return TOWER_CONFIGS[self.tower_type][self.level]["color"]

    def get_upgrade_cost(self) -> int:
        if self.can_upgrade():
            return TOWER_CONFIGS[self.tower_type][self.level]["upgrade_cost"]
        return 0

    def get_build_cost(self) -> int:
        return TOWER_CONFIGS[self.tower_type][1]["cost"]


# ============================================================
# Unit
# ============================================================

_unit_id_counter = 0

def _next_unit_id() -> int:
    global _unit_id_counter
    _unit_id_counter += 1
    return _unit_id_counter


@dataclass
class Unit:
    unit_type: UnitType
    owner: Owner
    lane_id: int

    unit_id: int = field(default_factory=_next_unit_id)
    hp: float = 0.0
    max_hp: float = 0.0
    damage_to_base: float = 0.0
    speed: float = 0.0
    cost: int = 0
    reward: int = 0
    position: float = 0.0   # tiến trình trên lane (0.0 = spawn, 1.0 = đến base)

    def __post_init__(self):
        cfg = UNIT_CONFIGS[self.unit_type]
        if self.hp == 0.0:
            self.hp = cfg["hp"]
            self.max_hp = cfg["hp"]
        if self.damage_to_base == 0.0:
            self.damage_to_base = cfg["damage_to_base"]
        if self.speed == 0.0:
            self.speed = cfg["speed"]
        if self.cost == 0:
            self.cost = cfg["cost"]
        if self.reward == 0:
            self.reward = cfg["reward"]

    def take_damage(self, amount: float) -> bool:
        """Trả về True nếu đơn vị chết"""
        self.hp = max(0.0, self.hp - amount)
        return self.hp <= 0

    def is_dead(self) -> bool:
        return self.hp <= 0

    def hp_ratio(self) -> float:
        return self.hp / self.max_hp if self.max_hp > 0 else 0.0

    def get_color(self):
        return UNIT_CONFIGS[self.unit_type]["color"]

    def get_radius(self):
        return UNIT_CONFIGS[self.unit_type]["radius"]


# ============================================================
# Lane - bản đồ lane cố định
# ============================================================

@dataclass
class Lane:
    lane_id: int
    length: float                    # pixel length
    build_slots: List[Tuple[int, int]]   # (x, y) tọa độ slot xây tháp (phía defender)
    player_spawn: Tuple[int, int]    # điểm spawn quân của player
    ai_spawn: Tuple[int, int]        # điểm spawn quân của AI
    player_base_end: Tuple[int, int] # điểm gây damage cho player base
    ai_base_end: Tuple[int, int]     # điểm gây damage cho ai base

    # Danger score - được tính mỗi tick
    danger_score: float = 0.0        # 0.0 - 1.0, player side bị đe dọa
    ai_danger_score: float = 0.0     # AI side bị đe dọa

    def get_spawn_point(self, owner: Owner) -> Tuple[int, int]:
        return self.player_spawn if owner == Owner.PLAYER else self.ai_spawn

    def get_base_target(self, owner: Owner) -> Tuple[int, int]:
        """Điểm đích mà quân của owner đang tiến tới"""
        return self.ai_base_end if owner == Owner.PLAYER else self.player_base_end


# ============================================================
# Action
# ============================================================

@dataclass
class Action:
    action_type: ActionType
    actor: Owner
    target_lane: Optional[int] = None
    entity_type: Optional[Any] = None   # TowerType hoặc UnitType
    target_tower_id: Optional[int] = None
    cost: int = 0
    metadata: Dict = field(default_factory=dict)

    def get_description(self) -> str:
        if self.action_type == ActionType.BUILD_TOWER:
            return f"BUILD {self.entity_type.value if self.entity_type else '?'} tower on lane {self.target_lane}"
        elif self.action_type == ActionType.UPGRADE_TOWER:
            return f"UPGRADE tower #{self.target_tower_id} on lane {self.target_lane}"
        elif self.action_type == ActionType.SEND_UNIT:
            quantity = self.metadata.get("quantity", 1)
            return f"SEND x{quantity} {self.entity_type.value if self.entity_type else '?'} unit to lane {self.target_lane}"
        elif self.action_type == ActionType.SAVE_RESOURCE:
            return "SAVE resource"
        return "NO_ACTION"


# ============================================================
# LaneSummary - trạng thái rút gọn của lane cho AI
# ============================================================

@dataclass
class LaneSummary:
    lane_id: int
    enemy_unit_pressure: float      # áp lực quân địch đang tiến vào AI (0.0-1.0)
    friendly_unit_pressure: float   # áp lực quân AI đang tiến vào player
    enemy_tower_strength: float     # độ mạnh tháp địch (player)
    friendly_tower_strength: float  # độ mạnh tháp AI
    breakthrough_risk: float        # nguy cơ lane bị vỡ phía AI (0.0-1.0)
    attack_opportunity: float       # cơ hội tấn công lane này (0.0-1.0)
    num_build_slots_free: int       # số slot còn trống phía AI


# ============================================================
# GameState - nguồn sự thật trung tâm
# ============================================================

@dataclass
class GameState:
    # Căn cứ
    player_base: Base
    ai_base: Base

    # Tài nguyên
    player_resource: float
    ai_resource: float
    resource_income_rate: float     # mỗi giây

    # Cấu trúc
    lanes: List[Lane]

    # Tháp (theo owner)
    player_towers: List[Tower] = field(default_factory=list)
    ai_towers: List[Tower] = field(default_factory=list)

    # Quân đang hoạt động
    active_units: List[Unit] = field(default_factory=list)

    # Thời gian
    match_time: float = 0.0         # giây đã trôi qua
    max_match_time: float = 300.0   # giây (5 phút)

    # Thống kê
    player_kills: int = 0
    ai_kills: int = 0
    player_base_damage_dealt: float = 0.0
    ai_base_damage_dealt: float = 0.0
    player_unit_damage_dealt: float = 0.0
    ai_unit_damage_dealt: float = 0.0
    player_damage_dealt: float = 0.0
    ai_damage_dealt: float = 0.0
    player_resource_spent: float = 0.0
    ai_resource_spent: float = 0.0
    player_attack_count: int = 0
    player_defense_count: int = 0
    ai_attack_count: int = 0
    ai_defense_count: int = 0
    ai_economy_count: int = 0
    player_attack_lane_counts: Dict[int, int] = field(default_factory=dict)
    ai_attack_lane_counts: Dict[int, int] = field(default_factory=dict)
    player_unit_type_counts: Dict[str, int] = field(default_factory=dict)
    ai_unit_type_counts: Dict[str, int] = field(default_factory=dict)
    player_base_damage_by_lane: Dict[int, float] = field(default_factory=dict)
    ai_base_damage_by_lane: Dict[int, float] = field(default_factory=dict)

    # Tower ID counter
    _tower_id_counter: int = 0

    def next_tower_id(self) -> int:
        self._tower_id_counter += 1
        return self._tower_id_counter

    def is_game_over(self) -> bool:
        return (self.player_base.is_destroyed() or
                self.ai_base.is_destroyed() or
                self.match_time >= self.max_match_time)

    def get_winner(self) -> Optional[str]:
        if not self.is_game_over():
            return None
        if self.player_base.is_destroyed():
            return "AI"
        if self.ai_base.is_destroyed():
            return "PLAYER"
        # Hết thời gian
        if self.player_base.hp > self.ai_base.hp:
            return "PLAYER"
        elif self.ai_base.hp > self.player_base.hp:
            return "AI"
        return "DRAW"

    def get_towers_by_lane(self, owner: Owner, lane_id: int) -> List[Tower]:
        towers = self.player_towers if owner == Owner.PLAYER else self.ai_towers
        return [t for t in towers if t.lane_id == lane_id]

    def get_units_in_lane(self, lane_id: int) -> List[Unit]:
        return [u for u in self.active_units if u.lane_id == lane_id]

    def get_free_build_slots(self, owner: Owner, lane_id: int) -> List[int]:
        """Trả về danh sách slot_index còn trống"""
        lane = self.lanes[lane_id]
        used = {t.slot_index for t in
                (self.player_towers if owner == Owner.PLAYER else self.ai_towers)
                if t.lane_id == lane_id}
        total = len(lane.build_slots) // 2  # mỗi phía có nửa slots
        return [i for i in range(total) if i not in used]

    def get_resource(self, owner: Owner) -> float:
        return self.player_resource if owner == Owner.PLAYER else self.ai_resource

    def spend_resource(self, owner: Owner, amount: float):
        if owner == Owner.PLAYER:
            self.player_resource -= amount
            self.player_resource_spent += amount
        else:
            self.ai_resource -= amount
            self.ai_resource_spent += amount
