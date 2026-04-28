# Báo cáo trình bày ý tưởng bài tập lớn

> Môn học: Nhập môn Trí tuệ nhân tạo  
> Nhóm: Trường Giang - Bình An  
> Trạng thái: Bản trình bày tiến độ/ý tưởng để báo cáo với giáo viên  
> Ngày chuẩn bị: 2026-04-28

---

## 1. Tên đề tài

**Thiết kế tác tử thông minh cho game thủ thành đối kháng người - AI trong môi trường 2D đơn giản**

Tên ngắn khi trình bày:

**Game thủ thành đối kháng người - AI sử dụng Heuristic Agent**

Trong đó:

- `Agent` (tác tử): AI đóng vai trò là một người chơi đối kháng với người chơi thật.
- `Heuristic` (kinh nghiệm/ước lượng nhanh): AI dùng các chỉ số như máu căn cứ, tài nguyên, số tháp, số quân, độ nguy hiểm của lane để ra quyết định.

---

## 2. Thành viên tham gia

| Thành viên | Vai trò chính | Công việc phụ |
|---|---|---|
| Trường Giang | Game engine, gameplay, giao diện demo | Tích hợp hệ thống, kiểm thử game, chuẩn bị demo |
| Bình An | AI, thuật toán, thực nghiệm, báo cáo số liệu | Thiết kế chỉ số đánh giá, chạy mô phỏng, viết báo cáo AI |

---

## 3. Phân chia công việc

### 3.1. Trường Giang

Phụ trách phần game chạy được:

- Xây dựng màn chơi 2D dạng 3 lane.
- Xây hệ thống căn cứ người chơi và căn cứ AI.
- Xây hệ thống tháp phòng thủ.
- Xây hệ thống quân tấn công.
- Xử lý combat: tháp bắn quân, quân đi tới căn cứ gây sát thương.
- Xây giao diện Pygame để người chơi có thể thao tác.
- Tích hợp AI vào vòng lặp game.

### 3.2. Bình An

Phụ trách phần AI và đánh giá:

- Mô hình hóa bài toán theo `Agent` (tác tử), `Environment` (môi trường), `State` (trạng thái), `Action` (hành động).
- Xây các loại AI:
  - `Random AI` (AI chọn ngẫu nhiên).
  - `Rule-based AI` (AI dựa trên luật).
  - `Heuristic AI` (AI dùng hàm đánh giá).
- Thiết kế `Utility Function` (hàm đánh giá độ tốt của hành động).
- Chạy `Batch Simulation` (mô phỏng nhiều trận tự động).
- Ghi log và lập bảng so sánh kết quả.
- Chuẩn bị phần báo cáo thuật toán và thực nghiệm.

### 3.3. Phối hợp chung

- Cả hai cùng thống nhất cấu trúc `GameState` (trạng thái trận đấu).
- Cả hai cùng kiểm thử gameplay để đảm bảo AI và game hoạt động đúng.
- Cả hai cùng chuẩn bị slide, báo cáo và kịch bản demo cuối kỳ.

---

## 4. Nội dung dự định làm

Nhóm dự định xây dựng một game thủ thành đối kháng 2D đơn giản, trong đó người chơi đấu với AI.

### 4.1. Nghiệp vụ gameplay

Game có hai bên:

- Người chơi.
- AI.

Mỗi bên có một căn cứ cần bảo vệ. Trận đấu diễn ra trên bản đồ 3 lane. Người chơi và AI có thể:

- Xây tháp phòng thủ.
- Nâng cấp tháp.
- Gửi quân tấn công căn cứ đối phương.
- Quản lý tài nguyên.
- Chọn lane để phòng thủ hoặc tấn công.

Quân sẽ di chuyển theo lane. Nếu quân đi tới căn cứ đối phương, căn cứ sẽ mất máu. Trận đấu kết thúc khi một căn cứ bị phá hoặc hết thời gian.

### 4.2. Mục tiêu bài toán AI

Mục tiêu chính không phải làm một game thương mại hoàn chỉnh, mà là xây dựng một mô phỏng để thể hiện các nội dung của môn Nhập môn Trí tuệ nhân tạo.

AI cần tự ra quyết định:

- Khi nào nên tấn công.
- Khi nào nên phòng thủ.
- Nên gửi loại quân nào.
- Nên đánh lane nào.
- Nên xây hoặc nâng cấp tháp ở đâu.
- Nên dùng tài nguyên ngay hay tiết kiệm.

### 4.3. Các thuật toán/phương pháp AI ứng dụng

| Thuật toán/phương pháp | Nghĩa tiếng Việt | Ứng dụng trong đề tài |
|---|---|---|
| `Random Policy` | Chính sách chọn ngẫu nhiên | Làm AI cơ sở yếu nhất để so sánh |
| `Rule-based Agent` | Tác tử dựa trên luật | AI dùng các luật if-else đơn giản |
| `Heuristic Agent` | Tác tử dùng kinh nghiệm/ước lượng nhanh | AI chính của đề tài |
| `State Abstraction` | Rút gọn trạng thái | Từ GameState đầy đủ rút ra chỉ số từng lane |
| `Candidate Action Generation` | Sinh danh sách hành động ứng viên | AI chỉ xét các hành động hợp lý, không xét toàn bộ khả năng |
| `Utility Function` | Hàm đánh giá độ tốt | Chấm điểm từng hành động |
| `Greedy Action Selection` | Chọn hành động có điểm cao nhất hiện tại | AI chọn hành động tốt nhất ở thời điểm đang xét |
| `Batch Simulation` | Mô phỏng nhiều trận tự động | Chạy nhiều trận để đánh giá AI bằng số liệu |

Pipeline (quy trình) ra quyết định của AI:

```text
GameState
-> State Abstraction
-> Candidate Action Generation
-> Utility Function
-> Greedy Action Selection
-> Execute Action
```

Giải thích dễ hiểu:

AI đọc trạng thái trận đấu, rút gọn thành các chỉ số dễ hiểu, tạo danh sách hành động có thể làm, chấm điểm từng hành động, rồi chọn hành động có điểm cao nhất.

---

## 5. Kết quả mong muốn

Nhóm mong muốn đạt được các kết quả sau:

- Có một demo game chạy được.
- Người chơi có thể đấu với AI.
- AI có thể tự tấn công, phòng thủ và quản lý tài nguyên.
- Có ít nhất 3 loại AI để so sánh:
  - AI ngẫu nhiên.
  - AI luật đơn giản.
  - AI heuristic.
- Có số liệu thực nghiệm để chứng minh AI heuristic tốt hơn baseline (mốc so sánh ban đầu).
- Có báo cáo giải thích được:
  - AI quan sát gì.
  - AI có hành động nào.
  - AI chấm điểm hành động ra sao.
  - AI nào hiệu quả hơn qua số liệu.

Kết quả kỳ vọng cuối kỳ:

> Một bản game mô phỏng học thuật có AI rõ ràng, có demo, có số liệu đánh giá và có báo cáo phân tích thuật toán.

---

## 6. Nội dung đã làm đến giờ

### 6.1. Phần phân tích và tài liệu

Nhóm đã chuẩn bị bộ tài liệu phân tích gồm:

- Phân tích tổng hợp đề tài.
- Phân tích gameplay.
- Mô hình hóa AI.
- Phân tích thuật toán AI.
- Thiết kế kiến trúc hệ thống.
- Thiết kế chỉ số đánh giá.
- Lộ trình, rủi ro và sản phẩm bàn giao.

### 6.2. Phần game

Đã hoàn thành MVP game:

- Game 2D dạng 3 lane.
- Có căn cứ người chơi và căn cứ AI.
- Có hệ thống tài nguyên.
- Có 3 loại tháp.
- Có 3 loại quân.
- Có xây tháp, nâng cấp tháp, gửi quân.
- Có điều kiện thắng/thua.
- Có giao diện Pygame để chơi thử.

### 6.3. Phần AI

Đã xây dựng các AI:

- `Random AI` (AI chọn ngẫu nhiên).
- `Rule-based AI` (AI dựa trên luật đơn giản).
- `Heuristic AI` (AI dùng hàm đánh giá).

`Heuristic AI` hiện có 3 phong cách:

- `Defensive` (phòng thủ).
- `Balanced` (cân bằng).
- `Aggressive` (tấn công).

### 6.4. Phần thực nghiệm

Đã chạy mô phỏng nhiều trận để so sánh AI.

Kết quả mới nhất với 30 trận cho mỗi AI, trong kịch bản người chơi tự động cân bằng:

| Loại AI | Tỷ lệ thắng | Máu nhà AI trung bình | Sát thương vào nhà người chơi | Hiệu quả tài nguyên |
|---|---:|---:|---:|---:|
| AI ngẫu nhiên | 0.0% | 302.2 | 19.6 | 0.004 |
| AI luật đơn giản | 0.0% | 255.2 | 44.8 | 0.010 |
| AI phòng thủ | 43.3% | 377.8 | 113.3 | 0.024 |
| AI cân bằng | 3.3% | 292.8 | 118.1 | 0.026 |
| AI tấn công | 0.0% | 248.3 | 118.1 | 0.026 |

Nhận xét:

- AI heuristic đã gây sát thương vào căn cứ người chơi cao hơn AI luật đơn giản.
- AI phòng thủ có tỷ lệ thắng cao nhất.
- AI cân bằng và AI tấn công gây áp lực tốt hơn lên căn cứ người chơi.
- Tất cả AI đều ra quyết định đủ nhanh để chạy trong game real-time (thời gian thực).

---

## 7. Khó khăn gặp phải

### 7.1. Khó khăn về cân bằng gameplay

Nếu chỉ chỉnh cho AI tấn công nhiều, AI có thể gây sát thương cao nhưng lại dễ thua vì bỏ phòng thủ.

Nếu chỉnh AI phòng thủ quá nhiều, AI sống lâu nhưng trận đấu kém hấp dẫn và khó phá nhà người chơi.

### 7.2. Khó khăn về chỉ số đánh giá

Ban đầu nhóm phát hiện chỉ số sát thương bị cộng lẫn giữa:

- Sát thương lên quân.
- Sát thương lên căn cứ.

Sau đó nhóm đã tách lại để kết quả báo cáo chính xác hơn.

### 7.3. Khó khăn về thiết kế AI

AI không chỉ cần gửi nhiều quân mà phải gửi đúng loại quân, đúng lane, đúng thời điểm.

Ví dụ:

- Gửi quân rẻ quá nhiều chưa chắc hiệu quả.
- Gửi quân nhanh vào lane yếu có thể gây sát thương tốt hơn.
- AI tấn công mạnh nhưng không phòng thủ thì vẫn dễ thua.

### 7.4. Khó khăn về phạm vi

Nếu thêm quá nhiều thứ như multiplayer (nhiều người chơi online), đồ họa 3D, học sâu hoặc học tăng cường phức tạp thì sẽ vượt quá phạm vi bài tập lớn.

Vì vậy nhóm đang ưu tiên bản mô phỏng đơn giản nhưng thể hiện rõ tư duy AI.

---

## 8. Kế hoạch đến cuối kỳ

### Giai đoạn 1: Hoàn thiện lõi game và AI

Trạng thái: cơ bản đã hoàn thành.

- Game chạy được.
- Người chơi đấu với AI được.
- Có nhiều loại AI.
- Có log và số liệu thực nghiệm.

### Giai đoạn 2: Hoàn thiện báo cáo và slide

Cần làm tiếp:

- Viết báo cáo chính thức.
- Chuẩn hóa bảng số liệu thực nghiệm.
- Giải thích rõ `Utility Function` (hàm đánh giá độ tốt).
- Giải thích rõ sự khác nhau giữa các AI.
- Chuẩn bị slide trình bày.

### Giai đoạn 3: Cải thiện demo

Cần làm tiếp:

- Cải thiện giao diện để dễ nhìn hơn.
- Thêm màn hình kết quả sau trận.
- Hiển thị một số chỉ số AI trong lúc demo.
- Chuẩn bị kịch bản chơi thử trong 3-5 phút.

### Giai đoạn 4: Phần mở rộng nếu còn thời gian

Nếu còn thời gian, nhóm có thể thêm:

- `1-step Lookahead` (nhìn trước 1 bước): AI thử ước lượng kết quả sau một hành động trước khi chọn.
- `Minimax` (thuật toán đối kháng): chỉ thêm ở mức nhỏ nếu đủ thời gian.
- Biểu đồ kết quả thực nghiệm.

Nhóm sẽ không làm:

- Multiplayer online (nhiều người chơi qua mạng).
- Đồ họa 3D.
- Hệ thống tài khoản.
- Deep Learning (học sâu).
- Reinforcement Learning phức tạp (học tăng cường phức tạp).

---

## 9. Kịch bản trình bày ngắn gọn

Nhóm có thể trình bày theo thứ tự sau:

1. Giới thiệu đề tài: game thủ thành đối kháng người - AI.
2. Nêu mục tiêu: không làm game thương mại, tập trung mô hình hóa AI.
3. Giải thích gameplay: 2 căn cứ, 3 lane, xây tháp, gửi quân, quản lý tài nguyên.
4. Giới thiệu AI: Random, Rule-based, Heuristic.
5. Giải thích AI chính: đọc GameState, rút gọn lane, sinh hành động, chấm điểm, chọn hành động tốt nhất.
6. Trình bày kết quả đã làm: game chạy được, AI hoạt động, có log và số liệu.
7. Nêu khó khăn: cân bằng công-thủ, đo chỉ số đúng, tránh mở rộng quá mức.
8. Nêu kế hoạch cuối kỳ: hoàn thiện báo cáo, polish demo, có thể thêm lookahead nếu còn thời gian.

---

## 10. Lời trình bày gợi ý

> Đề tài của nhóm em là thiết kế tác tử thông minh cho game thủ thành đối kháng người - AI trong môi trường 2D đơn giản. Game có hai căn cứ, người chơi và AI cùng xây tháp, gửi quân theo lane và quản lý tài nguyên. Mục tiêu chính của nhóm không phải xây game thương mại hoàn chỉnh, mà là mô hình hóa bài toán AI và chứng minh AI có thể ra quyết định hợp lý.

> Về AI, nhóm em xây dựng ba mức: Random AI, Rule-based AI và Heuristic AI. AI chính là Heuristic Agent, tức là tác tử dùng hàm đánh giá. AI quan sát GameState, rút gọn trạng thái từng lane, sinh ra các hành động ứng viên như xây tháp, nâng cấp tháp, gửi quân, sau đó chấm điểm bằng Utility Function và chọn hành động có điểm cao nhất bằng Greedy Action Selection.

> Hiện tại nhóm đã có game chạy được, có giao diện demo, có nhiều loại tháp và quân, có điều kiện thắng thua, có log và batch simulation để đo kết quả. Kết quả thực nghiệm ban đầu cho thấy Heuristic AI gây sát thương vào căn cứ người chơi tốt hơn AI ngẫu nhiên và AI luật đơn giản ở một số chỉ số quan trọng.

> Khó khăn chính của nhóm là cân bằng giữa tấn công và phòng thủ. Nếu AI tấn công quá nhiều thì dễ mất nhà, còn nếu phòng thủ quá nhiều thì trận đấu kém hấp dẫn. Trong thời gian tới nhóm sẽ hoàn thiện báo cáo, chuẩn hóa thực nghiệm, cải thiện demo và nếu còn thời gian sẽ bổ sung lookahead một bước để mở rộng phần thuật toán.

