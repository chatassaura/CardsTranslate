from tkinter import *
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"
TEXT1 = ("Ariel", 40, "italic")
TEXT2 = ("Ariel", 60, "bold")
current_card = ''
flip_timer = ''


try:
    data = pd.read_csv('data/words_to_learn.csv')
except FileNotFoundError:
    original_data = pd.read_csv('data/french_words.csv')
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(img_canvas, image=img_card_front)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    flip_timer = window.after(3000, func=flip_card)


def btn_right_click():
    to_learn.remove(current_card)
    new_data = pd.DataFrame(to_learn)
    new_data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


def btn_wrong_click():
    next_card()


def flip_card():
    canvas.itemconfig(img_canvas, image=img_card_back)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")


window = Tk()
window.title('Flashy')
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526)
img_card_front = PhotoImage(file="images\\card_front.png")
img_card_back = PhotoImage(file="images\\card_back.png")
img_canvas = canvas.create_image(400, 263, image=img_card_front)
card_title = canvas.create_text(400, 150, font=TEXT1)
card_word = canvas.create_text(400, 263, font=TEXT2)

canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

my_image_wrong = PhotoImage(file='images\\wrong.png')
btn_wrong = Button(image=my_image_wrong, highlightthickness=0, command=btn_wrong_click)
btn_wrong.grid(column=0, row=1)

my_image_right = PhotoImage(file='images\\right.png')
btn_right = Button(image=my_image_right, highlightthickness=0, command=btn_right_click)
btn_right.grid(column=1, row=1)

next_card()
window.mainloop()
