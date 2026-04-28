# Bao cao thuc nghiem AI - vong 1

> Ngay cap nhat: 2026-04-28  
> Pham vi: do luong AI, chuan hoa logger, chay batch simulation  
> Trang thai: da co bo so lieu ban dau de dua vao bao cao

## 1. Muc tieu

Vong nay chuyen trong tam tu giao dien sang do luong AI. Muc tieu la co so lieu dinh luong de tra loi cac cau hoi:

- AI nao thang nhieu hon?
- AI nao phong thu tot hon?
- AI nao gay damage vao can cu doi phuong tot hon?
- AI nao dung tai nguyen hieu qua hon?
- Thoi gian ra quyet dinh co du nhanh cho game real-time khong?

## 2. Thay doi da thuc hien

### 2.1. Lam sach metric damage

Truoc do, `player_damage_dealt` va `ai_damage_dealt` gom ca:

- damage thap gay len linh/quai;
- damage linh/quai gay len can cu.

Dieu nay lam chi so `damage_to_player_base` va `resource_efficiency_ai` bi phong dai. Da tach them cac metric:

- `player_base_damage_dealt`
- `ai_base_damage_dealt`
- `player_unit_damage_dealt`
- `ai_unit_damage_dealt`

Logger chinh thuc hien dung `*_base_damage_dealt` de tinh damage vao can cu va hieu qua tai nguyen.

### 2.2. Bo sung batch experiment runner

Da nang cap `simulate.py` va `src/simulation/simulation.py` de ho tro:

- chay so sanh tat ca AI bang `--experiment`;
- chon so tran bang `-n`;
- chon seed bang `--seed`;
- chon chien luoc nguoi choi tu dong bang `--player`;
- xuat ket qua ra JSON, CSV, Markdown.

Lenh thuc nghiem da dung:

```powershell
$env:PYTHONIOENCODING='utf-8'; python simulate.py --experiment -n 20 --player balanced --seed 42
```

File ket qua:

- `logs/experiments/ai_comparison_balanced_20.json`
- `logs/experiments/ai_comparison_balanced_20.csv`
- `logs/experiments/ai_comparison_balanced_20.md`

### 2.3. Chinh nhe heuristic AI

Da sua bo sinh action ung vien de AI heuristic co the can nhac nhieu loai thap hon, thay vi chi them mot loai thap dau tien moi lane.

Da them opening-defense bonus: lane chua co thap AI se duoc cong diem phong thu. Muc tieu la giup profile defensive/balanced the hien ro hon, khong chi spam quan.

## 3. Thiet lap thuc nghiem

| Thiet lap | Gia tri |
|---|---:|
| So tran moi AI | 20 |
| Seed | 42 |
| Map | fixed_lane |
| Player tu dong | balanced |
| Thoi gian toi da moi tran | 300 giay |
| AI duoc so sanh | random, rule_based, heuristic_defensive, heuristic_balanced, heuristic_aggressive |

Luu y: `balanced AutoPlayer` la doi thu test co kiem soat, chua phai nguoi choi that.

## 4. Ket qua tong hop

| AI Profile | Win % | Draw % | AI HP TB | Damage vao Player Base TB | Damage vao AI Base TB | Eff AI | Attack TB | Defense TB | Decision ms TB |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| random_balanced | 0.0 | 0.0 | 394.5 | 15.85 | 105.5 | 0.0034 | 81.0 | 20.1 | 0.0717 |
| rule_based_balanced | 0.0 | 0.0 | 254.25 | 45.2 | 245.75 | 0.0099 | 87.0 | 2.15 | 0.0213 |
| heuristic_defensive | 20.0 | 50.0 | 498.0 | 2.25 | 2.0 | 0.0008 | 82.7 | 3.0 | 0.3307 |
| heuristic_balanced | 0.0 | 0.0 | 428.0 | 3.75 | 72.0 | 0.0014 | 83.45 | 3.0 | 0.3087 |
| heuristic_aggressive | 0.0 | 0.0 | 359.75 | 3.75 | 140.25 | 0.0010 | 118.0 | 3.0 | 0.3061 |

## 5. Nhan xet ban dau

### 5.1. Dieu da tot

- Logger da do dung damage vao can cu, khong con nham voi damage len linh.
- Batch runner da du de lap bang thuc nghiem cho bao cao.
- Thoi gian ra quyet dinh trung binh rat thap, tat ca AI deu chay du nhanh cho game real-time.
- Cac profile da bat dau co khac biet hanh vi: aggressive tan cong nhieu hon, defensive giu HP tot hon.

### 5.2. Van de phat hien

- AI heuristic hien phong thu tot hon tan cong, dac biet `heuristic_defensive` giu HP rat cao nhung gay damage vao can cu nguoi choi rat thap.
- `rule_based_balanced` dang gay damage vao can cu nguoi choi cao nhat trong batch nay, du thua ve HP cuoi tran.
- `heuristic_aggressive` tan cong nhieu nhat nhung khong tao du damage vao base, nghia la spam quan chua dong nghia voi hieu qua.
- Ket qua nay cho thay can tune utility function va/hoac logic chon loai quan/lane tan cong.

### 5.3. Ket luan thuc nghiem vong 1

Day la vong do luong nen muc tieu chinh khong phai lam AI manh ngay, ma la lam ro su that ve hanh vi AI. Sau khi sua metric, ta thay AI can duoc cai thien o kha nang tan cong can cu. Day la co so tot de tiep tuc tune heuristic mot cach co bang chung.

## 6. Viec nen lam tiep theo

1. Tune `HeuristicEvaluator._score_send_unit()` de AI tan cong dung lane va dung loai quan hieu qua hon.
2. Them chi so lane tan cong chinh va lane bi thung nhieu nhat vao logger.
3. Chay lai `--experiment -n 30` sau moi vong tune de so sanh.
4. Thu them cac player strategy: `random`, `early_attacker`, `defensive`.
5. Neu heuristic on dinh, moi can nhac them `1-step lookahead`.

---

## 7. Cap nhat vong 2 - tune tan cong va metric theo lane

> Ngay cap nhat: 2026-04-28  
> Muc tieu: tang kha nang tan cong cua Heuristic AI va them du lieu giai thich hanh vi theo lane/loai quan.

### 7.1. Thay doi da lam

- Them metric theo lane va loai quan:
  - `ai_attack_lane_counts`
  - `ai_unit_type_counts`
  - `ai_base_damage_by_lane`
  - `dominant_ai_attack_lane`
  - `most_effective_ai_damage_lane`
- Them metadata `quantity` cho hanh dong `SEND_UNIT` de AI co the gui wave nho 2-4 quan neu du tai nguyen.
- Cap nhat `GameEngine._execute_send_unit()` de spawn nhieu unit trong mot action neu action co `metadata.quantity`.
- Cap nhat `HeuristicEvaluator`:
  - uu tien lane phong thu yeu cua player;
  - thuong lane dang co ap luc san;
  - tang diem cho wave nho;
  - tang diem dung Tank khi lane co thap;
  - giam diem spam Swarm vao lane phong thu manh;
  - tach phong cach defensive/balanced/aggressive ro hon.

### 7.2. Ket qua chinh - player strategy balanced, 20 tran/AI

Lenh:

```powershell
$env:PYTHONIOENCODING='utf-8'; python simulate.py --experiment -n 20 --player balanced --seed 42
```

| AI Profile | Win % | AI HP TB | Damage vao Player Base TB | Eff AI | Attack TB | Defense TB | Lane tan cong chinh |
|---|---:|---:|---:|---:|---:|---:|---:|
| random_balanced | 0.0 | 301.5 | 20.3 | 0.004 | 94.4 | 8.4 | 0 |
| rule_based_balanced | 0.0 | 254.2 | 45.2 | 0.010 | 87.0 | 2.1 | 0 |
| heuristic_defensive | 0.0 | 362.0 | 26.8 | 0.006 | 89.2 | 3.0 | 1 |
| heuristic_balanced | 0.0 | 263.2 | 26.8 | 0.006 | 109.0 | 1.6 | 1 |
| heuristic_aggressive | 0.0 | 244.2 | 26.8 | 0.006 | 121.0 | 0.0 | 1 |

So voi vong 1, damage cua heuristic vao Player Base tang tu khoang `3.75` len `26.8` trong cung kich ban balanced. Tuy nhien, `rule_based` van gay damage vao base cao hon trong kich ban nay.

### 7.3. Kich ban phu

Da chay them:

```powershell
$env:PYTHONIOENCODING='utf-8'; python simulate.py --experiment -n 10 --player random --seed 42
$env:PYTHONIOENCODING='utf-8'; python simulate.py --experiment -n 10 --player early_attacker --seed 42
$env:PYTHONIOENCODING='utf-8'; python simulate.py --experiment -n 10 --player defensive --seed 42
```

Ket qua dang chu y:

- Voi `early_attacker`, tat ca AI deu thang 100%, cho thay player tan cong som nhung thieu phong thu se bi AI khai thac.
- Voi `defensive`, `heuristic_defensive` thang 90% va giu AI HP trung binh 475.5, the hien kha nang song sot va thang theo HP khi het gio.
- Voi `random`, `rule_based` gay damage base cao nhat, con heuristic balanced/aggressive tan cong nhieu nhung HP con thap, can tiep tuc can bang lai.

### 7.4. Ket luan vong 2

Vong 2 da cai thien AI heuristic ve kha nang tan cong va da co them metric giai thich hanh vi theo lane. Tuy nhien heuristic van chua toi uu trong kich ban player balanced: tan cong nhieu hon nhung hieu qua chua vuot rule-based. Dieu nay la co so tot cho bao cao vi cho thay qua trinh thuc nghiem phat hien han che that, khong chi trinh bay ket qua dep.

### 7.5. Viec nen lam tiep

1. Tune tiep `heuristic_balanced` de tang damage base nhung khong hy sinh HP qua nhieu.
2. Giam spam attack cua `heuristic_aggressive` bang cach uu tien wave dung thoi diem thay vi gui lien tuc.
3. Them mot AI `heuristic_lookahead_1` neu can diem nang cao, dung mo phong ngan 1 buoc de chon action.
4. Dua bang vong 2 vao bao cao thuc nghiem, nhan manh heuristic co kha nang giai thich va chay real-time.

---

## 8. Cap nhat vong 3 - tune heuristic vuot baseline rule-based

> Ngay cap nhat: 2026-04-28  
> Muc tieu: lam Heuristic AI vuot hoac it nhat ngang Rule-based trong kich ban player `balanced`.

### 8.1. Gia thuyet tune

Phan tich log vong 2 cho thay:

- `rule_based` gay damage base tot hon vi chu yeu gui `fast`.
- `heuristic_balanced` va `heuristic_aggressive` gui qua nhieu `swarm`, dac biet tap trung lane 1.
- `swarm` tao ap luc so dong nhung khong xuyen duoc phong thu tot bang `fast` trong map lane MVP hien tai.

Gia thuyet: Heuristic AI thua Rule-based khong phai vi thuat toan sai, ma vi utility dang thuong `swarm` qua nhieu va chua uu tien `fast wave` tren lane yeu.

### 8.2. Thay doi da lam

- Tang diem cho `FAST` khi lane co `enemy_tower_strength < 0.45`.
- Tang diem cho `FAST` khi lane co `attack_opportunity` cao.
- Tang bonus cho wave nhieu quan neu la `FAST`.
- Giam diem `SWARM` khi lane co phong thu manh.
- Giam nhe diem `SWARM` trong wave lon de tranh spam quan re.
- Giu `RuleBasedAI` va `RandomAI` nguyen trang thai lam baseline.

### 8.3. Ket qua chinh - player balanced, 30 tran/AI

Lenh:

```powershell
$env:PYTHONIOENCODING='utf-8'; python simulate.py --experiment -n 30 --player balanced --seed 42
```

| AI Profile | Win % | AI HP TB | Damage vao Player Base TB | Eff AI | Attack TB | Defense TB | Lane chinh | Decision ms TB |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| random_balanced | 0.0 | 302.2 | 19.6 | 0.004 | 94.6 | 8.5 | 0 | 0.1361 |
| rule_based_balanced | 0.0 | 255.2 | 44.8 | 0.010 | 87.9 | 1.8 | 0 | 0.0531 |
| heuristic_defensive | 43.3 | 377.8 | 113.3 | 0.024 | 89.9 | 2.9 | 2 | 0.6631 |
| heuristic_balanced | 3.3 | 292.8 | 118.1 | 0.026 | 107.0 | 1.8 | 1 | 0.4756 |
| heuristic_aggressive | 0.0 | 248.3 | 118.1 | 0.026 | 121.0 | 0.0 | 1 | 0.4299 |

### 8.4. Nhan xet

- Muc tieu vong 3 dat duoc: `heuristic_balanced` gay damage vao Player Base `118.1`, cao hon `rule_based` la `44.8`.
- `heuristic_balanced` co resource efficiency `0.026`, cao hon `rule_based` la `0.010`.
- `heuristic_defensive` co ty le thang cao nhat trong batch balanced: `43.3%`, do giu HP AI cao hon va van gay damage dang ke.
- `heuristic_aggressive` gay damage base cao nhung HP AI thap va khong phong thu, nen chua phai profile tot nhat.
- Decision time trung binh cua heuristic van du thap duoi 1ms. Mot so max decision time co outlier, nhung AI chi quyet dinh moi 2.5 giay nen van chap nhan duoc cho demo/bai tap lon.

### 8.5. Ket luan vong 3

Sau 3 vong do luong va tune, Heuristic AI da co bang chung tot hon baseline rule-based o muc damage base va resource efficiency trong kich ban `balanced`. Ket qua nay du tot de dua vao bao cao nhu minh chung cho pipeline:

`GameState -> LaneSummary -> candidate actions -> utility score -> greedy action selection`.

Khong nen tiep tuc tune thu cong qua lau. Buoc tiep theo nen la dong goi ket qua vao bao cao, hoac neu can diem nang cao thi them `1-step lookahead` nhu mot thuat toan mo rong.
