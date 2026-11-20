# -*- coding: utf-8 -*-
"""Agent 2: Narrative & Content Strategist (Chuyên gia Kịch bản & Nội dung)
Nhiệm vụ: Ép nội dung tuân theo nguyên tắc "1 slide = 1 thông điệp cốt lõi".
Cô đọng copy, viết Action Title và soạn Speaker Notes chi tiết.
"""

from typing import List
from studio.schemas import StudioBrief, DesignTokens, SlideSpec, ContentItem


class NarrativeStrategist:
    def __init__(self, tokens: DesignTokens):
        self.tokens = tokens

    def build_storyboard(self, brief: StudioBrief) -> List[SlideSpec]:
        """Tạo dàn ý Storyboard chuẩn xác, chia nhỏ nội dung vào 3 slide cô đọng."""
        slides: List[SlideSpec] = []

        # SLIDE 1: Mở đầu ấn tượng - Lời chào & Định vị chủ đề
        s1 = SlideSpec(
            slide_id=1,
            slide_type="hero_cover",
            kicker="HỌC PHẦN TRIẾT HỌC MÁC – LÊNIN",
            headline="Triết học Mác – Lênin",
            subheadline="LỜI CHÀO  ·  GIỚI THIỆU PHÂN CÔNG 13 THÀNH VIÊN",
            quote="“Tư duy phê phán bắt đầu từ việc hoài nghi đúng cách và đặt lại những câu hỏi.”",
            items=[
                ContentItem(
                    title="Trình bày",
                    subtitle="Nhóm 13 thành viên",
                    body="Đại học Quốc gia",
                    badge_label="SLIDE"
                )
            ],
            speaker_notes=(
                "Kính chào thầy cô và các bạn. Chúng em là Nhóm 13 thành viên. "
                "Hôm nay nhóm xin gửi lời chào và giới thiệu chi tiết phân công nhiệm vụ trước khi bước vào bài thảo luận. "
                "Nhóm gồm 13 thành viên phụ trách các phần: Điều hành, Thuyết trình, 3 Quy luật cơ bản và các Cặp phạm trù biện chứng."
            )
        )
        slides.append(s1)

        # SLIDE 2: Đội ngũ & Phân công nhiệm vụ 13 thành viên (Hành động & Phân ban)
        s2 = SlideSpec(
            slide_id=2,
            slide_type="member_distribution",
            kicker="ĐỘI NGŨ THỰC HIỆN  ·  HỌC PHẦN TRIẾT HỌC MÁC – LÊNIN",
            headline="PHÂN CÔNG NHIỆM VỤ",
            subheadline="Mười ba thành viên, một tinh thần biện chứng",
            quote="“Không có lý luận cách mạng thì không có phong trào cách mạng.” — V. I. Lênin (1902)",
            items=[],  # Sẽ được Data & Chart Specialist chuẩn hóa và điền vào
            speaker_notes=(
                "Chi tiết phân công nhiệm vụ 13 thành viên: "
                "Ban điều hành gồm Nhóm Trưởng, Thư Ký Nguyễn Anh Thư và phụ trách kỹ thuật slide Quyên Lê. "
                "Thuyết trình do Trần Nam Anh và Giaa Minhh đảm nhận; Phạm Văn Huy phụ trách câu hỏi thảo luận. "
                "Nội dung 3 quy luật do Hồng Nhung và Khánh Linh nghiên cứu (Thư ký tổng hợp). "
                "Nội dung các cặp phạm trù do Phạm Duy, Đào Dươngg, Vũ Minh Nghĩa và Duy nghiên cứu (Nhóm trưởng tổng hợp)."
            )
        )
        slides.append(s2)

        # SLIDE 3: Kết thúc lời chào & Chuyển giao vào Chương 01
        s3 = SlideSpec(
            slide_id=3,
            slide_type="thank_you_transition",
            kicker="LỜI CẢM ƠN  ·  NHÓM 13 THÀNH VIÊN",
            headline="CẢM ƠN",
            subheadline="và hẹn gặp lại ở Chương 1",
            quote="“Mời thầy cô và các bạn bước vào hành trình tư duy phê phán.”",
            items=[
                ContentItem(
                    title="01",
                    subtitle="CHƯƠNG",
                    body="DUY VẬT BIỆN CHỨNG",
                    badge_label="01"
                )
            ],
            speaker_notes=(
                "Cảm ơn thầy cô và các bạn đã lắng nghe phần giới thiệu đội ngũ. "
                "Nhóm 13 thành viên xin mời cả lớp bước vào Chương 1: Chủ nghĩa duy vật biện chứng. "
                "Phần tiếp theo sẽ bắt đầu từ câu hỏi trung tâm: vật chất và ý thức quan hệ với nhau như thế nào?"
            )
        )
        slides.append(s3)

        return slides
