# -*- coding: utf-8 -*-
"""Định nghĩa JSON Schema cứng (Data Contracts) cho 6 Sub-agents trong AI Slide Studio.
Tuân thủ nguyên tắc: Không giao tiếp bằng văn xuôi - toàn bộ dữ liệu truyền qua Schema chuẩn.
"""

from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any
import json


@dataclass
class DesignTokens:
    """Design System Tokens do Creative Director thiết lập."""
    theme_name: str
    primary_color: str
    accent_gold: str
    card_bg: str
    text_cream: str
    text_muted: str
    font_display: str
    font_sans: str
    font_script: str
    slide_width: float = 13.333
    slide_height: float = 7.500
    morph_duration_ms: int = 1000
    grid_margin_left: float = 0.68
    grid_margin_right: float = 12.66
    grid_margin_top: float = 0.52
    grid_margin_bottom: float = 6.96


@dataclass
class VisualSlot:
    """Đặc tả vị trí và vai trò của một thành phần thị giác."""
    slot_id: str
    asset_id: str
    asset_path: str
    shape_morph_id: str
    layer_order: int
    x: float
    y: float
    w: float
    h: float
    role: str
    opacity: float = 1.0


@dataclass
class ContentItem:
    """Từng đơn vị nội dung / thành viên / gạch đầu dòng."""
    title: str
    subtitle: str
    body: str
    badge_label: Optional[str] = None


@dataclass
class SlideSpec:
    """Storyboard chi tiết cho một slide do Narrative Strategist & Data Specialist tạo ra."""
    slide_id: int
    slide_type: str  # hero_cover, member_distribution, thank_you_transition
    kicker: str
    headline: str
    subheadline: str
    quote: Optional[str] = None
    items: List[ContentItem] = field(default_factory=list)
    visual_slots: List[VisualSlot] = field(default_factory=list)
    speaker_notes: str = ""


@dataclass
class StudioBrief:
    """Đầu vào tổng quan từ người dùng gửi cho Studio."""
    topic: str
    deck_title: str
    target_audience: str
    total_slides: int
    raw_content: Dict[str, Any]


@dataclass
class QATicket:
    """Lỗi hoặc điểm cần hoàn thiện do Design QA phát hiện."""
    slide_id: int
    severity: str  # CRITICAL, WARNING, POLISH
    category: str  # OVERFLOW, CONTRAST, ALIGNMENT, OCCLUSION
    description: str
    fix_suggestion: str


@dataclass
class QAReport:
    """Báo cáo nghiệm thu của Design QA & Art Critic."""
    overall_status: str  # APPROVED, REVISE
    score: float  # 0 to 10
    tickets: List[QATicket] = field(default_factory=list)
    summary: str = ""

    def is_approved(self) -> bool:
        return self.overall_status == "APPROVED"
