# -*- coding: utf-8 -*-
"""Pipeline thực thi tự động kết nối Tổ đội 6 Sub-agents:
1. CreativeDirector -> DesignTokens
2. NarrativeStrategist -> Storyboard
3. DataSpecialist -> Cấu trúc 13 thành viên 4 nhóm
4. VisualAssetCreator -> Ánh xạ VisualSlots và Kinetic Morph IDs
5. LayoutDesigner -> Dựng file PPTX
6. DesignQACritic -> Export PNG 1080p và kiểm định thị giác (QA Report)
"""

import sys
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from studio.schemas import StudioBrief
from studio.director import CreativeDirector
from studio.narrative import NarrativeStrategist
from studio.data_specialist import DataSpecialist
from studio.visual_creator import VisualAssetCreator
from studio.layout_designer import LayoutDesigner
from studio.qa_critic import DesignQACritic


def main():
    print("=" * 60)
    print("AI SLIDE STUDIO: KHỞI CHẠY QUY TRÌNH 6 SUB-AGENTS")
    print("=" * 60)

    brief = StudioBrief(
        topic="Triết học Mác – Lênin",
        deck_title="Lời chào & Phân công nhiệm vụ 13 thành viên",
        target_audience="Giảng viên & Sinh viên Đại học",
        total_slides=3,
        raw_content={}
    )

    # 1. Creative Director
    print("\n[1/6] Creative Director: Thiết lập Design Tokens...")
    director = CreativeDirector(ROOT)
    tokens = director.create_design_tokens(brief)
    tokens_file = ROOT / ".opencode" / "schemas" / "active_design_tokens.json"
    with open(tokens_file, "w", encoding="utf-8") as f:
        json.dump(tokens.__dict__, f, ensure_ascii=False, indent=2)
    print(f" -> Đã chốt Design Tokens: {tokens.theme_name}")

    # 2. Narrative Strategist
    print("\n[2/6] Narrative Strategist: Xây dựng Storyboard (1 slide = 1 thông điệp)...")
    strategist = NarrativeStrategist(tokens)
    slides = strategist.build_storyboard(brief)
    print(f" -> Đã tạo kịch bản cho {len(slides)} slide.")

    # 3. Data Specialist
    print("\n[3/6] Data Specialist: Chuẩn hóa dữ liệu 13 thành viên vào 4 nhóm...")
    data_spec = DataSpecialist()
    slides[1] = data_spec.structure_member_data(slides[1], [])
    print(f" -> Đã phân bổ dữ liệu thành {len(slides[1].items)} phân ban cân xứng.")

    # 4. Visual Asset Creator
    print("\n[4/6] Visual Asset Creator: Quản lý Cutout & Gán Visual Slots Morph...")
    visual_creator = VisualAssetCreator(ROOT / "assets")
    slides = visual_creator.resolve_visual_slots(slides, tokens)
    print(" -> Đã ánh xạ toàn bộ Cutout, 3D Emblem và Off-screen Coordinates.")

    # 5. Layout Designer
    print("\n[5/6] Layout Designer: Tính toán Grid 16:9 & Render file PPTX...")
    output_pptx = ROOT / "Triet_hoc_Mac_Lenin_Loi_chao.pptx"
    layout_designer = LayoutDesigner(output_pptx)
    # File PPTX chính thức được render với độ tinh xảo cao nhất từ build_deck.py
    # Chạy build_deck.py để đảm bảo toàn vẹn typography gradient & shadow
    import subprocess
    subprocess.run(["python", str(ROOT / "build_deck.py")], check=True)
    subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", str(ROOT / "tools" / "finalize.ps1")], check=True)
    print(" -> Đã biên dịch PPTX & nhúng toàn bộ bản quyền font.")

    # 6. Design QA & Art Critic
    print("\n[6/6] Design QA & Art Critic: Soi ảnh PNG 1080p & Nghiệm thu...")
    qa_critic = DesignQACritic(ROOT)
    qa_report = qa_critic.inspect_and_evaluate(output_pptx)
    print(f"\nKẾT QUẢ NGHIỆM THU: {qa_report.overall_status} (Điểm: {qa_report.score}/10)")
    print(f"Tổng kết: {qa_report.summary}")
    for ticket in qa_report.tickets:
        print(f" - [{ticket.severity}] Slide {ticket.slide_id} ({ticket.category}): {ticket.description}")

    report_file = ROOT / "preview_red" / "qa_report.json"
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(qa_report.__dict__, f, ensure_ascii=False, indent=2, default=str)
    print(f" -> Đã lưu báo cáo QA: {report_file}")
    print("\n" + "=" * 60)
    print("HOÀN TẤT THÀNH CÔNG QUY TRÌNH STUDIO 6 SUB-AGENTS!")
    print("=" * 60)


if __name__ == "__main__":
    main()
