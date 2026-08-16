#!/home/pi/Documents/github/Test_0809_A/.venv/bin/python3
# -*- coding: utf-8 -*-
"""台灣身分證字號驗證器 — Gradio 網頁介面"""

import gradio as gr

# 英文字母對應的地區代碼(數字)
letter_to_num = {
    'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15,
    'G': 16, 'H': 17, 'I': 34, 'J': 18, 'K': 19, 'L': 20,
    'M': 21, 'N': 22, 'O': 35, 'P': 23, 'Q': 24, 'R': 25,
    'S': 26, 'T': 27, 'U': 28, 'V': 29, 'W': 32, 'X': 30,
    'Y': 31, 'Z': 33
}


def check_id(id_no):
    """檢查台灣身分證字號是否正確,回傳 (是否正確, 訊息)"""
    id_no = id_no.strip().upper()

    # 1. 檢查長度是否為 10
    if len(id_no) != 10:
        return False, "錯誤!長度必須為 10 碼,你輸入了 %d 碼(正確格式範例:A123456789)" % len(id_no)

    # 2. 檢查第 1 碼是否為英文字母
    if not id_no[0].isalpha():
        return False, "錯誤!第 1 碼必須是英文字母 A~Z(正確格式範例:A123456789)"

    # 3. 檢查第 2 碼是否為性別碼(1 或 2)
    if id_no[1] not in ('1', '2'):
        return False, "錯誤!第 2 碼必須是性別碼 1(男)或 2(女),你輸入了 %s" % id_no[1]

    # 4. 檢查第 3~10 碼是否為數字
    if not id_no[2:].isdigit():
        return False, "錯誤!第 3~10 碼必須是數字,請檢查是否有英文字母或符號"

    # 5. 計算檢查碼
    # 字母轉成兩位數字,十位數 ×1,個位數 ×9
    code = letter_to_num[id_no[0]]
    total = (code // 10) * 1 + (code % 10) * 9

    # 其餘 9 位數字依序 × 8, 7, 6, 5, 4, 3, 2, 1, 1
    weights = [8, 7, 6, 5, 4, 3, 2, 1, 1]
    for d, w in zip(id_no[1:], weights):
        total += int(d) * w

    # 總和必須是 10 的倍數
    if total % 10 == 0:
        return True, "身分證字號正確"
    else:
        return False, "錯誤!檢查碼不符,此身分證字號不存在"


def validate_ui(id_no):
    """Gradio 介面用的驗證函式"""
    if not id_no or not id_no.strip():
        return "請輸入身分證字號"
    ok, msg = check_id(id_no)
    return f"✓ {msg}({id_no.strip().upper()})" if ok else f"✗ {msg}"


with gr.Blocks(title="台灣身分證字號驗證器") as demo:
    gr.Markdown("# 台灣身分證字號驗證器")
    gr.Markdown(
        "格式:**1 個大寫英文字母 + 9 位數字**(共 10 碼)\n"
        "第 2 碼為性別碼:1(男)/2(女),最後 1 碼為檢查碼"
    )

    with gr.Row():
        id_input = gr.Textbox(
            label="身分證字號",
            placeholder="請輸入身分證字號,例:A123456789",
            max_lines=1,
            scale=3,
        )
        output = gr.Textbox(label="驗證結果", interactive=False, scale=2)

    btn = gr.Button("確認", variant="primary")
    btn.click(validate_ui, inputs=id_input, outputs=output)
    id_input.submit(validate_ui, inputs=id_input, outputs=output)

    gr.Examples(
        examples=["A123456789", "B276543214", "B123456789", "A12345678"],
        inputs=id_input,
    )


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
