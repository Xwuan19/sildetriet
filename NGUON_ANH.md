# Nguồn ảnh, nguồn chữ và giấy phép

Tài liệu này ghi lại mọi tài nguyên bên ngoài được dùng trong bộ slide, để bạn biết phần nào được dùng tự do và phần nào cần thay nếu mục đích sử dụng thay đổi.

## 1. Chân dung V. I. Lenin

| Mục | Thông tin |
|---|---|
| Tác phẩm | Chân dung V. I. Lenin |
| Tác giả | Pavel Semyonovich Zhukov (1870–1942) |
| Năm | 1920 |
| Nguồn | Wikimedia Commons — [File:Lenin 1920.jpg](https://commons.wikimedia.org/wiki/File:Lenin_1920.jpg) |
| File gốc | [Lenin_1920.jpg](https://upload.wikimedia.org/wikipedia/commons/8/83/Lenin_1920.jpg) · 2112 × 3200 px |
| Giấy phép | **Public domain** (hết thời hạn bảo hộ; tác giả mất năm 1942) |
| Lưu trong dự án | `assets/lenin_1920.jpg` |

Wikimedia Commons xác nhận ảnh thuộc phạm vi công cộng; có thể dùng, in, cắt, chỉnh màu và phân phối lại mà không cần xin phép. Ghi công là lịch sự, không bắt buộc — deck vẫn ghi nguồn ở layer `CREDIT_IMAGE`.

### Các phiên bản đã xử lý

| File | Kích thước | Cách tạo | Dùng ở đâu |
|---|---|---|---|
| `assets/lenin_warm.png` | 1548 × 2029 | Tách nền bằng rembg (u2net), cắt bán thân, chỉnh sepia ấm, tăng tương phản | Slide 1 — `LENIN_HERO` |
| `assets/lenin_medallion.png` | 1200 × 1200 | Cắt tròn từ bản duotone vàng, nền trong suốt | Trung gian để làm huy hiệu |
| `assets/lenin_badge.png` | 1200 × 1200 | Ghép đĩa đỏ gradient + viền vàng + medallion | Slide 2 — `PORTRAIT_LENIN` |

Script tạo lại: `tools/prepare_lenin.py` (cutout, warm, gold, medallion, rays, grain) và `tools/make_badge.py` (huy hiệu tròn).

> Chạy lại rembg có thể cho kết quả hơi khác do model/phiên bản. File PNG đã xử lý được giữ sẵn trong `assets/`, không cần chạy lại nếu chỉ sửa chữ.

### Trích dẫn trên slide 2

> “Không có lý luận cách mạng thì không có phong trào cách mạng.”
> V. I. Lênin, *Làm gì?* (1902)

Tác phẩm gốc đã hết thời hạn bảo hộ. Bản dịch tiếng Việt ngắn dùng cho mục đích học tập; nếu xuất bản thương mại, nên đối chiếu lại với bản dịch chính thức của nhà xuất bản.

## 2. Họa tiết nền

| File | Kích thước | Cách tạo |
|---|---|---|
| `assets/rays_gold.png` | 2400 × 1350 | Vẽ bằng Pillow: chùm tia vàng mảnh, mờ dần từ tâm |
| `assets/grain_red.png` | 2000 × 1125 | Nhiễu hạt đỏ sinh bằng Pillow, alpha thấp |

Cả hai do script trong dự án tạo, không lấy từ ảnh ngoài, không có vấn đề bản quyền.

Nền chính là gradient vector `#8E191D → #650E13 → #2C0408`, không dùng ảnh.

## 3. Font chữ

Cả ba font đều theo **SIL Open Font License 1.1 (OFL)** — được dùng miễn phí, kể cả thương mại, được nhúng vào file và phân phối kèm tài liệu; nếu sửa và phát hành lại, phải đổi tên nếu font gốc có Reserved Font Name.

| Font trong deck | Font gốc | Giấy phép | Ghi chú |
|---|---|---|---|
| `Playfair Editorial` | [Playfair Display](https://fonts.google.com/specimen/Playfair+Display) | OFL 1.1, RFN “Playfair Display” | Đã đổi tên family; giữ nguyên dòng copyright trong file |
| `Playfair Editorial Italic` | Playfair Display Italic | OFL 1.1, RFN “Playfair Display” | Biến thể nghiêng, đổi tên family |
| `Script Viet` | [Dancing Script](https://fonts.google.com/specimen/Dancing+Script) | OFL 1.1, RFN “Dancing Script” | **Đã đổi tên** khỏi tên dành riêng; file `fonts/ScriptViet-Bold.ttf` |
| `Be Vietnam Pro` | [Be Vietnam Pro](https://fonts.google.com/specimen/Be+Vietnam+Pro) | OFL 1.1, không có RFN | Giữ tên gốc, tạo các style Regular / SemiBold / Bold |
| `Be Vietnam Pro SemiBold` | Be Vietnam Pro | OFL 1.1 | Family riêng để PowerPoint không tự ghép weight |

Văn bản giấy phép đầy đủ:

- `fonts/licenses/OFL-PlayfairDisplay.txt`
- `fonts/licenses/OFL-DancingScript.txt`
- `fonts/licenses/OFL-BeVietnamPro.txt`

Dòng copyright gốc vẫn nằm trong name table của từng file TTF (nameID 0), đúng yêu cầu OFL.

### Vì sao đổi tên font?

OFL cấm dùng Reserved Font Name cho **phiên bản đã sửa**. Vì deck tạo instance tĩnh từ variable font (một dạng sửa đổi), các family được đặt tên mới:

- “Playfair Display” → **Playfair Editorial**
- “Dancing Script” → **Script Viet**

Tên file và tên family trong `build_deck.py` phải khớp với name table; đổi một chỗ mà không đổi chỗ kia sẽ khiến PowerPoint fallback font.

## 4. Nếu thay tài nguyên

1. **Thay ảnh Lenin:** dùng ảnh public domain hoặc ảnh bạn có quyền; cập nhật `CREDIT_IMAGE` (dòng nguồn ảnh cuối slide) và `PORTRAIT_CAPTION`/`PORTRAIT_SOURCE` ở slide 2.
2. **Thay font:** kiểm tra font có đủ dấu tiếng Việt, cài cho user, sửa `DISPLAY`/`SCRIPT`/`SANS` trong `build_deck.py`, rồi build lại và chạy `finalize.ps1`.
3. **Dùng cho mục đích thương mại:** ảnh Lenin và font đều ổn; chỉ cần xem lại phần trích dẫn dịch thuật và thông tin nhóm/lớp.
