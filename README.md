# Triết học Mác – Lênin · Bộ 3 Slide Mở Đầu & Kinetic Morphing

Bộ slide chuẩn 16:9 gồm **Lời chào → Phân công nhiệm vụ 13 thành viên → Cảm ơn / Dẫn vào Chương 1**, được thiết kế mô phỏng kỹ thuật chuyển động đỉnh cao từ video tham chiếu *Tuyệt Kỹ PowerPoint*.

Deck sử dụng cơ chế **True Layer-by-Layer Kinetic Morphing**: mọi layer đều được định danh bằng cú pháp tiền tố `!!NAME` để ép PowerPoint nội suy chuyển động 1:1, kết hợp toạ độ chờ ngoài khung (off-canvas) giúp các khối chữ, bảng phân công và huy hiệu lướt vào/lướt ra mượt mà theo không gian vật lý 2D, không dùng hiệu ứng mờ nhạt (cross-fade) đơn điệu.

---

## 1. Danh sách file và sản phẩm bàn giao

| File / Thư mục | Định dạng | Vai trò & Hướng dẫn sử dụng |
|---|---|---|
| `Triet_hoc_Mac_Lenin_Loi_chao.pptx` | **PPTX (Chính thức)** | **File bài giảng chính** — đã nhúng toàn bộ 5 font tiếng Việt cao cấp, hiệu ứng Morph 2.0s đã cấu hình sẵn trong OpenXML. Mở lên và nhấn **F5** để trình chiếu ngay. |
| `preview_red/Triet_hoc_Mac_Lenin_Loi_chao.pdf` | **PDF (1080p)** | Bản xuất vector PDF nét căng dùng xem nhanh trên điện thoại hoặc nộp báo cáo trước cho giảng viên. |
| `preview_red/final_png/Slide1.PNG` | **PNG (1920×1080)** | Ảnh chụp thực tế Slide 1: Lời chào trang trọng & Tiêu đề chính luận. |
| `preview_red/final_png/Slide2.PNG` | **PNG (1920×1080)** | Ảnh chụp thực tế Slide 2: Bảng phân công 13 thành viên đầy đủ & Quote Lenin. |
| `preview_red/final_png/Slide3.PNG` | **PNG (1920×1080)** | Ảnh chụp thực tế Slide 3: Lời cảm ơn hoành tráng & Huy hiệu Chương 01. |
| `preview_red/morph_preview.mp4` | **MP4 Video** | Video xuất trực tiếp từ PowerPoint COM (15 giây) ghi lại toàn bộ chuyển động Morph thực tế giữa các slide. |
| `preview_red/morph_animation_sheet.jpg` | **Ảnh Contact Sheet** | Bảng phân rã 15 frame liên tiếp chứng minh cơ chế chuyển động từng layer của Morph. |
| `build_deck.py` | Python Script | Mã nguồn tái tạo 100% file PPTX từ dữ liệu toạ độ và vector. |
| `tools/finalize.ps1` | PowerShell Script | Script tự động nạp font hệ thống, nhúng font vào PPTX và render PDF/PNG qua PowerPoint COM. |
| `NGUON_ANH.md` | Tài liệu | Bản quyền ảnh chân dung Lenin (Public Domain, 1920) và giấy phép mã nguồn mở của bộ font (OFL). |

---

## 2. Bảng phân công nhiệm vụ 13 thành viên (Slide 2)

Toàn bộ 13 thành viên được phân bổ mạch lạc thành 4 phân ban trên Slide 2:

### I. Ban Điều Hành & Kỹ Thuật
- **Nhóm Trưởng**: `@tao` — Điều phối chung & Phụ trách tổng hợp phần phạm trù.
- **Thư Ký**: `@Nguyễn Anh Thư` — Quản lý tiến độ & Phụ trách tổng hợp phần quy luật.
- **Thiết Kế Slide**: `@Quyen Le` — Kỹ thuật đồ hoạ, typography & kinetic morph.

### II. Ban Thuyết Trình & Phản Biện
- **Thuyết Trình 01**: `@Trần Nam Anh` — Dẫn dắt bài nói, phân tích cơ sở lý luận.
- **Thuyết Trình 02**: `@Giaa Minhh` — Trình bày trực quan, liên hệ thực tiễn.
- **Câu Hỏi Thảo Luận**: `@Phạm Văn Huy` — Nghiên cứu câu hỏi mở rộng & tương tác phản biện.

### III. Nghiên Cứu 3 Quy Luật Cơ Bản
- **QL Lượng – Chất**: `@Hồng Nhung` — Tích luỹ lượng đổi dẫn đến chất đổi.
- **QL Mâu Thuẫn**: `@Khánh Linh` — Nguồn gốc, động lực nội tại của sự phát triển.
- **QL Phủ Định của Phủ Định**: `@Hồng Nhung` — Khuynh hướng vận động xoáy ốc tiến lên.
- **Tổng hợp & Lọc ý**: `@Nguyễn Anh Thư` — Đúc kết luận điểm trọng tâm quy luật.

### IV. Nghiên Cứu Các Cặp Phạm Trù Biện Chứng
- **Nguyên nhân – Kết quả**: `@Phạm Duy` — Phân tích mối liên hệ nhân quả khách quan.
- **Tất nhiên – Ngẫu nhiên**: `@Đào Dươngg` — Bản chất bên trong & ngẫu nhiên bên ngoài.
- **Nội dung – Hình thức**: `@Vũ Minh Nghĩa` — Thống nhất biện chứng giữa nội dung và phương thức.
- **Khả năng – Hiện thực**: `@Duy` — Điều kiện khách quan chuyển hoá thực tiễn.
- **Tổng hợp & Lọc ý**: `@tao` — Kiểm duyệt hệ thống luận cứ & kết luận toàn bài.

---

## 3. Bản đồ Layer & Cơ chế Kinetic Morphing

Trong PowerPoint Morph, khi hai shape ở hai slide có cùng tiền tố `!!` (ví dụ `!!LENIN_HERO`), PowerPoint sẽ nội suy toạ độ $(x, y)$, kích thước $(w, h)$ và độ xoay thay vì mờ hình.

```
Slide 1 (Lời chào)                 Slide 2 (Đội ngũ 13 TV)            Slide 3 (Cảm ơn & Dẫn chương)
┌──────────────────────────────┐   ┌──────────────────────────────┐   ┌──────────────────────────────┐
│ [Title 1,2 on-screen]        │   │ [Title 1,2 exit left off-scr]│   │ [Title 1,2 exit left off-scr]│
│ [Lenin Hero (x=8.28, h=7.28)]│──>│ [Lenin Hero (x=9.35, h=6.55)]│──>│ [Lenin Hero (x=8.28, h=7.28)]│
│ [Team Cards wait at bottom]  │   │ [Team Cards rise from bottom]│   │ [Card 1 exit left, Card 2 btm]
│ [Badge 01 wait off-screen R] │   │ [Badge 01 wait off-screen R] │   │ [Badge 01 glides into center]│
└──────────────────────────────┘   └──────────────────────────────┘   └──────────────────────────────┘
```

### Danh mục layer chi tiết trong Selection Pane (`Alt + F10`):
1. **Lớp sân khấu cố định (Shared Stage)**:
   - `!!BG_DEEP`: Nền gradient đỏ sâu (`#8E191D` $\to$ `#650E13` $\to$ `#2C0408`).
   - `!!RAY_BURST`: Lớp tia sáng vàng kim toả từ tâm.
   - `!!TEXTURE_GRAIN`: Lớp hạt đỏ mờ tạo chất liệu giấy in cổ điển.
   - `!!FRAME_TOP`, `!!FRAME_BOTTOM`, `!!FRAME_LEFT`, `!!FRAME_RIGHT`: Khung viền chỉ vàng thanh lịch.
   - `!!KICKER_MARK`, `!!KICKER_TEXT`, `!!KICKER_RULE`: Masthead nhận diện học phần.
   - `!!FOOTER_LEFT`, `!!FOOTER_RIGHT`, `!!PAGE_NO`, `!!CREDIT_IMAGE`: Chân trang thông tin.
   - `!!SIDE_TEXT`: Dải chữ đọc dọc viền trái phong cách tạp chí Thuỵ Sĩ.

2. **Chân dung & Hào quang linh động**:
   - `!!LENIN_HERO`: Chân dung Lenin tách nền độ phân giải cao; di chuyển và co dãn mượt mà giữa các slide.
   - `!!GLOW_PORTRAIT`: Vầng sáng đỏ ấm phía sau đầu Lenin.
   - `!!STAR_BG`: Ngôi sao 5 cánh đường nét xoay góc nhẹ nhàng qua từng slide.
   - `!!ORBIT_RING`: Vòng cung quỹ đạo vàng mảnh.

3. **Khối nội dung động**:
   - `!!COVER_...`: Tiêu đề mở màn và lời chào (trượt sang mép trái ở Slide 2 & 3).
   - `!!TEAM_...`, `!!CARD_PANEL_1/2`, `!!CARD_CONTENT_1/2`: Bảng phân công 13 thành viên (chờ ở đáy slide 1, trồi lên slide 2, lướt ra slide 3).
   - `!!LENIN_QUOTE_BG` & `!!LENIN_QUOTE_BOX`: Biển trích dẫn câu nói kinh điển của Lenin năm 1902.
   - `!!THANKS_1/2`, `!!THANKS_SCRIPT`, `!!THANKS_LEAD`: Chữ CẢM ƠN typography hoành tráng Slide 3.
   - `!!BADGE_CIRCLE`, `!!BADGE_INNER_RING`, `!!BADGE_TEXT`: Huy hiệu phong cách huân chương Chương 01.

---

## 4. Hướng dẫn chỉnh sửa

- **Mở bảng chọn Layer**: Vào thẻ **Home** $\to$ **Select** $\to$ **Selection Pane** (hoặc gõ `Alt + F10`).
- **Sửa họ tên / vai trò**: Nhấp trực tiếp vào hộp văn bản trên Slide 2 để sửa tên thành viên hoặc tag `@tên`.
- **Đảm bảo Morph không bị gián đoạn**: Khi sửa đổi hoặc thêm bớt thành phần, luôn giữ nguyên tiền tố `!!` ở tên layer giữa các slide. Không thực hiện lệnh **Group (`Ctrl + G`)** đối với các shape tham gia Morph.

---

## 5. Quy trình biên dịch lại (Dành cho Developer)

Khi cần chỉnh sửa mã nguồn Python hoặc tạo biến thể slide mới:

```powershell
# 1. Cài đặt thư viện phụ thuộc (nếu chưa có)
pip install python-pptx pillow lxml

# 2. Sinh file trình chiếu PPTX với XML Morph
python build_deck.py

# 3. Nạp font, nhúng font vào PPTX và xuất bản PDF/PNG 1080p
powershell -ExecutionPolicy Bypass -File tools\finalize.ps1

# 4. Xuất video MP4 kiểm tra chuyển động Morph thực tế
python tools\test_video_export.py
```
