from tkinter import *
from tkinter import messagebox
import random

root = Tk()
root.title('OX Game')
root.config(bg="lightgreen")  # Thay đổi màu nền thành xanh lá nhạt

clicked = True  # Người chơi bắt đầu với X
count = 0
difficulty = "Easy"  # Độ khó mặc định
game_mode = "Single Player"  # Chế độ chơi mặc định
player_mark = "X"  # Ký hiệu mặc định của người chơi

def disableButtons():
    for row in buttons:
        for button in row:
            button.config(state=DISABLED)

def checkWinner():
    global win
    win = False
    
    # Kiểm tra các hàng
    for row in range(6):
        for col in range(6 - 4):
            if (buttons[row][col]["text"] == buttons[row][col+1]["text"] == 
                buttons[row][col+2]["text"] == buttons[row][col+3]["text"] == 
                buttons[row][col+4]["text"] != " "):
                for i in range(5):
                    buttons[row][col+i].config(bg="#80ffaa")
                win = True
                messagebox.showinfo("OX Game", f"Người chơi {'1' if buttons[row][col]['text'] == 'X' else '2'} THẮNG!!")
                disableButtons()
                return

    # Kiểm tra các cột
    for col in range(6):
        for row in range(6 - 4):
            if (buttons[row][col]["text"] == buttons[row+1][col]["text"] == 
                buttons[row+2][col]["text"] == buttons[row+3][col]["text"] == 
                buttons[row+4][col]["text"] != " "):
                for i in range(5):
                    buttons[row+i][col].config(bg="#80ffaa")
                win = True
                messagebox.showinfo("OX Game", f"Người chơi {'1' if buttons[row][col]['text'] == 'X' else '2'} THẮNG!!")
                disableButtons()
                return

    # Kiểm tra đường chéo (từ trái trên xuống phải dưới)
    for row in range(6 - 4):
        for col in range(6 - 4):
            if (buttons[row][col]["text"] == buttons[row+1][col+1]["text"] == 
                buttons[row+2][col+2]["text"] == buttons[row+3][col+3]["text"] == 
                buttons[row+4][col+4]["text"] != " "):
                for i in range(5):
                    buttons[row+i][col+i].config(bg="#80ffaa")
                win = True
                messagebox.showinfo("OX Game", f"Người chơi {'1' if buttons[row][col]['text'] == 'X' else '2'} THẮNG!!")
                disableButtons()
                return

    # Kiểm tra đường chéo (từ trái dưới lên phải trên)
    for row in range(4, 6):
        for col in range(6 - 4):
            if (buttons[row][col]["text"] == buttons[row-1][col+1]["text"] == 
                buttons[row-2][col+2]["text"] == buttons[row-3][col+3]["text"] == 
                buttons[row-4][col+4]["text"] != " "):
                for i in range(5):
                    buttons[row-i][col+i].config(bg="#80ffaa")
                win = True
                messagebox.showinfo("OX Game", f"Người chơi {'1' if buttons[row][col]['text'] == 'X' else '2'} THẮNG!!")
                disableButtons()
                return

def checkDraw():
    global count, win
    if count == 36 and not win:
        messagebox.showinfo("OX Game", "HÒA!!")
        start()

def buttonClicked(button):
    global clicked, count, player_mark
    if button["text"] == " ":
        if clicked:
            button["text"] = player_mark
            button.config(fg="red", bg="lightblue")  # Đặt màu cho X
            count += 1
            checkWinner()
            checkDraw()
            if game_mode == "Single Player" and not win:
                computerMove()
            else:
                clicked = not clicked  # Chuyển lượt trong chế độ Hai Người Chơi
        elif game_mode == "Two Players":  # Lượt của người chơi O
            button["text"] = "O"
            button.config(fg="green", bg="lightgreen")  # Đặt màu cho O
            count += 1
            checkWinner()
            checkDraw()
            clicked = not clicked

def computerMove():
    global clicked, count

    # Xác định ký hiệu của máy (ngược với ký hiệu của người chơi)
    computer_mark = "O" if player_mark == "X" else "X"

    def findBestMove(mark):
        for row in range(6):
            for col in range(6 - 5):
                line = [buttons[row][col+i] for i in range(6)]
                if line.count(mark) == 5 and line.count(" ") == 1:
                    return line[line.index(" ")]

        for col in range(6):
            for row in range(6 - 5):
                line = [buttons[row+i][col] for i in range(6)]
                if line.count(mark) == 5 and line.count(" ") == 1:
                    return line[line.index(" ")]

        return None

    best_move = None

    if difficulty == "Easy":
        available_buttons = [(r, c) for r in range(6) for c in range(6) if buttons[r][c]["text"] == " "]
        if available_buttons:
            row, col = random.choice(available_buttons)
            best_move = buttons[row][col]

    elif difficulty == "Medium":
        best_move = findBestMove("X")  # Chặn người chơi nếu họ sắp thắng

        if not best_move:
            available_buttons = [(r, c) for r in range(6) for c in range(6) if buttons[r][c]["text"] == " "]
            if available_buttons:
                row, col = random.choice(available_buttons)
                best_move = buttons[row][col]

    elif difficulty == "Hard":
        best_move = findBestMove("O")  # Thử thắng nếu có thể
        if not best_move:
            best_move = findBestMove("X")  # Thử chặn người chơi nếu họ sắp thắng

        if not best_move:
            if buttons[2][2]["text"] == " ":
                best_move = buttons[2][2]
            elif buttons[3][3]["text"] == " ":
                best_move = buttons[3][3]
            else:
                available_buttons = [(r, c) for r in range(6) for c in range(6) if buttons[r][c]["text"] == " "]
                if available_buttons:
                    row, col = random.choice(available_buttons)
                    best_move = buttons[row][col]

    if best_move:
        best_move["text"] = computer_mark
        best_move.config(fg="green")  # Đặt màu cho O
        count += 1
        checkWinner()
        checkDraw()
        clicked = True  # Chuyển lượt về cho người chơi

def setDifficulty(selected_difficulty):
    global difficulty
    difficulty = selected_difficulty
    start()

def setGameMode(mode):
    global game_mode
    game_mode = mode
    start()  # Khởi động lại trò chơi với chế độ mới

def setPlayerMark(mark):
    global player_mark
    player_mark = mark
    start()  # Khởi động lại trò chơi với ký hiệu đã chọn

def start():
    global buttons, clicked, count, win
    clicked = True
    count = 0
    win = False
    
    # Xóa các widget trước đó
    for widget in root.winfo_children():
        widget.grid_forget()

    # Hiển thị lựa chọn ký hiệu của người chơi
    mark_menu = Frame(root)
    Label(mark_menu, text="Chọn X hoặc O:").pack(side=LEFT)
    Button(mark_menu, text="X", command=lambda: setPlayerMark("X")).pack(side=LEFT)
    Button(mark_menu, text="O", command=lambda: setPlayerMark("O")).pack(side=LEFT)
    mark_menu.grid(row=7, column=0, columnspan=6, pady=10)

    # Hiển thị lựa chọn chế độ chơi
    mode_menu = Frame(root)
    Label(mode_menu, text="Chế độ chơi:").pack(side=LEFT)
    Button(mode_menu, text="Chơi với máy", command=lambda: setGameMode("Single Player")).pack(side=LEFT)
    Button(mode_menu, text="Chơi với người", command=lambda: setGameMode("Two Players")).pack(side=LEFT)
    mode_menu.grid(row=8, column=0, columnspan=6, pady=10)

    # Hiển thị lựa chọn độ khó (chỉ ảnh hưởng trong chế độ Single Player)
    difficulty_menu = Frame(root)
    Label(difficulty_menu, text="Chọn độ khó:").pack(side=LEFT)
    Button(difficulty_menu, text="Dễ", command=lambda: setDifficulty("Easy")).pack(side=LEFT)
    Button(difficulty_menu, text="Trung Bình", command=lambda: setDifficulty("Medium")).pack(side=LEFT)
    Button(difficulty_menu, text="Khó", command=lambda: setDifficulty("Hard")).pack(side=LEFT)
    difficulty_menu.grid(row=9, column=0, columnspan=6, pady=10)

    # Khởi tạo các nút
    buttons = [[Button(root, text=" ", font=("Helvetica", 15), height=2, width=5, bg="lightgrey",
                       command=lambda r=r, c=c: buttonClicked(buttons[r][c])) for c in range(6)] for r in range(6)]

    for r in range(6):
        for c in range(6):
            buttons[r][c].grid(row=r, column=c)

start()
root.mainloop()
