import tkinter as tk
from tkinter import ttk


# 힘 단위를 뉴턴(N) 기준으로 변환하기 위한 비율
UNIT_TO_NEWTON = {
    "N": 1,
    "kN": 1000,
    "kgf": 9.80665,
    "gf": 0.00980665,
    "lbf": 4.44822
}


def convert_force():
    """변환 버튼을 눌렀을 때 실행되는 함수"""
    try:
        # 입력값 읽기
        value = float(input_entry.get())

        # 선택한 단위 읽기
        from_unit = from_combo.get()
        to_unit = to_combo.get()

        if from_unit == "" or to_unit == "":
            result_label.config(
                text="변환할 단위를 선택하세요.",
                foreground="red"
            )
            return

        # 입력 단위를 뉴턴으로 변환
        value_in_newton = value * UNIT_TO_NEWTON[from_unit]

        # 뉴턴을 결과 단위로 변환
        result = value_in_newton / UNIT_TO_NEWTON[to_unit]

        # 결과 표시
        result_label.config(
            text=f"{value:g} {from_unit} = {result:.6f} {to_unit}",
            foreground="blue"
        )
        history_listbox.insert(
            0,
            f"{value:g} {from_unit} = {result:.6f} {to_unit}"
        )
        if history_listbox.size() > 5:
            history_listbox.delete(5, tk.END)

    except ValueError:
        result_label.config(
            text="숫자를 올바르게 입력하세요.",
            foreground="red"
        )


def reset_form():
    """
    초기화 기능
    숫자와 결과만 지우고,
    선택한 단위는 그대로 유지한다.
    """
    input_entry.delete(0, tk.END)
    result_label.config(text="결과가 여기에 표시됩니다.", foreground="black")
    input_entry.focus()


# 창 생성
window = tk.Tk()
window.title("힘 단위 변환기")
window.geometry("430x500")
window.resizable(False, False)


# 제목
title_label = tk.Label(
    window,
    text="힘 단위 변환기",
    font=("맑은 고딕", 20, "bold")
)
title_label.pack(pady=15)


# 입력 영역
input_frame = tk.Frame(window)
input_frame.pack(pady=5)

tk.Label(
    input_frame,
    text="숫자 입력:",
    font=("맑은 고딕", 11)
).grid(row=0, column=0, padx=5, pady=5)

input_entry = tk.Entry(
    input_frame,
    width=15,
    font=("맑은 고딕", 12)
)
input_entry.grid(row=0, column=1, padx=5, pady=5)


# 단위 선택 영역
unit_frame = tk.Frame(window)
unit_frame.pack(pady=5)

tk.Label(
    unit_frame,
    text="변환 전 단위:",
    font=("맑은 고딕", 11)
).grid(row=0, column=0, padx=5, pady=5)

from_combo = ttk.Combobox(
    unit_frame,
    values=list(UNIT_TO_NEWTON.keys()),
    state="readonly",
    width=8
)
from_combo.grid(row=0, column=1, padx=5, pady=5)
from_combo.set("N")


tk.Label(
    unit_frame,
    text="변환 후 단위:",
    font=("맑은 고딕", 11)
).grid(row=1, column=0, padx=5, pady=5)

to_combo = ttk.Combobox(
    unit_frame,
    values=list(UNIT_TO_NEWTON.keys()),
    state="readonly",
    width=8
)
to_combo.grid(row=1, column=1, padx=5, pady=5)
to_combo.set("kN")


# 버튼 영역
button_frame = tk.Frame(window)
button_frame.pack(pady=15)

convert_button = tk.Button(
    button_frame,
    text="변환",
    width=10,
    command=convert_force
)
convert_button.grid(row=0, column=0, padx=5)

reset_button = tk.Button(
    button_frame,
    text="초기화",
    width=10,
    command=reset_form
)
reset_button.grid(row=0, column=1, padx=5)


# 결과 표시
result_label = tk.Label(
    window,
    text="결과가 여기에 표시됩니다.",
    font=("맑은 고딕", 12)
)
result_label.pack(pady=5)

# 최근 변환 기록
history_label = tk.Label(
    window,
    text="최근 변환 기록",
    font=("맑은 고딕", 11, "bold")
)
history_label.pack(pady=(10, 3))

history_listbox = tk.Listbox(
    window,
    width=42,
    height=5,
    font=("맑은 고딕", 10)
)
history_listbox.pack()


# Enter 키를 누르면 변환
window.bind("<Return>", lambda event: convert_force())


# 프로그램 시작 시 입력창에 커서 표시
input_entry.focus()

window.mainloop()