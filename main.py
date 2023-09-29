from tkinter import *
from tkinter.messagebox import showwarning
import os
import tkinter as tk
import string

show_setting = "*"
font_style = ("Arial", 14, "bold")
font_style_text = ("Arial", 14)
frm = []; btn = []; who = True
playArea = []
standings = []

def registration():
    username = entry_username.get()
    password = entry_password.get()

    if not username or not password:
        showwarning("Регистрация","Пожалуйста, заполните все поля")
        return
    if len(username) <= 2:
        showwarning("Регистрация", "Имя пользователя должно быть длиннее 2 символов")
        return

    if len(password) < 8 or not any(char in password for char in string.punctuation):
        showwarning("Регистрация","Пароль должен быть длиннее 7 символов и содержать хотя бы один специальный символ")
        return

    print(username, password)
    with open("user_data.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            stored_username, _ = line.strip().split('•')
            if username == stored_username:
                showwarning("Регистрация", "Пользователь с таким именем уже существует")
                return

    with open("user_data.txt", "a") as file:
        file.write(f'{username}•{password}\n')
    showwarning("Регистрация", "Регистрация прошла успешно!")
    program_start(username)


def login():
    username = entry_username.get()
    password = entry_password.get()

    if not username or not password:
        showwarning("Авторизация","Пожалуйста, заполните все поля")
        return

    with open("user_data.txt", "r") as file:
        lines = file.readlines()
        user_found = False
        incorrect_password = False

        for line in lines:
            stored_username, stored_password = line.strip().split('•')
            if username == stored_username:
                if password == stored_password:
                    user_found = True
                    program_start(username)
                    break
                else:
                    incorrect_password = True
                    break

        if not user_found or incorrect_password:
            showwarning("Вход", "Неверный логин или пароль")

        return


if not os.path.exists("user_data.txt"):
    with open("user_data.txt", "w"):
        pass




def show_password():
    global show_setting
    if show_setting == "*":
        show_setting = ""
        button_text = "Скрыть пароль"
    else:
        show_setting = "*"
        button_text = "Показать пароль"

    try:
        button_show_password.config(text=button_text)
        entry_password.config(show=show_setting)
    except (NameError):
        pass


def check_winner(board, player):
    for i in range(3):
        if all([cell == player for cell in board[i]]) or all([board[j][i] == player for j in range(3)]):
            return True
    if all([board[i][i] == player for i in range(3)]) or all([board[i][2 - i] == player for i in range(3)]):
        return True
    return False

def evaluate(board):
    if check_winner(board, "X"):
        return 1
    elif check_winner(board, "O"):
        return -1
    else:
        return 0

def minimax(board, depth, alpha, beta, is_maximizing_player):
    if check_winner(board, "X"):
        return 1
    elif check_winner(board, "O"):
        return -1
    elif all([cell != '' for row in board for cell in row]):
        return 0

    if is_maximizing_player:
        max_eval = float("-inf")
        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    board[i][j] = "X"
                    eval = minimax(board, depth + 1, alpha, beta, False)
                    board[i][j] = ""
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
        return max_eval
    else:
        min_eval = float("inf")
        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    board[i][j] = "O"
                    eval = minimax(board, depth + 1, alpha, beta, True)
                    board[i][j] = ""
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return min_eval

def best_move(board):
    best_eval = float("-inf")
    best_move = None
    alpha = float("-inf")
    beta = float("inf")
    for i in range(3):
        for j in range(3):
            if board[i][j] == "":
                board[i][j] = "X"
                eval = minimax(board, 0, alpha, beta, False)
                board[i][j] = ""
                if eval > best_eval:
                    best_eval = eval
                    best_move = (i, j)
                alpha = max(alpha, eval)
    return best_move

def reset_game():
    global board, buttons, player_turn
    board = [['' for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(text="", state="normal", command=lambda row=i, col=j: on_click(row, col))
    player_turn = True
    label.config(text="")

def end_game(winner):
    if winner == "X":
        label.config(text="Бот выиграл!")
    elif winner == "O":
        label.config(text="Вы выиграли!")
    else:
        label.config(text="Ничья!")

    MsgBox = tk.messagebox.askquestion ("Игра окончена","Хотите сыграть еще раз?")
    if MsgBox == "yes":
        reset_game()
    else:
        root.destroy()

def on_click(row, col):
    global board, player_turn
    if board[row][col] == "" and player_turn:
        buttons[row][col].config(text="O", state=tk.DISABLED)
        board[row][col] = "O"
        if check_winner(board, "O"):
            end_game("O")
        elif all([cell != "" for row in board for cell in row]):
            end_game("draw")
        else:
            player_turn = False
            row, col = best_move(board)
            buttons[row][col].config(text="X", state=tk.DISABLED)
            board[row][col] = "X"
            if check_winner(board, "X"):
                end_game("X")
            elif all([cell != "" for row in board for cell in row]):
                end_game("draw")
            else:
                player_turn = True

def program_start(username):

    label_username.destroy(),entry_username.destroy(),label_password.destroy(),entry_password.destroy()
    button_reg.destroy(),button_log.destroy(),button_show_password.destroy()

    global board, player_turn, buttons, label, root

    root.title("Крестики-нолики")
    board = [["" for _ in range(3)] for _ in range(3)]
    player_turn = True
    buttons = [[tk.Button(root, text="", font=("normal", 40), width=5, height=2, command=lambda row=i, col=j: on_click(row, col)) for j in range(3)] for i in range(3)]
    for i in range(3):
        for j in range(3):
            buttons[i][j].grid(row=i, column=j)
    label = tk.Label(root, text="", font=("normal", 16))
    label.grid(row=3, columnspan=3)



root = Tk()
root.resizable (width=False, height=False)
root.title("Регистрация и вход")

width = 495 # Width
height = 530 # Height

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)

root.geometry("%dx%d+%d+%d" % (width, height, x, y))

label_username = Label(root, text="Логин",font= font_style)
label_username.place(x=150, y=20)

entry_username = Entry(root,font= font_style_text)
entry_username.place(x=150, y=50,width=195,height=30)

label_password = Label(root, text="Пароль",font=font_style)
label_password.place(x=150, y=90)

entry_password = Entry(root,show=show_setting,font= font_style_text)
entry_password.place(x=150, y=120,width=195,height=30)

button_reg = Button(root, text="Регистрация",command=registration,font= font_style)
button_reg.place(x=150, y=170,width=195,height=30)

button_log = Button(root, text="Авторизация",command=login,font= font_style)
button_log.place(x=150, y=210,width=195,height=30)

button_show_password = Button(root,text="Показать пароль",command=show_password,font="Arial")
button_show_password.place(x=350,y=120,height=30)

root.mainloop()
