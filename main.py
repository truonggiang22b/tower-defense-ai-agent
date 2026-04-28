"""
Main entry point - Chạy game tương tác Player vs AI
"""
from __future__ import annotations
import pygame
import sys
import argparse
import time

from src.ai.ai_agent import create_ai
from src.engine.game_engine import GameEngine
from src.ui.ui_manager import UIManager
from src.systems.map_manager import MapManager


TARGET_FPS = 60


def parse_args():
    parser = argparse.ArgumentParser(
        description="Tower Defense AI - Nhập môn Trí tuệ nhân tạo"
    )
    parser.add_argument("--ai", default="heuristic",
                        choices=["random", "rule_based", "heuristic"],
                        help="Loại AI: random | rule_based | heuristic")
    parser.add_argument("--profile", default="balanced",
                        choices=["defensive", "aggressive", "balanced"],
                        help="Profile AI (chỉ với heuristic): defensive | aggressive | balanced")
    parser.add_argument("--match-id", default="match_001",
                        help="ID trận đấu để log")
    return parser.parse_args()


def main():
    args = parse_args()

    # Khởi tạo AI
    ai_agent = create_ai(args.ai, args.profile)
    print(f"[Main] AI: {ai_agent.name}  |  Match: {args.match_id}")

    # Khởi tạo engine và UI
    engine = GameEngine(ai_agent)
    map_manager = engine.map_manager
    ui = UIManager(engine, map_manager)

    # Bắt đầu trận
    engine.start_match(args.match_id)

    clock = pygame.time.Clock()
    running = True

    while running:
        dt = clock.tick(TARGET_FPS) / 1000.0
        dt = min(dt, 0.05)  # Cap delta time

        # Xử lý events
        for event in pygame.event.get():
            if not ui.handle_event(event):
                running = False
                break

        # Update game
        if not engine.running and engine.game_state and engine.game_state.is_game_over():
            # Game kết thúc, chỉ render để người chơi xem kết quả
            pass
        else:
            engine.update(dt)

        ui.update(dt)

        # Render
        gs = engine.get_state()
        ui.render(gs, engine.lane_summaries)

    pygame.quit()
    print("[Main] Game kết thúc. Xem log trong thư mục logs/")


if __name__ == "__main__":
    main()
