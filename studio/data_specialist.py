# -*- coding: utf-8 -*-
"""Agent 3: Data & Chart Specialist (Chuyên gia Dữ liệu & Cấu trúc Thông tin)
Nhiệm vụ: Chuyển hóa dữ liệu thô (danh sách 13 thành viên) thành cấu trúc phân ban
khoa học, cân đối số lượng giữa 4 nhóm và làm sạch câu chữ để tránh tràn khung.
"""

from typing import List, Dict, Any
from studio.schemas import SlideSpec, ContentItem


class DataSpecialist:
    def __init__(self):
        pass

    def structure_member_data(self, slide2: SlideSpec, raw_members: List[Dict[str, Any]]) -> SlideSpec:
        """Chuẩn hóa dữ liệu 13 thành viên vào 4 nhóm biện chứng cân đối."""
        # 4 nhóm biện chứng chuẩn xác
        groups = [
            {
                "roman": "I",
                "title": "Ban Điều Hành & Kỹ Thuật",
                "badge": "assets/soviet_seal_badge_1.png",
                "members": [
                    ("Nhóm Trưởng", "Điều phối chung", "Điều phối tiến độ & Tổng hợp các cặp phạm trù"),
                    ("Nguyễn Anh Thư", "Thư ký học thuật", "Quản lý hồ sơ nghiên cứu & Tổng hợp quy luật"),
                    ("Quyên Lê", "Thiết kế & Kỹ thuật", "Kiến trúc mỹ thuật, typography & chuyển động morph"),
                ]
            },
            {
                "roman": "II",
                "title": "Ban Thuyết Trình & Phản Biện",
                "badge": "assets/soviet_seal_badge_2.png",
                "members": [
                    ("Trần Nam Anh", "Thuyết trình 01", "Dẫn dắt bài nói, phân tích cơ sở lý luận & luận điểm"),
                    ("Giaa Minhh", "Thuyết trình 02", "Trình bày trực quan, liên hệ thực tiễn sinh động"),
                    ("Phạm Văn Huy", "Thảo luận", "Nghiên cứu câu hỏi tương tác & phản biện mở rộng"),
                ]
            },
            {
                "roman": "III",
                "title": "Nghiên Cứu 3 Quy Luật Cơ Bản",
                "badge": "assets/soviet_seal_badge_3.png",
                "members": [
                    ("Hồng Nhung", "QL Lượng – Chất", "Tích luỹ lượng đổi dẫn đến biến đổi về chất"),
                    ("Khánh Linh", "QL Mâu Thuẫn", "Nguồn gốc, động lực nội tại của sự phát triển"),
                    ("Hồng Nhung", "QL Phủ Định của PĐ", "Khuynh hướng vận động xoáy ốc tiến lên"),
                    ("Nguyễn Anh Thư", "Tổng hợp luận điểm", "Đúc kết luận điểm trọng tâm của ba quy luật"),
                ]
            },
            {
                "roman": "IV",
                "title": "Các Cặp Phạm Trù Biện Chứng",
                "badge": "assets/soviet_seal_badge_4.png",
                "members": [
                    ("Phạm Duy", "Nguyên nhân – KQ", "Phân tích mối liên hệ nhân quả khách quan"),
                    ("Đào Dươngg", "Tất nhiên – NN", "Bản chất bên trong & hiện tượng bên ngoài"),
                    ("Vũ Minh Nghĩa", "Nội dung – HT", "Thống nhất biện chứng giữa nội dung & hình thức"),
                    ("Duy", "Khả năng – HT", "Điều kiện khách quan chuyển hoá vào thực tiễn"),
                    ("Nhóm Trưởng", "Tổng hợp luận cứ", "Kiểm duyệt hệ thống luận cứ & kết luận toàn bài"),
                ]
            }
        ]

        slide2.items = []
        for g in groups:
            # Gói mỗi nhóm thành một ContentItem có cấu trúc sạch
            import json
            item = ContentItem(
                title=f"{g['roman']}.  {g['title'].upper()}",
                subtitle=g["roman"],
                body=json.dumps(g["members"], ensure_ascii=False),
                badge_label=g["badge"]
            )
            slide2.items.append(item)

        return slide2
