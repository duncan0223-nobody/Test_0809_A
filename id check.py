"""台灣國民身分證字號檢查視窗程式。"""

import tkinter as tk
from tkinter import ttk


# 英文字母對應的身分證字號編碼。
LETTER_CODES = {
    letter: code
    for letter, code in zip(
        "ABCDEFGHJKLMNPQRSTUVXYWZIO",  # 官方編碼使用的字母順序
        range(10, 36),
    )
}


def is_valid_taiwan_id(id_number: str) -> bool:
    """判斷是否為有效的台灣國民身分證字號。

    規則：一個英文字母、9 個數字，第二碼為 1 或 2，且通過檢查碼。
    """
    id_number = id_number.strip().upper()

    if len(id_number) != 10:
        return False
    if id_number[0] not in LETTER_CODES:
        return False
    if id_number[1] not in "12" or not id_number[1:].isdigit():
        return False

    code = LETTER_CODES[id_number[0]]
    total = (code // 10) + (code % 10) * 9
    weights = (8, 7, 6, 5, 4, 3, 2, 1, 1)
    total += sum(int(digit) * weight for digit, weight in zip(id_number[1:], weights))
    return total % 10 == 0


def check_id(event=None) -> None:
    """讀取輸入欄位並顯示檢查結果。"""
    id_number = id_entry.get().strip().upper()
    id_entry.delete(0, tk.END)
    id_entry.insert(0, id_number)

    if is_valid_taiwan_id(id_number):
        result_label.config(text="✓ 身分證字號格式與檢查碼正確", foreground="#16803c")
    else:
        result_label.config(text="✗ 身分證字號不正確，請重新確認", foreground="#c62828")


root = tk.Tk()
root.title("台灣身分證字號驗證")
root.geometry("460x240")
root.resizable(False, False)

frame = ttk.Frame(root, padding=28)
frame.pack(expand=True, fill="both")

ttk.Label(frame, text="台灣國民身分證字號驗證", font=("Arial", 16, "bold")).pack(pady=(0, 20))
ttk.Label(frame, text="請輸入 1 個英文字母與 9 個數字：").pack(anchor="w")

id_entry = ttk.Entry(frame, font=("Arial", 15), justify="center")
id_entry.pack(fill="x", pady=(6, 14))
id_entry.focus()

ttk.Button(frame, text="開始驗證", command=check_id).pack()
result_label = ttk.Label(frame, text="")
result_label.pack(pady=(16, 0))

root.bind("<Return>", check_id)
root.mainloop()
