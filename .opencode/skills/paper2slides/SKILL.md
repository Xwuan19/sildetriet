---
name: Paper2Slides (tool wrapper)
description: Chuyển paper/PDF/report thành slide hoặc poster chuyên nghiệp có liên kết nguồn cho từng ý. Dùng khi đầu vào là bài báo nghiên cứu và cần deck/poster truy vết được nguồn, không phải khi chỉ cần viết nội dung từ đầu.
---

# Paper2Slides — wrapper nội bộ

Repo gốc: `tools/Paper2Slides` — https://github.com/HKUDS/Paper2Slides (MIT, 3.9k star).

## Khi nào dùng

- Có file PDF/Word/Markdown/paper và muốn biến thành slide hoặc poster.
- Cần giữ traceability: mỗi ý được sinh ra phải link lại đúng đoạn trong paper (RAG + source-linked).
- Muốn đổi style bằng ngôn ngữ tự nhiên hoặc dùng theme có sẵn (`doraemon`, `academic`, `custom`).

## Cách chạy

```bash
python -m paper2slides --input paper.pdf --output slides --style academic --length medium --fast --parallel 2
```

Yêu cầu: Python 3.12+, cài dependency từ `tools/Paper2Slides/requirements.txt`. Đọc `tools/Paper2Slides/README.md` trước khi chạy để biết tuỳ chọn mới nhất.

## Quy trình nội bộ khuyến nghị

1. Trích nội dung paper bằng `deep-research`/`paper-writing-section` nếu cần tóm tắt có cấu trúc.
2. Chạy `paper2slides` để có bản slide/poster đầu.
3. Áp `academic-pptx` để sửa action title, exhibit và citation.
4. Nếu cần thiết kế lại hoàn toàn, dùng `ppt-design-skill` (Build Mode) thay vì chỉnh trực tiếp output.

Không chỉnh sửa code trong `tools/Paper2Slides` trừ khi được yêu cầu — đây là bản vendored để tham khảo.
