#!/home/pi/Documents/github/Test_0809_A/.venv/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import html
import urllib.parse

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


def get_input():
    """讀取表單輸入(GET 或 POST 皆可)"""
    method = os.environ.get("REQUEST_METHOD", "GET").upper()
    if method == "POST":
        try:
            length = int(os.environ.get("CONTENT_LENGTH", "0"))
            body = sys.stdin.buffer.read(length).decode("utf-8", "replace")
        except Exception:
            body = ""
    else:
        body = os.environ.get("QUERY_STRING", "")

    params = urllib.parse.parse_qs(body, keep_blank_values=True)
    return params.get("id", [""])[0]


def render_page(id_input="", result_html=""):
    """輸出完整 HTML 頁面"""
    esc = html.escape(id_input)
    result_block = result_html if result_html else ""
    page = f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>台灣身分證字號驗證器</title>
<style>
body {{ font-family: sans-serif; max-width: 480px; margin: 40px auto; text-align: center; }}
h1 {{ color: #333; }}
form {{ margin: 20px 0; }}
input[type=text] {{ font-size: 20px; padding: 8px; letter-spacing: 3px; text-align: center; width: 240px; }}
button {{ font-size: 16px; padding: 8px 24px; margin: 8px; cursor: pointer; }}
.ok {{ color: green; font-weight: bold; font-size: 18px; }}
.err {{ color: red; font-weight: bold; font-size: 18px; }}
.hint {{ color: gray; font-size: 14px; }}
</style>
</head>
<body>
<h1>台灣身分證字號驗證器</h1>
<p class="hint">格式:1 個大寫英文字母 + 9 位數字(共 10 碼)</p>
<form method="post" action="id_check.py">
<input type="text" name="id" maxlength="10" placeholder="請輸入身分證字號" value="{esc}" autofocus>
<br>
<button type="submit">確認</button>
<button type="reset">清除</button>
</form>
{result_block}
<p class="hint">範例:A123456789(正確)&nbsp;|&nbsp;B123456789(錯誤)</p>
</body>
</html>
"""
    return page


def main():
    id_input = get_input()
    result_html = ""
    if id_input:
        ok, msg = check_id(id_input)
        if ok:
            result_html = f'<p class="ok">✓ {html.escape(msg)}<br>身分證字號:{html.escape(id_input)}</p>'
        else:
            result_html = f'<p class="err">✗ {html.escape(msg)}</p>'

    page = render_page(id_input, result_html)
    sys.stdout.buffer.write(
        ("Content-Type: text/html; charset=utf-8\r\n\r\n" + page).encode("utf-8")
    )


if __name__ == "__main__":
    main()
