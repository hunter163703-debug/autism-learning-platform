# -*- coding: utf-8 -*-
"""
驗證 public/session5.html 與 public/session6.html 是否完全符合：
1. 無 <video> 標籤
2. 作答欄位無任何 placeholder
3. 各題型與腳本完整性
"""
import re

for filename in ['public/session5.html', 'public/session6.html']:
    print(f"=== 驗證 {filename} ===")
    with open(filename, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. 檢查 <video> 標籤
    videos = re.findall(r'<video[\s\S]*?</video>', html)
    print(f"1. <video> 標籤數量: {len(videos)}")
    if videos:
        print("   警告：發現影片標籤！")

    # 2. 檢查表單內的 placeholder
    form_match = re.search(r'<form id="worksheetForm"[\s\S]*?</form>', html)
    if form_match:
        form_content = form_match.group(0)
        non_empty_ph = re.findall(r'placeholder="([^"]+)"', form_content)
        print(f"2. 表單作答區非空 placeholder 數量: {len(non_empty_ph)}")
        if non_empty_ph:
            print("   發現的非空 placeholder:", non_empty_ph)
        else:
            print("   -> 作答區完全無任何 placeholder 提示，符合純淨作答要求！")
    else:
        print("   錯誤：找不到表單！")

    # 3. 檢查按鈕與核心邏輯
    has_submit = 'submitWorksheet' in html
    has_save = 'saveDraft' in html
    has_modal = 'openStudentModal' in html
    has_teacher = 'loadTeacherDashboard' in html
    has_ai = 'requestAiReview' in html
    print(f"3. 功能完整性: 提交={has_submit}, 暫存={has_save}, 身分登記={has_modal}, 教師儀表板={has_teacher}, AI審閱={has_ai}")
    print()
