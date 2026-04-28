"""
ResourceManager - Quản lý tài nguyên
Cộng tài nguyên theo thời gian, trừ khi hành động
"""
from __future__ import annotations
from src.models import GameState, Owner


INCOME_RATE = 15.0    # tài nguyên mỗi giây mỗi bên
KILL_REWARD = 0.0     # thưởng khi hạ quân (lấy từ unit.reward)
MAX_RESOURCE = 999    # giới hạn tài nguyên


class ResourceManager:
    def __init__(self):
        self.income_rate = INCOME_RATE

    def update(self, game_state: GameState, delta_time: float):
        """Cộng tài nguyên định kỳ"""
        income = self.income_rate * delta_time
        game_state.player_resource = min(MAX_RESOURCE, game_state.player_resource + income)
        game_state.ai_resource = min(MAX_RESOURCE, game_state.ai_resource + income)

    def can_afford(self, game_state: GameState, owner: Owner, cost: int) -> bool:
        resource = game_state.player_resource if owner == Owner.PLAYER else game_state.ai_resource
        return resource >= cost

    def spend(self, game_state: GameState, owner: Owner, amount: int):
        """Trừ tài nguyên khi thực hiện hành động"""
        game_state.spend_resource(owner, amount)

    def add_kill_reward(self, game_state: GameState, killer_owner: Owner, reward: int):
        """Cộng thưởng khi hạ quân địch"""
        if killer_owner == Owner.PLAYER:
            game_state.player_resource = min(MAX_RESOURCE, game_state.player_resource + reward)
        else:
            game_state.ai_resource = min(MAX_RESOURCE, game_state.ai_resource + reward)
