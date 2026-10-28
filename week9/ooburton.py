def on_button_clicked(event):
    print("버튼1이 클릭되었습니다.", event)
    label.config(text= f"버튼1이 클릭되었습니다.{event}")

def on_label_clicked(event):
    print(f"라벨이 클릭되었습니다: {event}")

import tkinter as tk

root = tk.Tk()
root.title("ooburton")
root.geometry("600x400")

label = tk.Label(root, text="객체지향윈도우프로그래밍")
label.bind("<Double-1>", on_label_clicked)
label.pack()

#btni = tk.Button(root, text="클릭해볼까요?", command = on_button_clicked)
btni = tk.Button(root, text="클릭해볼까요?", width = 100, height = 50, fg = "red", bg = "black")
btni.bind("<Double-1>", on_button_clicked)
btni.pack()

root.mainloop()