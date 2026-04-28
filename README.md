# Tower Defense AI - Nhập môn Trí tuệ Nhân tạo

> **Đề tài:** Thiết kế tác tử thông minh cho game thủ thành đối kháng người - AI trong môi trường 2D đơn giản

## Giới thiệu

Game thủ thành đối kháng 2D đơn giản giữa người chơi và AI, xây dựng cho môn học **Nhập môn Trí tuệ Nhân tạo**. Hệ thống tập trung vào mô hình hóa tác tử thông minh, thiết kế heuristic, và đánh giá so sánh nhiều chiến lược AI.

## Cài đặt

### Yêu cầu
- Python 3.10+
- pygame 2.x

```bash
pip install pygame
```

### Chạy game tương tác
```bash
# AI mặc định: heuristic balanced
python main.py

# Chọn AI khác
python main.py --ai random
python main.py --ai rule_based
python main.py --ai heuristic --profile defensive
python main.py --ai heuristic --profile aggressive
python main.py --ai heuristic --profile balanced
```

### Chạy batch simulation (không cần UI)
```bash
# Simulation 1 AI
python simulate.py heuristic balanced
python simulate.py random
python simulate.py rule_based

# So sánh tất cả AI profiles (20 trận mỗi loại)
python simulate.py --compare

# Xuất bộ thực nghiệm AI ra JSON/CSV/Markdown
python simulate.py --experiment -n 20 --player balanced --seed 42
```

## Điều khiển (khi chơi tương tác)

| Phím/Nút | Tác dụng |
|---|---|
| Chọn loại tháp | Tháp Nhanh / Tháp Nặng / Tháp CB |
| Chọn loại quân | Quân Nhanh / Quân Trâu / Quân Rẻ |
| Chọn Lane 1/2/3 | Chọn lane để hành động |
| Gửi Quân | Gửi quân đã chọn vào lane đã chọn |
| Xây Tháp | Xây tháp đã chọn ở lane đã chọn |
| Nâng Cấp | Nâng cấp tháp đầu tiên ở lane đã chọn |
| [D] hoặc AI Debug | Hiện thông tin debug AI (danger score, opportunity) |
| [P] | Pause/Resume |
| [ESC] | Thoát |

## Kiến trúc hệ thống

```
src/
├── models/
│   └── game_state.py     # GameState, Base, Tower, Unit, Lane, Action
├── systems/
│   ├── map_manager.py    # MapManager - 3 lane cố định
│   ├── resource_manager.py # ResourceManager
│   ├── tower_manager.py  # TowerManager
│   ├── unit_manager.py   # UnitManager
│   ├── combat_system.py  # CombatSystem
│   └── game_logger.py    # GameLogger
├── ai/
│   ├── ai_agent.py       # RandomAI, RuleBasedAI, HeuristicAI
│   └── heuristic_evaluator.py # HeuristicEvaluator + utility function
├── engine/
│   └── game_engine.py    # GameEngine - game loop
├── ui/
│   └── ui_manager.py     # UIManager - Pygame rendering
└── simulation/
    └── simulation.py     # Batch simulation + comparison
```

## Mô hình AI

### 3 loại AI

| AI | Phương pháp | Mô tả |
|---|---|---|
| RandomAI | Ngẫu nhiên | Chọn hành động random từ tập hợp hợp lệ - baseline |
| RuleBasedAI | Luật đơn giản | Dùng if-then rules: phòng thủ khi bị ép, tấn công khi an toàn |
| HeuristicAI | Utility + Greedy | Tính LaneSummary → sinh candidates → chấm điểm → greedy chọn tốt nhất |

### 3 profile HeuristicAI

| Profile | Trọng số | Đặc trưng |
|---|---|---|
| `defensive` | w2=5, w6=5 cao | Xây/nâng cấp nhiều, phản công khi an toàn |
| `aggressive` | w1=5, w4=5 cao | Gây áp lực liên tục, hy sinh phòng thủ |
| `balanced` | Cân bằng | Chuyển trạng thái theo tình hình |

### Pipeline quyết định (HeuristicAI)

```
GameState → LaneSummary (danger, opportunity, pressure)
         → Candidate Actions (build/upgrade/send/save)
         → Utility Score (7 thành phần có trọng số)
         → Greedy → Best Action
```

### Utility Function

```
Utility = w1*damage_to_player_base
        + w2*ai_base_hp_remaining
        + w3*enemy_units_killed
        + w4*pressure_on_player
        - w5*resource_spent
        - w6*damage_taken_by_ai_base
        - w7*idle_penalty
```

## Gameplay

- **Bản đồ:** 3 lane cố định, mỗi lane 3 slot xây tháp mỗi phía
- **HP căn cứ:** 500 mỗi bên
- **Tài nguyên:** 15/giây, bắt đầu 100
- **Giới hạn:** 5 phút (hết giờ: HP cao hơn thắng)

### Tháp

| Loại | Damage | Range | Speed | Cost | Upgrade |
|---|---|---|---|---|---|
| Fast (Nhanh) | 10 | 150 | 0.4s | 80 | 60→80 |
| Heavy (Nặng) | 40 | 130 | 1.5s | 130 | 100→120 |
| Balanced (CB) | 22 | 140 | 0.9s | 100 | 75→90 |

### Quân

| Loại | HP | Speed | Damage to Base | Cost |
|---|---|---|---|---|
| Fast (Nhanh) | 50 | 90 px/s | 8 | 50 |
| Tank (Trâu) | 200 | 35 px/s | 20 | 120 |
| Swarm (Rẻ) | 25 | 65 px/s | 5 | 30 |

## Log và thống kê

Kết quả tự động ghi vào thư mục `logs/`:
- `{match_id}.json` - chi tiết từng trận
- `batch_{ai_profile}.json` - tổng hợp batch simulation

### Chỉ số đánh giá
- Winner, match duration
- Player/AI base HP cuối trận
- Damage dealt to each base
- Units killed
- Resources spent
- AI decision time (avg/max ms)
- Resource efficiency = damage / resource_spent
- Action counts: attack / defense / economy

## Kết quả thực nghiệm mẫu (3 trận heuristic_balanced)

```
Match sim_000: Winner=AI  | Player HP=0    AI HP=24  | Dur=268s | Eff=0.35
Match sim_001: Winner=AI  | Player HP=0    AI HP=4   | Dur=268s | Eff=0.40
Match sim_002: Winner=PLAYER | Player HP=55 AI HP=0  | Dur=240s | Eff=0.40
```

AI quyết định trung bình < 0.2ms, đủ real-time.

## Local skills cho Codex

Repo này có thêm 5 skill cục bộ trong `.codex/skills/` để hỗ trợ coding đúng trọng tâm của đề tài:

- `tower-defense-core-architecture` - giữ đúng boundary giữa `GameState`, `GameEngine`, systems, AI, UI
- `tower-defense-ai-tuning` - chỉnh heuristic, profiles, candidate generation và buộc kiểm chứng bằng simulation
- `tower-defense-experiment-eval` - chạy so sánh AI và tóm tắt số liệu từ `logs/`
- `tower-defense-realtime-debug` - debug game loop, combat, cooldown, resource, action execution
- `tower-defense-report-writer` - viết phần báo cáo, kết quả thực nghiệm, slide outline và demo script từ tài liệu, code và log

Ví dụ dùng trong prompt:

```text
Use $tower-defense-ai-tuning to improve the balanced heuristic without increasing average decision time.
Use $tower-defense-realtime-debug to find why towers sometimes stop attacking after long matches.
```

## Mở rộng tiếp theo (nếu còn thời gian)

1. Bản đồ lưới + A* pathfinding
2. One-step lookahead trong HeuristicEvaluator
3. Minimax độ sâu 2 cho pha rời rạc
4. Hill-climbing để tinh chỉnh trọng số utility
5. Genetic Algorithm tối ưu cấu hình wave

## Tác giả

Đề tài môn Nhập môn Trí tuệ Nhân tạo - nhóm sinh viên.
