# -*- coding: utf-8 -*-
"""Agent 4: Visual Asset Creator (Chuyên gia Hình ảnh & Đồ họa)
Nhiệm vụ: Quản lý và chuẩn hóa các tài nguyên thị giác (cutout, biểu tượng vàng,
huy hiệu sáp, background), gán Visual Slots và ánh xạ mã Morphing Shape ID đồng nhất.
"""

from pathlib import Path
from typing import List, Dict
from studio.schemas import SlideSpec, VisualSlot, DesignTokens


class VisualAssetCreator:
    def __init__(self, assets_dir: Path):
        self.assets_dir = assets_dir

    def resolve_visual_slots(self, slides: List[SlideSpec], tokens: DesignTokens) -> List[SlideSpec]:
        """Gán các Visual Slot và tọa độ Kinetic Morphing cho 3 slide."""

        for s in slides:
            if s.slide_id == 1:
                # SLIDE 1: Hero Cover
                # Nền + Quầng sáng + Hero Card + Chân dung Lenin
                s.visual_slots = [
                    VisualSlot("bg_1", "stage_hero", "assets/master_stage_clean_bg.png", "!!STAGE_BG", 1, 0, 0, tokens.slide_width, tokens.slide_height, "background"),
                    VisualSlot("glow_1", "glow", "", "!!GLOW_PORTRAIT", 2, 6.80, 0.15, 6.40, 6.40, "glow"),
                    VisualSlot("star_1", "star_back", "", "!!STAR_BACK", 3, 6.80, 0.15, 6.40, 6.40, "vector_star"),
                    VisualSlot("ring_1", "orbit_ring", "", "!!ORBIT_RING", 4, 7.30, 0.65, 5.40, 5.40, "vector_ring"),
                    VisualSlot("card_1", "hero_card", "", "!!HERO_CARD", 5, 0.72, 0.85, 7.20, 5.80, "card_container"),
                    VisualSlot("star_badge_1", "star_badge", "assets/gold_star_clean.png", "!!CARD_STAR", 6, 0.95, 1.15, 0.24, 0.22, "emblem"),
                    VisualSlot("lenin_1", "lenin_cutout", "assets/lenin_hero_clean.png", "!!LENIN_HERO", 7, 6.85, 0.45, 5.95, 6.45, "character_hero"),
                    VisualSlot("pill_star_1", "pill_star", "assets/gold_star_clean.png", "!!PRESENTER_STAR", 8, 1.08, 5.95, 0.24, 0.22, "emblem"),
                    # Các layer Slide 2 chờ sẵn ngoài khung (Off-screen)
                    VisualSlot("worker_off", "worker_flag", "assets/soviet_worker_flag_clean.png", "!!WORKER_FLAG", 9, 0.15, 8.50, 4.55, 5.15, "offscreen_bottom"),
                    VisualSlot("hs_off", "hammer_sickle", "assets/soviet_hammer_sickle_clean.png", "!!HAMMER_SICKLE", 10, 1.20, -2.50, 1.15, 1.00, "offscreen_top"),
                    VisualSlot("star3d_off", "star_3d", "assets/soviet_3d_star_clean.png", "!!STAR_3D", 11, 2.45, -2.50, 1.15, 1.10, "offscreen_top"),
                    VisualSlot("lenin_wm_off", "lenin_watermark", "assets/lenin_crimson_watermark.png", "!!LENIN_WATERMARK", 12, 8.50, 8.50, 4.70, 6.90, "offscreen_bottom"),
                ]

            elif s.slide_id == 2:
                # SLIDE 2: Member Distribution & Soviet Constructivist Art
                s.visual_slots = [
                    VisualSlot("bg_2", "stage_dimmed", "assets/stage_bg_clean_dimmed.png", "!!STAGE_BG", 1, 0, 0, tokens.slide_width, tokens.slide_height, "background"),
                    # Left side: Emblems (drop down from top)
                    VisualSlot("hs_2", "hammer_sickle", "assets/soviet_hammer_sickle_clean.png", "!!HAMMER_SICKLE", 2, 1.20, 0.55, 1.15, 1.00, "emblem_top_left"),
                    VisualSlot("star3d_2", "star_3d", "assets/soviet_3d_star_clean.png", "!!STAR_3D", 3, 2.45, 0.50, 1.15, 1.10, "emblem_top_left"),
                    # Left side: Worker Flag (rises up from bottom)
                    VisualSlot("worker_2", "worker_flag", "assets/soviet_worker_flag_clean.png", "!!WORKER_FLAG", 4, 0.15, 2.35, 4.55, 5.15, "poster_bottom_left"),
                    # Right side: Lenin Watermark (in place)
                    VisualSlot("lenin_wm_2", "lenin_watermark", "assets/lenin_crimson_watermark.png", "!!LENIN_WATERMARK", 5, 8.50, 0.50, 4.70, 6.90, "character_watermark"),
                    # Lenin hero morphs away or blends
                    VisualSlot("lenin_exit", "lenin_cutout", "assets/lenin_hero_clean.png", "!!LENIN_HERO", 6, 15.0, 0.45, 5.95, 6.45, "offscreen_right"),
                    # Hero card exits left
                    VisualSlot("card_exit", "hero_card", "", "!!HERO_CARD", 7, -9.0, 0.85, 7.20, 5.80, "offscreen_left"),
                    VisualSlot("star_exit", "star_badge", "assets/gold_star_clean.png", "!!CARD_STAR", 8, -9.0, 1.15, 0.24, 0.22, "offscreen_left"),
                ]

            elif s.slide_id == 3:
                # SLIDE 3: Thank You & Chapter 01 Badge
                s.visual_slots = [
                    VisualSlot("bg_3", "stage_dimmed", "assets/stage_bg_clean_dimmed.png", "!!STAGE_BG", 1, 0, 0, tokens.slide_width, tokens.slide_height, "background"),
                    VisualSlot("glow_3", "glow", "", "!!GLOW_PORTRAIT", 2, 7.55, 0.55, 6.50, 6.50, "glow"),
                    VisualSlot("star_3", "star_back", "", "!!STAR_BACK", 3, 7.55, 0.55, 7.05, 7.05, "vector_star"),
                    VisualSlot("ring_3", "orbit_ring", "", "!!ORBIT_RING", 4, 9.38, 1.98, 3.28, 3.28, "vector_ring"),
                    # Slide 2 elements exit
                    VisualSlot("worker_exit", "worker_flag", "assets/soviet_worker_flag_clean.png", "!!WORKER_FLAG", 5, -8.0, 2.35, 4.55, 5.15, "offscreen_left"),
                    VisualSlot("hs_exit", "hammer_sickle", "assets/soviet_hammer_sickle_clean.png", "!!HAMMER_SICKLE", 6, 1.20, -2.50, 1.15, 1.00, "offscreen_top"),
                    VisualSlot("star3d_exit", "star_3d", "assets/soviet_3d_star_clean.png", "!!STAR_3D", 7, 2.45, -2.50, 1.15, 1.10, "offscreen_top"),
                    VisualSlot("lenin_wm_exit", "lenin_watermark", "assets/lenin_crimson_watermark.png", "!!LENIN_WATERMARK", 8, 15.0, 0.50, 4.70, 6.90, "offscreen_right"),
                ]

        return slides
