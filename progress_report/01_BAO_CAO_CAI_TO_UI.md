# Báo cáo cải tổ UI và asset pipeline

> Ngày cập nhật: 2026-04-28  
> Phạm vi: UI/UX Pygame, visual polish, asset pipeline  
> Trạng thái: Hoàn thành vòng cải tổ UI đầu tiên

## 1. Mục tiêu

Mục tiêu của vòng này là nâng giao diện từ mức MVP kỹ thuật lên mức có thể dùng để demo thuyết phục hơn trước khi tiếp tục đi sâu vào AI và thuật toán.

Trọng tâm:

- Làm giao diện giống một bảng điều khiển chiến thuật.
- Giữ gameplay và AI core ổn định.
- Chuẩn bị pipeline asset để sau này có thể thay sprite/icon bằng file ảnh thật.
- Kiểm tra lại bằng screenshot render thay vì chỉ sửa code cảm tính.

## 2. Skill và quy trình đã áp dụng

Các skill trong `.codex` đã được đọc và ứng dụng ở mức phù hợp với dự án hiện tại:

- `imagegen`: dùng làm định hướng asset pipeline. Chưa generate bitmap bằng tool ở vòng này vì cần ổn định layout trước; thay vào đó đã tạo fallback procedural để sẵn sàng thay bằng asset thật.
- `screenshot`: dùng theo tinh thần visual QA. Dự án Pygame được kiểm tra bằng cách render trực tiếp surface ra ảnh.
- `figma` và `figma-implement-design`: đã xem quy trình, nhưng chưa dùng vì hiện chưa có Figma URL hoặc mockup Figma.

Kết luận: với game Pygame desktop hiện tại, workflow đúng là `layout -> component -> asset pipeline -> visual QA -> bitmap asset pass`.

## 3. Thay đổi đã thực hiện

### 3.1. Tách design token và widget

Đã thêm:

- `src/ui/theme.py`
- `src/ui/widgets.py`

Vai trò:

- `theme.py`: quản lý màu sắc, spacing, kích thước layout, font token.
- `widgets.py`: chứa `Button`, `draw_panel`, `draw_bar`, `draw_text`.

Lợi ích:

- UIManager không còn chứa toàn bộ logic vẽ cơ bản.
- Dễ đổi theme và polish giao diện.
- Dễ mở rộng button có icon, trạng thái selected, disabled, hover.

### 3.2. Sửa layout tổng thể

Đã cập nhật `src/systems/map_manager.py`:

- `SCREEN_WIDTH = 1280`
- `SCREEN_HEIGHT = 760`
- `BASE_Y = 315`
- `LANE_Y_POSITIONS = [155, 315, 475]`
- `TOWER_SLOT_SPACING = 118`

Kết quả:

- Lane 3 không còn bị panel dưới che.
- Không gian battlefield rộng và cân đối hơn.
- Base và lane nằm rõ trong vùng chiến đấu.

### 3.3. Viết lại UIManager theo hướng tactical console

Đã thay đổi lớn trong `src/ui/ui_manager.py`:

- Top HUD mới: tên game, AI profile, timer, HP Player/AI.
- Battlefield mới: nền grid, lane texture, risk meter, slot rõ hơn.
- Command deck mới: nhóm tháp, quân, lane, hành động, tài nguyên, thống kê.
- AI Debug panel mới: last action, score, decision time, risk/opportunity từng lane.
- Game over overlay mới: rõ ràng và phù hợp demo.

### 3.4. Thêm asset pipeline

Đã thêm:

- `src/ui/assets.py`
- `assets/README.md`
- thư mục `assets/ui/`
- thư mục `assets/icons/`
- thư mục `assets/bases/`

AssetManager hiện hỗ trợ:

- Load asset từ file nếu có.
- Tự tạo fallback procedural nếu file chưa tồn tại.
- Cache surface để tránh load/tạo lại nhiều lần.

Tên file asset đã quy ước:

- `assets/icons/tower_fast.png`
- `assets/icons/tower_heavy.png`
- `assets/icons/tower_balanced.png`
- `assets/icons/unit_fast.png`
- `assets/icons/unit_tank.png`
- `assets/icons/unit_swarm.png`
- `assets/bases/player_base.png`
- `assets/bases/ai_base.png`

### 3.5. Gắn asset vào UI

Đã gắn:

- Icon tháp/quân vào button.
- Icon tháp trên battlefield.
- Icon quân trên battlefield.
- Sprite căn cứ Player/AI.
- Background và lane texture procedural.

Kết quả:

- Game bớt giống debug tool.
- Button dễ nhận diện hơn.
- Trận đấu có cảm giác trực quan hơn.

### 3.6. Bổ sung dữ liệu AI cho debug UI

Đã cập nhật `src/engine/game_engine.py`:

- `last_ai_action`
- `last_ai_score`
- `last_ai_decision_ms`

Kết quả:

- AI Debug panel có dữ liệu thật để giải thích trong demo.
- Có thể nói rõ AI vừa chọn hành động gì, điểm bao nhiêu, tính trong bao lâu.

## 4. Kiểm thử đã chạy

### 4.1. Compile

Lệnh:

```powershell
python -m compileall main.py simulate.py src
```

Kết quả:

- Thành công.
- Không phát hiện lỗi syntax/import.

### 4.2. Simulation nhanh

Lệnh:

```powershell
$env:PYTHONIOENCODING='utf-8'; python simulate.py heuristic balanced -n 1
```

Kết quả:

- Simulation chạy hoàn tất.
- Game logic và AI không bị ảnh hưởng bởi refactor UI.

Kết quả mẫu:

```text
Winner: AI
Duration: 271.2s
Player HP: 0
AI HP: 32
AI Actions: Attack=106, Defense=3, Economy=0
Avg decision time: khoảng 0.21 ms
```

### 4.3. Visual QA

Đã render ảnh kiểm tra tại:

- `logs/asset_polish_screenshots/01_initial_asset_pass.png`
- `logs/asset_polish_screenshots/02_after_build_asset_pass.png`
- `logs/asset_polish_screenshots/03_combat_asset_pass.png`
- `logs/asset_polish_screenshots/04_debug_asset_pass.png`
- `logs/asset_polish_screenshots/05_game_over_asset_pass.png`

Đánh giá nhanh:

- Layout không còn bị đè.
- Lane đọc được rõ.
- Button có icon và trạng thái disabled/selected.
- Debug panel có giá trị thuyết trình.
- Game over overlay rõ.
- Vòng range chỉ hiện khi hover/debug, giảm rối màn hình.

## 5. Đánh giá hiện trạng

### Điểm đã tốt hơn

- UI có phong cách thống nhất hơn.
- Màn hình demo nhìn giống game chiến thuật hơn.
- Player đọc tài nguyên, timer, HP, lane và lựa chọn dễ hơn.
- Debug AI hỗ trợ tốt hơn cho phần báo cáo môn AI.
- Asset pipeline đã sẵn sàng cho ảnh thật.

### Điểm còn hạn chế

- Asset hiện tại vẫn là procedural fallback, chưa phải bitmap AI-generated/polished art.
- Một số text tiếng Việt trong terminal Windows vẫn có thể bị lỗi mã hóa nếu không dùng UTF-8.
- Chưa có animation hit flash/base damage.
- Chưa có sound feedback.
- Chưa sửa vấn đề thống kê damage đang gộp damage lên unit và damage lên base.

## 6. Khuyến nghị bước tiếp theo

Thứ tự nên làm tiếp:

1. Sửa logger damage để tách `damage_to_units` và `damage_to_base`.
2. Chạy batch comparison lại sau khi sửa thống kê.
3. Tinh chỉnh heuristic `balanced` và `aggressive`.
4. Nếu muốn polish UI thêm, dùng `imagegen` tạo asset PNG thật cho icon/base/background theo quy ước trong `assets/README.md`.
5. Chụp lại bộ ảnh demo cuối cùng để đưa vào báo cáo và slide.

## 7. Kết luận

Vòng cải tổ UI đầu tiên đã hoàn thành đúng mục tiêu: giao diện sạch hơn, chiến thuật hơn, có asset pipeline, có ảnh QA và không phá game logic. Dự án hiện đã đủ nền để tiếp tục xử lý phần AI/đánh giá một cách nghiêm túc hơn.
