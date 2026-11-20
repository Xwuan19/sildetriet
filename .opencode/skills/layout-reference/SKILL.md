---
name: Layout reference (350 bố cục)
description: Tra cứu 350 mẫu bố cục thị giác (typography, grid, editorial, film, presentation) làm tài liệu tham khảo khi cần chọn composition cho slide hoặc deck. Không sinh slide — chỉ chọn và mô tả bố cục.
---

# Layout reference — wrapper nội bộ

Repo gốc: `tools/350-layout-compositions` — https://github.com/nevertoday/350-layout-compositions (891 star).

## Cấu trúc

- `v2/catalog.csv` — danh mục 350 bố cục, có thể lọc bằng tên/chủ đề.
- `docs/350/README.md` — chỉ dẫn 8 nhóm chính:
  1. 构图逻辑 (86) — logic bố cục
  2. 视觉原则 (45) — nguyên tắc thị giác
  3. 出版广告 (36) — editorial/quảng cáo
  4. 字体网格 (54) — typography & grid
  5. 网页 UI (79)
  6. 影视画面 (14) — film frame
  7. 中国传统 (20)
  8. 演示文稿 (16) — **slide presentation**
- Ảnh PNG 1086×1448 **không có trong bản cài nội bộ** (archive đầy đủ bị treo khi tải). Nếu cần xem ảnh, tải zip từ trang release của repo rồi giải nén vào `tools/350-layout-compositions/v2/images/`.

## Cách dùng trong quy trình slide

1. Đọc brief → xác định vai trò trang (cover, statement, KPI, compare, process, closing).
2. Lọc `docs/350/08-presentation.md` (16 layout) và `v2/catalog.csv` trước. File `01-composition-logic.md` chỉ có trong repo đầy đủ — tải thêm nếu cần 86 layout logic.
3. Mô tả layout đã chọn bằng tiếng Việt/Anh cho `ppt-design-skill` hoặc `guizang-ppt-skill` như một **design anchor** (ví dụ: "KPI Tower, một số lớn lệch trái, ba chỉ số nhỏ dọc phải, đường kẻ hairline").
4. Không copy ảnh trực tiếp vào slide đã giao khách nếu chưa kiểm tra license trong `tools/350-layout-compositions/LICENSE`.
