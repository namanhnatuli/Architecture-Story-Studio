# PROJECT BRIEF — ARCHITECTURE STORY STUDIO

## Sản phẩm
Kênh YouTube **tiếng Anh** (mục tiêu 8–15 phút/video) giải thích những lựa chọn, biến đổi, khác biệt và lịch sử kiến trúc bằng **hoạt ảnh 3D stylized** kết hợp tư liệu, bản đồ, đồ họa và thuyết minh.

### Ba nhóm video cốt lõi
1. **Design decisions:** A là ý tưởng ban đầu; ràng buộc X/Y/Z dẫn tới B. Visual A → tháo cấu kiện → visual B; làm nổi bật lý do thay đổi.
2. **Evolution through time:** theo dõi các kiểu cầu, mái, vật liệu, công nghệ qua những mốc *có kiểm chứng*. Không giả định một tiến trình tuyến tính toàn cầu.
3. **Regional comparison:** so sánh các loại hình công trình ở khu vực, thời kỳ và khí hậu cụ thể. Tránh đồng nhất 'nhà Trung Quốc/Nhật Bản/phương Tây'.

### Vai trò hình ảnh
- Cho người xem **nhìn thấy** logic. Mỗi scene có `claim_ids`, `visual_purpose`, một thay đổi dễ nhận biết.
- Chủ đạo: Clean Stylized 3D / Technical Architectural Visualization. Camera ổn định khi so sánh A/B; màu vật liệu dịu, đọc được cấu kiện.
- Hiệu ứng chuẩn: ASSEMBLE, DISASSEMBLE, REPLACE_PARTS, EXPLODED_VIEW, CUTAWAY, SIDE_BY_SIDE, STATE_TRANSITION, CAUSE_AND_EFFECT, HIGHLIGHT_DIFFERENCE.
- Không cần nhân vật, công nhân, xe cẩu; phá hủy vật lý chỉ khi câu chuyện *thực sự* cần.

### Công cụ
Codex hoặc Claude Code làm developer; Blender Python (`bpy`) làm 3D engine; Geometry Nodes/instancing khi phù hợp; Blender MCP để QA/tinh chỉnh scene tùy chọn; FFmpeg cho kết xuất; TTS và nguồn lưu trữ bên ngoài tùy chọn.

### Chất lượng và giới hạn
- Máy khởi điểm: Mac Apple Silicon M4 / 16 GB, preview 640x360 hoặc 960x540, 24 fps, Eevee. Final 1080p sau khi preview đạt.
- Không bịa dẫn chứng, kiểu nhà, niên đại, thông số chịu lực. Các cảnh demo luôn ghi là mô hình minh họa.
- Không tải/sử dụng tài sản chưa rõ license; không chuyển bản vẽ nghệ thuật thành chứng cứ.
- Không gửi tác vụ render final dài nếu chưa qua quality gates. Không cho MCP/code AI quyền xóa/sửa file ngoài project.

## Thành công giai đoạn 1
1. AI đọc spec và triển khai đúng không cần người dùng thao tác Blender.
2. JSON validate → dựng greybox → render still → render preview 6s → tạo MP4.
3. Hai state A/B cùng dùng bộ tường/móng; mái A tách ra và mái B lắp vào, camera không đổi.
4. Mở rộng được thư viện state/template mà không sửa toàn bộ engine.
