# 📊 BÁO CÁO TIẾN ĐỘ DỰ ÁN
# Tower Defense AI - Nhập môn Trí tuệ Nhân tạo

> **Cập nhật lần cuối:** 2026-04-28  
> **Trạng thái tổng thể:** 🟢 MVP hoàn thành, game chạy được

---

## 👥 Thông tin dự án

| Mục | Nội dung |
|---|---|
| **Tên đề tài** | Thiết kế tác tử thông minh cho game thủ thành đối kháng người - AI |
| **Môn học** | Nhập môn Trí tuệ Nhân tạo |
| **Môi trường** | Python 3.13 + Pygame 2.6.1 |
| **Thư mục gốc** | `c:\Users\Admin\Desktop\Nhap-Mon-TTNT\` |

---

## ✅ PHASE 1 — Chuẩn bị & Phân tích (HOÀN THÀNH)

### 1.1 Đọc & phân tích tài liệu
- [x] Đọc `README - Hướng dẫn bộ tài liệu.md`
- [x] Đọc `00 - Phân tích tổng hợp đề tài.md` → Xác định entities: Base, Tower, Unit, Lane, Resource, GameState
- [x] Đọc `01 - Phạm vi và phân tích gameplay.md` → Chốt MVP: 3 lane, 3 loại tháp/quân, lane-based movement
- [x] Đọc `02 - Mô hình hóa AI và thiết kế ra quyết định.md` → Xác định percepts, actions, utility function
- [x] Đọc `03 - Thuật toán AI và đánh đổi.md` → Chốt: Rule-based heuristic + Greedy selection
- [x] Đọc `04 - Kiến trúc hệ thống và mô hình dữ liệu.md` → Thiết kế module architecture
- [x] Đọc `05 - Thực nghiệm, chỉ số và đánh giá.md` → Xác định 8 chỉ số đánh giá bắt buộc
- [x] Đọc `06 - Lộ trình, rủi ro và sản phẩm bàn giao.md`
- [x] Đọc `07 - Mục lục báo cáo và checklist demo.md`

### 1.2 Thiết lập môi trường
- [x] Kiểm tra Python 3.13.3 ✓
- [x] Cài đặt `pygame` 2.6.1 ✓
- [x] Scaffold cấu trúc thư mục project theo kiến trúc module

---

## ✅ PHASE 2 — Data Models lõi (HOÀN THÀNH)

**File:** `src/models/game_state.py`

### Các entity đã hiện thực:

| Entity | Mô tả | Thuộc tính chính |
|---|---|---|
| `GameState` | Nguồn sự thật duy nhất của trận đấu | bases, resources, towers, units, match_time |
| `Base` | Căn cứ của mỗi bên | hp=500, max_hp, position, hp_ratio() |
| `Tower` | Tháp phòng thủ | type, level, damage, range, attack_interval, cooldown |
| `Unit` | Quân tấn công | type, hp, speed, position(0→1), damage_to_base |
| `Lane` | Làn đường | lane_id, danger_score, build_slots |
| `Action` | Hành động của tác tử | action_type, actor, target_lane, entity_type, cost |
| `LaneSummary` | Snapshot phân tích lane | breakthrough_risk, attack_opportunity, pressures |

### Configs đã định nghĩa:
```
TOWER_CONFIGS:
  FAST     → Level1: dmg=10, range=150, interval=0.4s, cost=80
  HEAVY    → Level1: dmg=40, range=130, interval=1.5s, cost=130
  BALANCED → Level1: dmg=22, range=140, interval=0.9s, cost=100

UNIT_CONFIGS:
  FAST  → hp=50,  speed=90px/s, cost=50,  reward=12
  TANK  → hp=200, speed=35px/s, cost=120, reward=30
  SWARM → hp=25,  speed=65px/s, cost=30,  reward=8
```

---

## ✅ PHASE 3 — Systems lõi (HOÀN THÀNH)

### MapManager (`src/systems/map_manager.py`)
- [x] 3 lane cố định, khoảng cách đồng đều theo chiều dọc
- [x] Tính tọa độ pixel cho: build slots (mỗi bên 3 slot/lane), spawn points, unit movement
- [x] Constants: SCREEN_WIDTH=1200, GAME_AREA_HEIGHT=500, PLAYER_BASE_X=60, AI_BASE_X=1140

### ResourceManager (`src/systems/resource_manager.py`)
- [x] Thu nhập tự động: 15 vàng/giây cho cả 2 bên
- [x] `spend()` trừ tài nguyên + ghi `resource_spent` vào GameState
- [x] `add_kill_reward()` thưởng khi tiêu diệt quân địch
- [x] `can_afford()` kiểm tra đủ tiền

### TowerManager (`src/systems/tower_manager.py`)
- [x] `build_tower()` đặt tháp vào slot, tính tọa độ pixel
- [x] `upgrade_tower()` tăng level, áp dụng multipliers (damage×1.5, range×1.15)
- [x] `update()` giảm cooldown tháp mỗi tick
- [x] `get_tower_by_id()` lookup

### UnitManager (`src/systems/unit_manager.py`)
- [x] `spawn_unit()` tạo quân tại điểm spawn
- [x] `update()` di chuyển quân theo progress 0.0→1.0 (tỷ lệ với speed/lane_length)
- [x] `get_screen_pos()` chuyển progress → tọa độ pixel
- [x] `get_enemy_units_in_lane()` query theo owner và lane

### CombatSystem (`src/systems/combat_system.py`)
- [x] Tháp chọn mục tiêu: quân địch trong tầm, ưu tiên tiến xa nhất (position cao nhất)
- [x] `_tower_attack()` gây damage, ghi damage stats, trigger kill reward
- [x] `_unit_attack_base()` quân đến base (position≥1.0) gây damage rồi bị loại
- [x] Quản lý vòng đời đơn vị: xóa quân chết và quân đã qua base

---

## ✅ PHASE 4 — AI Agents (HOÀN THÀNH)

### HeuristicEvaluator (`src/ai/heuristic_evaluator.py`)
- [x] `compute_lane_summaries()` → tính 6 chỉ số per-lane:
  - `enemy_unit_pressure` (0→1)
  - `friendly_unit_pressure` (0→1)
  - `enemy_tower_strength` (0→1)
  - `friendly_tower_strength` (0→1)
  - `breakthrough_risk` (nguy cơ bị phá lane)
  - `attack_opportunity` (cơ hội tấn công)
- [x] `score()` tính điểm utility cho từng action type
- [x] 3 profile trọng số: `defensive`, `aggressive`, `balanced`

### AIAgent (`src/ai/ai_agent.py`)

| Class | Phương pháp | Trạng thái |
|---|---|---|
| `RandomAI` | Chọn ngẫu nhiên từ candidates hợp lệ | ✅ |
| `RuleBasedAI` | 4 luật ưu tiên (defensive khi bị ép → attack khi an toàn → build → save) | ✅ |
| `HeuristicAI` | LaneSummary → Candidates → Score → Greedy best | ✅ |

- [x] `create_ai(type, profile)` factory function
- [x] AI cooldown 2.5s giữa các quyết định
- [x] `_generate_candidate_actions()` tạo tập hành động ứng viên

---

## ✅ PHASE 5 — GameEngine & Game Loop (HOÀN THÀNH)

**File:** `src/engine/game_engine.py`

### Thứ tự update mỗi tick:
```
1. match_time += delta_time
2. ResourceManager.update() → cộng thu nhập
3. TowerManager.update()   → giảm cooldown tháp
4. AI cooldown check → AIAgent.decide() → execute_action()
5. UnitManager.update()    → di chuyển quân
6. CombatSystem.update()   → tháp bắn + quân vào base
7. GameState.is_game_over() → kết thúc nếu có winner
```

### execute_action() xử lý:
- [x] `BUILD_TOWER` → kiểm tra slot + tiền → TowerManager.build + spend
- [x] `UPGRADE_TOWER` → kiểm tra level + tiền → TowerManager.upgrade + spend
- [x] `SEND_UNIT` → kiểm tra tiền → UnitManager.spawn + spend
- [x] `SAVE_RESOURCE` → chỉ ghi stats
- [x] Cả Player và AI đều dùng chung execute_action()

---

## ✅ PHASE 6 — GameLogger (HOÀN THÀNH)

**File:** `src/systems/game_logger.py`

### Chỉ số được ghi (theo tài liệu 05):
- [x] Winner (PLAYER / AI / DRAW)
- [x] Match duration (giây)
- [x] Player/AI base HP cuối trận
- [x] Damage dealt to each base
- [x] Units killed (mỗi bên)
- [x] Resources spent (mỗi bên)
- [x] AI action counts: attack / defense / economy
- [x] AI decision time: avg ms, max ms
- [x] Resource efficiency = damage_to_enemy_base / resource_spent

### Output:
- [x] In summary table ra terminal sau mỗi trận
- [x] Ghi `logs/{match_id}.json` (chi tiết + action log)
- [x] `save_batch_summary()` → `logs/batch_{profile}.json`
- [x] `print_batch_stats()` bảng so sánh nhiều AI

---

## ✅ PHASE 7 — UIManager Pygame (HOÀN THÀNH)

**File:** `src/ui/ui_manager.py`

### Giao diện đã implement:
- [x] **3 làn đường** với màu sắc theo danger level (đỏ/vàng/xanh)
- [x] **Danger bar** per-lane hiển thị breakthrough_risk
- [x] **Build slots** cho Player và AI (3 slot/lane)
- [x] **Base rendering** với HP bar màu và HP text
- [x] **Tower rendering** với: màu theo loại, level indicator, range circle, cooldown arc
- [x] **Unit rendering** với: màu theo owner/type, radius theo size, HP bar
- [x] **Bottom panel:** resource, timer, stats, selection indicator, type info
- [x] **10 buttons:** 3 tower types + 3 unit types + send/build/upgrade + AI debug + 3 lane selectors
- [x] **AI Debug overlay** hiển thị LaneSummary real-time (phím D)
- [x] **Game Over overlay** với kết quả và HP cuối
- [x] **Pause** (phím P)

---

## ✅ PHASE 8 — Simulation & Entry Points (HOÀN THÀNH)

### `src/simulation/simulation.py`
- [x] `run_simulation()` chạy batch N trận headless (không cần UI)
- [x] `AutoPlayer` tự động cho Player (random unit spam để test)
- [x] `run_comparison()` so sánh 5 AI configs cùng một bảng

### Entry points:
- [x] `main.py` → game tương tác (argparse: `--ai`, `--profile`, `--match-id`)
- [x] `simulate.py` → batch headless (argparse: type, profile, `-n`, `--compare`)
- [x] `README.md` → hướng dẫn đầy đủ

---

## 🧪 KẾT QUẢ KIỂM THỬ

### Test ngày 2026-04-28

| Test | Kết quả |
|---|---|
| Import tất cả modules | ✅ Thành công |
| Tạo GameState từ đầu | ✅ 3 lanes, HP=500 |
| Khởi tạo 3 loại AI | ✅ random / rule_based / heuristic_balanced |
| Simulation 3 trận heuristic_balanced | ✅ Hoàn thành |
| AI decision time | ✅ avg 0.17ms, max 0.77ms (< 16ms threshold) |
| Game kết thúc đúng (winner detection) | ✅ |
| Log JSON ghi đúng | ✅ `logs/*.json` |

### Sample kết quả 3 trận:
```
Match sim_000: Winner=AI     | Player HP=0  AI HP=24  | Dur=268s | Eff=0.35
Match sim_001: Winner=AI     | Player HP=0  AI HP=4   | Dur=268s | Eff=0.40
Match sim_002: Winner=PLAYER | Player HP=55 AI HP=0   | Dur=240s | Eff=0.40
```

---

## 📁 CẤU TRÚC FILE HIỆN TẠI

```
Nhap-Mon-TTNT/
├── main.py                          ✅ Entry point game tương tác
├── simulate.py                      ✅ Entry point batch simulation
├── README.md                        ✅ Hướng dẫn đầy đủ
│
├── src/
│   ├── models/
│   │   ├── __init__.py              ✅
│   │   └── game_state.py            ✅ GameState, Base, Tower, Unit, Lane, Action, Configs
│   ├── systems/
│   │   ├── __init__.py              ✅
│   │   ├── map_manager.py           ✅ MapManager
│   │   ├── resource_manager.py      ✅ ResourceManager
│   │   ├── tower_manager.py         ✅ TowerManager
│   │   ├── unit_manager.py          ✅ UnitManager
│   │   ├── combat_system.py         ✅ CombatSystem
│   │   └── game_logger.py           ✅ GameLogger, MatchRecord
│   ├── ai/
│   │   ├── __init__.py              ✅
│   │   ├── ai_agent.py              ✅ RandomAI, RuleBasedAI, HeuristicAI
│   │   └── heuristic_evaluator.py   ✅ HeuristicEvaluator, PROFILES
│   ├── engine/
│   │   ├── __init__.py              ✅
│   │   └── game_engine.py           ✅ GameEngine
│   ├── ui/
│   │   ├── __init__.py              ✅
│   │   └── ui_manager.py            ✅ UIManager
│   └── simulation/
│       ├── __init__.py              ✅
│       └── simulation.py            ✅ run_simulation, run_comparison
│
├── docs_tower_defense_ai_project/   📚 Tài liệu phân tích gốc (9 files)
├── logs/                            📊 Log JSON trận đấu (tự tạo khi chơi)
└── progress_report/
    └── 04_TIEN_DO_DU_AN.md          📋 File này
```

---

## 🚀 LỆNH CHẠY NHANH

```bash
# Chạy game tương tác Player vs AI
python main.py --ai heuristic --profile balanced

# Thử AI yếu hơn (dễ thắng hơn)
python main.py --ai random
python main.py --ai rule_based

# AI phòng thủ (khó tấn công)
python main.py --ai heuristic --profile defensive

# AI hung hăng (tấn công liên tục)
python main.py --ai heuristic --profile aggressive

# Batch simulation (không UI)
python simulate.py heuristic balanced

# So sánh tất cả AI
python simulate.py --compare
```

---

## 🔜 VIỆC CÒN LẠI (Nếu có thêm thời gian)

| Ưu tiên | Mục | Mô tả |
|---|---|---|
| 🟡 Medium | Tinh chỉnh balance | Điều chỉnh dmg/cost để trận đấu cân bằng hơn |
| 🟡 Medium | Batch comparison report | Chạy 20 trận/AI tạo bảng so sánh đầy đủ |
| 🔵 Low | Minimax lookahead | Thêm 1-step lookahead vào HeuristicAI |
| 🔵 Low | Hill-climbing tune | Tự động tối ưu weights utility function |
| 🔵 Low | A* pathfinding | Nếu mở rộng sang bản đồ lưới |

---

## 📌 GHI CHÚ KỸ THUẬT

- **GameState** là nguồn sự thật duy nhất — không có state nào được lưu trong Systems
- **Unit position** dùng dạng `float 0.0→1.0` (progress) thay vì pixel để dễ tính và portable
- **AI cooldown 2.5s** giữa các quyết định → tạo cảm giác "suy nghĩ" tự nhiên
- **Decision time < 0.2ms** → đáp ứng yêu cầu real-time (ngưỡng là 16ms/60fps)
- **Windows CP1252 issue** → tất cả print() trong game dùng ASCII để tương thích terminal Windows
- **Encode JSON** → dùng `ensure_ascii=True` cho batch summary, `utf-8` cho chi tiết trận

---

*Báo cáo được tạo tự động bởi Antigravity AI assistant. Cập nhật thủ công khi có tiến độ mới.*

---

## CAP NHAT 2026-04-28 - AI Evaluation Sprint vong 1

- Da chuyen trong tam tu UI sang do luong AI va thuc nghiem.
- Da tach metric damage: base damage va unit damage, tranh viec bao cao phong dai damage vao can cu.
- Da nang cap `simulate.py` de chay `--experiment`, ho tro `-n`, `--seed`, `--player`.
- Da bo sung player tu dong theo chien luoc: `random`, `early_attacker`, `defensive`, `balanced`.
- Da chinh nhe heuristic AI: mo rong candidate thap va them opening-defense bonus.
- Da chay thuc nghiem chinh thuc vong 1: `20 tran / AI`, seed `42`, player strategy `balanced`.
- Ket qua duoc luu tai `logs/experiments/ai_comparison_balanced_20.*`.
- Bao cao ngan da tao tai `progress_report/02_BAO_CAO_THUC_NGHIEM_AI.md`.
- Phat hien chinh: sau khi sua metric, heuristic AI phong thu tot hon nhung kha nang gay damage vao can cu con yeu; can tiep tuc tune utility tan cong.

---

## CAP NHAT 2026-04-28 - AI Evaluation Sprint vong 2

- Da them metric theo lane/loai quan: `ai_attack_lane_counts`, `ai_unit_type_counts`, `ai_base_damage_by_lane`, lane tan cong chinh.
- Da them co che wave nho cho `SEND_UNIT` thong qua `metadata.quantity`, giup AI co the gui 2-4 quan trong mot quyet dinh.
- Da cap nhat logger va summary Markdown/CSV/JSON de xuat them lane tan cong chinh.
- Da tune `HeuristicEvaluator` de uu tien lane yeu, wave co ap luc san, Tank khi lane co thap, va giam Swarm vao lane phong thu manh.
- Da chay lai thuc nghiem chinh `20 tran / AI`, player `balanced`, seed `42`.
- Ket qua: damage heuristic vao Player Base tang tu khoang `3.75` len `26.8`, nhung van chua vuot `rule_based` trong kich ban balanced.
- Da chay them cac kich ban phu `random`, `early_attacker`, `defensive` voi `10 tran / AI`.
- Phat hien: heuristic_defensive thang 90% khi gap player defensive; tat ca AI thang 100% khi player early_attacker; heuristic aggressive can tiep tuc tune de tan cong dung thoi diem hon.
- Bao cao `progress_report/02_BAO_CAO_THUC_NGHIEM_AI.md` da duoc cap nhat them muc vong 2.

---

## CAP NHAT 2026-04-28 - AI Evaluation Sprint vong 3

- Da phan tich log vong 2 va phat hien heuristic gui qua nhieu `swarm`, trong khi `rule_based` gay damage tot hon nho gui `fast`.
- Da tune `HeuristicEvaluator` de uu tien `FAST` tren lane yeu, tang diem fast wave, va giam spam `SWARM` vao lane phong thu manh.
- Da giu nguyen `RandomAI` va `RuleBasedAI` de lam baseline so sanh cong bang.
- Da chay thuc nghiem chinh thuc `30 tran / AI`, player `balanced`, seed `42`.
- Ket qua: `heuristic_balanced` dat damage vao Player Base `118.1`, cao hon `rule_based` la `44.8`.
- Resource efficiency cua `heuristic_balanced` dat `0.026`, cao hon `rule_based` la `0.010`.
- `heuristic_defensive` dat win rate `43.3%` trong batch balanced, cao nhat trong nhom AI hien tai.
- Ket luan: muc tieu vong 3 dat duoc; khong nen tiep tuc tune thu cong qua lau, nen chuyen sang dong goi bao cao hoac them `1-step lookahead` neu can phan nang cao.

---

## CAP NHAT 2026-04-28 - Chuan bi bao cao y tuong online

- Da tao file `progress_report/03_BAO_CAO_TRINH_BAY_Y_TUONG_ONLINE.md` theo dung cac muc giao vien yeu cau.
- Da dieu chinh thong tin nhom con 2 thanh vien: Truong Giang va Binh An.
- Da phan chia cong viec can bang: Truong Giang phu trach game engine/gameplay/UI/tich hop; Binh An phu trach AI/thuat toan/thuc nghiem/bao cao so lieu.
- Bao cao da gom: ten de tai, thanh vien, phan chia cong viec, noi dung du dinh lam, ket qua mong muon, noi dung da lam, kho khan, ke hoach den cuoi ky.
- Bao cao co them phan giai thich nghiep vu game, muc tieu bai toan AI, cac thuat toan/phuong phap AI va kich ban loi noi goi y khi trinh bay online.

---

## CAP NHAT 2026-04-28 - AI Evaluation Sprint vong 4

- Da tiep tuc cai thien cac chi so AI sau buoi bao cao y tuong.
- Van de tap trung: `heuristic_balanced` co damage tot nhung win rate thap vi phong thu chua du.
- Da tune `HeuristicEvaluator` de tang uu tien `BUILD_TOWER` va `UPGRADE_TOWER` khi AI HP thap hoac lane co rui ro.
- Da giam diem `SEND_UNIT` cua `heuristic_balanced` khi AI HP duoi nguong an toan va lane dang nguy hiem.
- Da chay lai thuc nghiem `30 tran / AI`, player `balanced`, seed `42`.
- Ket qua: win rate cua `heuristic_balanced` tang tu `3.3%` len `16.7%`.
- AI HP trung binh cua `heuristic_balanced` tang tu `292.8` len `340.3`.
- Damage vao Player Base cua `heuristic_balanced` van giu `118.1`, khong mat suc tan cong.
- Bao cao `progress_report/02_BAO_CAO_THUC_NGHIEM_AI.md` da cap nhat them muc vong 4.

---

## CAP NHAT 2026-06-03 - AI Optimization Sprint vong 5 - Baseline truoc toi uu

- Muc tieu vong 5: cai thien ca 3 profile `heuristic_defensive`, `heuristic_balanced`, `heuristic_aggressive` bang tinh chinh tham so va logic cham diem, khong them neural network, reinforcement learning, minimax hoac lookahead.
- Giu nguyen `RandomAI` va `RuleBasedAI` lam baseline so sanh cong bang.
- Baseline chinh lay tu `logs/experiments/ai_comparison_balanced_30.md`, dieu kien: `30 tran / AI`, player `balanced`, seed `42`, map `fixed_lane`.
- So lieu truoc toi uu:

| AI profile | Win rate | AI HP avg | Damage vao Player Base | Resource Eff | Attack avg | Defense avg | Decision ms avg |
|---|---:|---:|---:|---:|---:|---:|---:|
| `heuristic_defensive` | 43.3% | 377.5 | 113.3 | 0.024 | 87.8 | 4.9 | 0.4135 |
| `heuristic_balanced` | 16.7% | 340.3 | 118.1 | 0.025 | 100.5 | 4.0 | 0.3652 |
| `heuristic_aggressive` | 0.0% | 248.3 | 118.1 | 0.026 | 121.0 | 0.0 | 0.2644 |

- Gia thuyet toi uu: `heuristic_balanced` va `heuristic_aggressive` da gay damage tot nhung phong thu chua du, dac biet khi AI HP thap hoac lane co nguy co; can them "phanh an toan" cho tan cong va tang diem xay/nang cap thap trong tinh huong nguy hiem.
- Tieu chi chap nhan: `heuristic_balanced` win rate >= 30% va damage >= 100; `heuristic_aggressive` win rate >= 10% va damage >= 100; `heuristic_defensive` khong thap hon baseline 43.3%, uu tien tang len >= 50%.

---

## CAP NHAT 2026-06-03 - AI Optimization Sprint vong 5 - Ket qua sau toi uu

- Da tinh chinh `src/ai/heuristic_evaluator.py`, tap trung vao tham so va logic cham diem:
  - `defensive`: giu uu tien phong thu, them diem xay/nang cap khi HP duoi 90% hoac lane co rui ro; chi phan cong manh hon khi an toan va du tai nguyen.
  - `balanced`: tang diem phong thu khi HP/lane nguy hiem; giam diem gui quan khi co nguy co thung lane toan cuc.
  - `aggressive`: them "phanh an toan" dua tren HP AI va nguy co lane toan cuc, giup AI van xay/nang cap thap khi bi ep.
- Smoke test da chay thanh cong:
  - `python simulate.py heuristic balanced -n 3`
  - `python simulate.py heuristic defensive -n 3`
  - `python simulate.py heuristic aggressive -n 3`
- Kiem chung chinh da chay lai voi cung seed `42`:
  - `python simulate.py --experiment -n 30 --player balanced --seed 42`
  - `python simulate.py --experiment -n 10 --player defensive --seed 42`
  - `python simulate.py --experiment -n 10 --player early_attacker --seed 42`
  - `python simulate.py --experiment -n 10 --player random --seed 42`
- Ket qua chinh sau toi uu tai `logs/experiments/ai_comparison_balanced_30.md`:

| AI profile | Win truoc | Win sau | AI HP truoc | AI HP sau | Damage truoc | Damage sau | Defense truoc | Defense sau | Decision ms sau |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `heuristic_defensive` | 43.3% | 46.7% | 377.5 | 377.8 | 113.3 | 113.3 | 4.9 | 10.0 | 0.2034 |
| `heuristic_balanced` | 16.7% | 56.7% | 340.3 | 372.2 | 118.1 | 117.7 | 4.0 | 6.2 | 0.1867 |
| `heuristic_aggressive` | 0.0% | 20.0% | 248.3 | 350.7 | 118.1 | 118.1 | 0.0 | 5.1 | 0.1840 |

- Danh gia theo tieu chi chap nhan:
  - `heuristic_balanced`: DAT, win rate tang tu 16.7% len 56.7%, damage van >= 100.
  - `heuristic_aggressive`: DAT, win rate tang tu 0.0% len 20.0%, damage van >= 100.
  - `heuristic_defensive`: DAT, khong tut baseline, tang nhe tu 43.3% len 46.7%; chua dat muc uu tien 50% nhung da cai thien defense count ro.
  - Decision time trung binh cua cac heuristic profile van < 1ms, du tot cho realtime.
- Ket qua cac kich ban phu sau toi uu:
  - Player `defensive` 10 tran: `heuristic_defensive` 100%, `heuristic_balanced` 100%, `heuristic_aggressive` 0%.
  - Player `early_attacker` 10 tran: ca 3 heuristic profile deu dat 100%.
  - Player `random` 10 tran: ca 3 heuristic profile van 0%, nhung damage/base va AI HP cua `heuristic_aggressive` tot hon truoc; day la kich ban can tiep tuc phan tich neu con thoi gian.
- Ket luan vong 5: toi uu tham so da tang kha nang chien thang trong kich ban chinh ma khong lam mat damage tan cong. Tradeoff con lai la `heuristic_aggressive` van yeu khi gap player `defensive`, va tat ca heuristic profile van kho thang player `random` trong batch phu; nen dua hai diem nay vao phan han che/huong phat trien.

---

## CAP NHAT 2026-06-03 - AI Optimization Sprint vong 6 - Chon lane va wave tan cong

- Muc tieu vong 6: bo sung them 4 dau muc cai thien sau khi batch 100 tran cho thay `heuristic_aggressive` tan cong nhieu nhung chua gay damage vuot troi:
  - Cai thien chon lane tan cong dua tren hieu qua thuc te trong tran.
  - Khuyen khich wave co chu y thay vi gui quan rai rac.
  - Cai thien rieng profile `heuristic_aggressive`.
  - Ghi them ket qua 100 tran vao bao cao tien do.
- Da tinh chinh `src/ai/heuristic_evaluator.py`:
  - Them logic thuong lane da tung chuyen hoa attack thanh damage vao Player Base.
  - Phat lane bi spam nhieu nhung khong gay damage.
  - Tang diem wave lon khi lane co `attack_opportunity` tot hoac da tung gay damage.
  - Dieu chinh `heuristic_aggressive` uu tien `FAST` wave hon, giam bot `SWARM`/`TANK` khi lane chua co ap luc san.
- Smoke test da chay:
  - `python simulate.py heuristic balanced -n 3`
  - `python simulate.py heuristic aggressive -n 3`
  - `python simulate.py heuristic defensive -n 3`
- Tuning nhanh `10 tran / AI`, player `balanced`, seed `42`:

| AI profile | Win rate | AI HP avg | Damage vao Player Base | Resource Eff | Attack avg | Defense avg |
|---|---:|---:|---:|---:|---:|---:|
| `heuristic_defensive` | 70.0% | 388.5 | 120.8 | 0.025 | 84.6 | 9.4 |
| `heuristic_balanced` | 70.0% | 392.0 | 123.4 | 0.026 | 103.3 | 4.1 |
| `heuristic_aggressive` | 30.0% | 354.0 | 123.4 | 0.026 | 99.5 | 5.0 |

- Kiem chung lon `100 tran / AI`, player `balanced`, seed `42`, ket qua tai `logs/experiments/ai_comparison_balanced_100.*`:

| AI profile | Win rate | AI HP avg | Damage vao Player Base | Resource Eff | Attack avg | Defense avg | Lane tan cong chinh | Lane gay damage tot nhat | Decision ms avg |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `random_balanced` | 3.0% | 323.9 | 20.0 | 0.004 | 94.3 | 9.6 | 0 | 2 | 0.0491 |
| `rule_based_balanced` | 0.0% | 256.4 | 39.6 | 0.009 | 89.1 | 1.2 | 0 | 1 | 0.0160 |
| `heuristic_defensive` | 46.0% | 390.1 | 97.8 | 0.021 | 83.3 | 9.2 | 2 | 2 | 0.2640 |
| `heuristic_balanced` | 48.0% | 393.0 | 104.2 | 0.022 | 100.0 | 5.0 | 2 | 2 | 0.2381 |
| `heuristic_aggressive` | 17.0% | 356.2 | 104.3 | 0.022 | 97.6 | 4.9 | 2 | 2 | 0.2721 |

- Phan tich hanh vi sau vong 6:
  - Logic chon lane co tac dung ro ve mat hanh vi: `heuristic_balanced` va `heuristic_aggressive` deu chuyen lane tan cong chinh ve lane 2, trung voi lane gay damage tot nhat.
  - `heuristic_balanced` tang nhe trong batch 100 tu 47.0% len 48.0%, AI HP avg tang tu 388.2 len 393.0.
  - `heuristic_aggressive` giu win rate 17.0%, damage 104.3 gan nhu khong doi, nhung unit mix tot hon: tang uu tien `FAST` va giam `TANK` so voi truoc.
  - `heuristic_aggressive` van chua vuot `balanced` vi tan cong nhieu hon khong dong nghia voi quan cham duoc can cu; neu bi thap chan giua duong thi base damage khong tang.
  - Decision time trung binh van < 1ms, nhung max decision time cua `heuristic_aggressive` co spike 19.4484ms trong batch 100; can theo doi neu tiep tuc them scoring phuc tap.
- Ket luan vong 6: da them duoc co che chon lane va wave tan cong co giai thich duoc. Ket qua chien thang khong tang manh cho `aggressive`, nhung bao cao co them bang chung ve han che that: can lookahead ngan han hoac co che phoi hop wave phuc tap hon neu muon AI tan cong vuot len ro ret.
