# Báo cáo dọn dẹp dự án (M7 finalization, 2026-10-30)

**Mục tiêu:** `projects/` chỉ còn phim đang làm, `why-bridges-look-different`. Không mất lịch sử, không làm hỏng code dùng chung hay test hồi quy.

## Kết quả
- `projects/` hiện chỉ có `why-bridges-look-different/`.
- Sáu pilot cũ được tách làm hai phần:
  - **Nguồn git-tracked** (286 file): `git mv` sang `tests/fixtures/legacy_projects/<slug>/`. Cả 286 file là rename 100%, không sửa nội dung.
  - **File sinh ra, không có trong git** (9.979 file, 3.355.383.142 byte): chuyển ra ngoài repo vào `~/Work/Projects/Architecture-Story-Studio-archive/legacy-projects-2026-10-30/generated/<slug>/`. Có SHA256 trước và sau khi chuyển; kiểm lại toàn bộ ngày 2026-10-30, 0 sai lệch.
- **Bundle git** `architecture-story-studio-all-refs-2026-10-30.bundle`:
  - tạo bằng `git bundle --all`: mọi branch và tag tới `24d13c1`;
  - SHA256 `c9578dfc…4082`;
  - `git bundle verify`: complete history.
- **Tài liệu kèm theo** trong thư mục lưu trữ: `inventory.json` và `README.md` (cách khôi phục và cách kiểm tra).
- **Không xóa gì.** Không dùng `git clean` hay lệnh xóa đệ quy. Không xóa code, asset hay test dùng chung.

| Dự án | Vai trò cũ | File tracked → fixture | File sinh ra → lưu trữ |
|---|---|---:|---:|
| roof-evolution | M2 pilot mái A/B | 26 | 1.063 |
| suffolk-roofs | M3 pilot có lời dẫn (OmniVoice) | 68 | 1.912 |
| bridge-structure-evolution | M4 cầu thủ tục | 19 | 787 |
| bridge-story-m5, roof-plan-m5 | M5 planner hình ảnh | 41 + 19 | 1.900 + 538 |
| bridge-load-explained | M6 phim có lời dẫn Kokoro | 113 | 3.779 |

## Phụ thuộc đã tìm thấy và cách xử lý
Tìm bằng `grep -rlI <slug>` trên toàn repo, không tính `.git`, fixture và `projects/`.

| Nơi phụ thuộc | Phụ thuộc vào | Xử lý |
|---|---|---|
| 13 module test (`test_validation_m2`, `test_contracts`, `test_motion`, `test_blender_integration`, `test_m3_pipeline`, `test_m35`, `test_m4_arch`, `test_m5_planner`, `test_blender_m5`, `test_m55_visual_intelligence`, `test_blender_m55`, `test_m6_narrated`, `test_blender_m6`) | đọc `projects/<slug>` | Đọc `LEGACY = tests/fixtures/legacy_projects`. Assertion giữ nguyên, không xóa test nào. |
| `tests/test_m7_longform.py` | trạng thái "chờ duyệt" của phim M7 | Viết lại theo trạng thái đã duyệt. Các ca âm (thiếu duyệt, duyệt bị rút, revision lệch) chạy trên bản sao. |
| `evaluation/visual_planning/cases.json` | đường dẫn dự án M5/M6 | Trỏ sang fixture. |
| `planner/catalog.py` (asset catalog) | `states.json` của `roof-evolution` và `suffolk-roofs` | Bản sao ở `asset_library/legacy_states/<slug>/` (kèm tóm tắt QA Blender). Asset id giữ nguyên. |
| `tools/make_bridge_pilot.py` | `projects/bridge-structure-evolution` | Trỏ sang fixture. |
| `tools/cli.py` | `--project` mặc định `roof-evolution` | Không còn mặc định cứng: dùng dự án duy nhất trong `projects/`; có nhiều hơn một thì phải ghi `--project`. |
| `tools/pronunciation_test.py` | mặc định `suffolk-roofs` | `--project` bắt buộc. Docstring ghi rõ đây là công cụ của pilot OmniVoice M3. |
| `tools/voice_audition.py`, `tools/annotation_preview.py` | ví dụ trong docstring | Ví dụ đổi sang phim đang làm. |
| `config/visual_planning.json` | ghi chú hiệu chỉnh "calibrated on bridge-story-m5 frames" | Giữ nguyên: đây là nguồn gốc của ngưỡng, không phải đường dẫn. |
| `docs/m3` … `docs/m7`, `CHANGELOG.md`, `PROJECT_STATUS.md`, `DECISIONS.md` | đường dẫn `projects/<slug>` cũ | Giữ nguyên làm tài liệu lịch sử. Đường dẫn hiện tại là `tests/fixtures/legacy_projects/<slug>`. |
| `PACKAGE_MANIFEST.sha256` | danh sách file | Sinh lại bằng `python3 tools/cli.py manifest`. |

**Hạ tầng dùng chung giữ nguyên:**
- `engine/`, `planner/`, `pipeline/`, `integrations/`;
- `asset_library/architecture/` (mọi spec cầu, nhà, mái và site);
- `config/`, `evaluation/`;
- bộ test Blender.

## Kiểm chứng
- Bộ test offline và bộ test Blender chạy sau khi chuyển: kết quả ở `docs/m7/M7_FINALIZATION_REPORT.md`.
- `python3 tools/cli.py evaluate-planning` chạy trên fixture.
- `python3 tools/cli.py asset-catalog` vẫn liệt kê states mái cũ với id cũ.

## Khôi phục
Xem `README.md` trong thư mục lưu trữ. Tóm tắt:
1. `git mv tests/fixtures/legacy_projects/<slug> projects/<slug>`;
2. `rsync -a <archive>/generated/<slug>/ projects/<slug>/`;
3. chuyển lại về fixture trước khi chạy test.

Muốn lấy lại toàn bộ lịch sử: `git clone <bundle>`.
