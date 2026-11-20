# -*- coding: utf-8 -*-
"""Agent 1: Creative Director (Giám đốc Sáng tạo & Orchestrator)
Nhiệm vụ: Phân tích brief, chốt phong cách thẩm mỹ, khóa chặt Design Tokens (JSON)
và thiết lập quy tắc vận hành cho toàn bộ studio.
"""

from pathlib import Path
import json
from studio.schemas import StudioBrief, DesignTokens


class CreativeDirector:
    def __init__(self, workspace_root: Path):
        self.workspace_root = workspace_root

    def create_design_tokens(self, brief: StudioBrief) -> DesignTokens:
        """Khóa chặt Design Tokens ngay từ đầu, đảm bảo không bị trôi dạt thẩm mỹ."""
        # Nhận diện chủ đề: Triết học Mác – Lênin / Chính luận Liên Xô
        tokens = DesignTokens(
            theme_name="Soviet Constructivist & Editorial Neo-Classical",
            primary_color="#8E1A1E",      # Đỏ cờ nhung cách mạng
            accent_gold="#E8C872",        # Vàng kim dập nổi kim loại
            card_bg="#28080C",            # Đỏ thẫm sâu cho thẻ nội dung
            text_cream="#FBF6EE",         # Trắng kem ngà cho tiêu đề chính
            text_muted="#D6C4B8",         # Kem trầm cho phụ đề và chú thích
            font_display="Playfair Editorial",  # Serif chính luận trang trọng
            font_sans="Be Vietnam Pro",         # Sans tiếng Việt sắc sảo
            font_script="Script Viet",          # Cursive mềm mại mở đầu
            slide_width=13.333,
            slide_height=7.500,
            morph_duration_ms=1000,       # Chuẩn xác 1.00s theo video tham chiếu
            grid_margin_left=0.68,
            grid_margin_right=12.66,
            grid_margin_top=0.52,
            grid_margin_bottom=6.96,
        )
        return tokens
