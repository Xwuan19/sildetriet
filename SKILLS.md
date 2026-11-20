# Bộ skill nội bộ — Research → Giáo trình → Slide thiết kế

Curated ngày **19/11/2026** từ kết quả deep search. Nguyên tắc lọc: **mỗi vai trò chỉ giữ một skill mạnh nhất**; các repo cùng chức năng bị loại và ghi rõ lý do bên dưới.

## Cách dùng trong OpenCode V2

Mở chính folder này làm project. OpenCode tự discover skill từ `.opencode/skills/<id>/SKILL.md` — không cần `opencode.json`.

- Skill thường: gọi bằng `@ppt-design-skill`, `@huashu-design`, `@guizang-ppt-skill`, `@academic-pptx`, `@deep-research`, ...
- Tool wrapper: `@paper2slides`, `@layout-reference`.
- Refresh/cài lại: chạy `powershell -ExecutionPolicy Bypass -File .\setup-skills.ps1`.
- Repo gốc (để đọc README/license) nằm trong `tools/`.

## Danh sách đã cài

| ID skill | Vai trò duy nhất | Nguồn | Star | License | Vì sao chọn |
|---|---|---|---:|---|---|
| `ppt-design-skill` | **Sinh + nghiệm thu PPTX có thể edit** (chính) | [sunchaokun/PPT-Design-Skill](https://github.com/sunchaokun/PPT-Design-Skill) | 510 | MIT | Build Mode khoá design token, render PNG rồi qua 2 cổng QA (thẩm mỹ + lỗi/nội dung) trước khi giao — khác biệt thật so với generator thường. |
| `huashu-design` | **Hệ thống phong cách + đa đầu ra** (web/app/PPTX/infographic/animation) | [alchaincyf/huashu-design](https://github.com/alchaincyf/huashu-design) | 29.8k | MIT | 92 style có sample, 6 thumbnail → chọn 3 hướng, có design check; MIT từ 14/05/2026. |
| `guizang-ppt-skill` | **Deck HTML thiên thiết kế** (single file) | [op7418/guizang-ppt-skill](https://github.com/op7418/guizang-ppt-skill) | 30.1k | AGPL-3.0 | Swiss/International 22 layout khoá + editorial, có chế độ thuyết trình (speaker view) và fallback tĩnh. Output HTML, không cạnh tranh trực tiếp với PPTX. |
| `academic-pptx` | **Chuẩn truyền đạt học thuật** (bổ trợ, không sinh deck) | [Gabberflast/academic-pptx-skill](https://github.com/Gabberflast/academic-pptx-skill) | 1.6k | MIT | Action titles, ghost-deck test, 1 exhibit/trang, citation, slide Conclusions — áp dụng cho mọi deck học thuật. |
| `agent-research-skills` | **Workflow nghiên cứu nội dung** | [lingzhi227/agent-research-skills](https://github.com/lingzhi227/agent-research-skills) | 470 | xem repo | 31 skill thật (deep-research, literature-search, citation-management, figure-generation...). Đã xoá `slide-generation` để trùng với nhóm slide ở trên. |
| `paper2slides` (wrapper) | **Paper/PDF/report → slide + poster có nguồn** | [HKUDS/Paper2Slides](https://github.com/HKUDS/Paper2Slides) | 3.9k | MIT | RAG + link nguồn từng ý;CLI một lệnh. Repo là app Python nên dùng wrapper. |
| `layout-reference` (wrapper) | **Thư viện 350 bố cục** (tham khảo thiết kế) | [nevertoday/350-layout-compositions](https://github.com/nevertoday/350-layout-compositions) | 891 | xem repo | 8 nhóm/33 chủ đề. **Bản nội bộ chỉ có file text** (`README.md`, `docs/350/README.md`, `docs/350/08-presentation.md`, `v2/catalog.csv`); ảnh PNG nằm ở release nếu cần. Không phải skill sinh deck. |

Tool đi kèm **không đăng ký skill** (để tránh chồng trigger): `tools/ppt-master` — [hugohe3/ppt-master](https://github.com/hugohe3/ppt-master), 78.4k, MIT. Dùng khi cần chuyển hàng loạt PDF/DOCX/web → PPTX native có chart/template; là fallback cho `ppt-design-skill`.

## Lọc trùng — đã loại gì và tại sao

| Nhóm trùng | Giữ | Loại | Lý do |
|---|---|---|---|
| Sinh PPTX có kiểm tra thiết kế | `ppt-design-skill` | `siril9/presentation-skill` (109), `likaku/Mck-ppt-design-skill` (346), `chuspeeism/dashi-ppt-skill` (10.8k AGPL) | Cùng vai trò "outline → PPTX + QA". `ppt-design-skill` có 2 cổng QA + Build Mode rõ ràng nhất; dashi nhiều layout nhưng AGPL và không có QA tương đương; Mck chỉ là 1 style system con. |
| Generator PPTX hàng loạt | `tools/ppt-master` (fallback, không auto) | `Anionex/banana-slides`, `ningzimu/codex-ppt-skill`, `ningzimu/image-to-editable-ppt-skill`, chế độ FreeStyle của `sunchaokun` | Trùng cơ chế sinh ảnh/slide; ppt-master MIT + 78.4k + cập nhật 19/11/2026 nên hiệu quả hơn. |
| Deck HTML thiết kế | `guizang-ppt-skill` | `zarazhangrui/frontend-slides` (32.6k) | Cả hai tạo HTML deck đẹp. Giữ guizang vì hệ thống Swiss/editorial cụ thể +演讲者模式; frontend-slides để lại làm phương án dự phòng (chưa cài). |
| Workflow nghiên cứu | `agent-research-skills` | `WenyuChiou/ai-research-skills` (677), `LMDHQ-0420/ResearchPilot-Skills` (336) | Hai cái sau là catalog/harness (không có `SKILL.md` trong repo) hoặc trùng 31 skill. agent-research-skills có skill cài được ngay. |
| Slide trong bundle research | — | `agent-research-skills/skills/slide-generation` | Trùng với `ppt-design-skill` / `guizang-ppt-skill`; đã xoá khỏi bản cài. |
| App web đọc paper | — | `khoj-ai/openpaper`, `summarizepaper/summarizepaper`, `vitorfs/parsifal` | Là ứng dụng/web service, không phải skill cài được trong project. Giữ làm nguồn ngoài. |

> Ghi chú: `dashi-ppt-skill`, `PPT-Design-Skill` và `ai-research-skills` lúc đầu được liệt kê trong danh sách tìm kiếm, nhưng sau khi kiểm tra cây thư mục: dashi có skill tại `skills/dashi-ppt/SKILL.md`, PPT-Design-Skill tại `skill/SKILL.md` (đã flatten để ID đúng), ai-research-skills **không có SKILL.md nào** — nên không thể cài như skill.

## Cấu trúc thư mục

```text
sildetriet/
├─ SKILLS.md                     ← file này
├─ setup-skills.ps1              ← script tải/cài lại (curl + tar, không cần git)
├─ .download/                    ← ZIP tải về (có thể xoá sau khi cài)
├─ .opencode/skills/             ← OpenCode tự discover ở đây
│  ├─ ppt-design-skill/          ← flatten từ tools/PPT-Design-Skill/skill
│  ├─ huashu-design/
│  ├─ guizang-ppt-skill/
│  ├─ academic-pptx/
│  ├─ agent-research-skills/     ← 30 skill (đã bỏ slide-generation)
│  ├─ paper2slides/SKILL.md      ← wrapper
│  └─ layout-reference/SKILL.md  ← wrapper
└─ tools/                        ← repo gốc để đọc README/license
   ├─ PPT-Design-Skill/
   ├─ huashu-design/
   ├─ guizang-ppt-skill/
   ├─ academic-pptx-skill/
   ├─ agent-research-skills/
   ├─ ppt-master/
   ├─ Paper2Slides/
   └─ 350-layout-compositions/
```

## Lưu ý khi chạy

- `guizang-ppt-skill`, `ppt-master`, `Paper2Slides` cần Python; `ppt-design-skill` cần thư viện `pptx-designer` và có script render (`render_pptx.ps1`) → cần LibreOffice/PowerPoint để xuất PNG QA.
- `huashu-design` và `guizang-ppt-skill` có asset lớn; nếu export PDF cần Chrome/Edge đã cài.
- License: `guizang-ppt-skill` là **AGPL-3.0** — cẩn trọng khi phân phối bản dẫn xuất. Các skill còn lại MIT/Apache hoặc license ghi trong repo.
- Không lưu API key vào thư mục này; dùng biến môi trường nếu skill cần model API.
