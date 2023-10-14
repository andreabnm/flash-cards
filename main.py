from tkinter import *
import pandas
from random import choice

BACKGROUND_COLOR = "#B1DDC6"
WHITE = "#FFFFFF"
BLACK = "#000000"
INITIAL_FILE = "data/french_words.csv"
TO_LEARN_FILE = "data/words_to_learn.csv"

# Load data
curr_word = {}
flip_id = ''
try:
    words_data_frame = pandas.read_csv(TO_LEARN_FILE)
except FileNotFoundError:
    words_data_frame = pandas.read_csv(INITIAL_FILE)
words = words_data_frame.to_dict(orient="records")


def next_card():
    global curr_word, flip_id
    window.after_cancel(flip_id)
    curr_word = choice(words)
    canvas.itemconfig(image, image=image_front)
    canvas.itemconfig(title_text_id, text='French', fill=BLACK)
    canvas.itemconfig(word_text_id, text=curr_word['French'], fill=BLACK)
    flip_id = window.after(3000, flip_card)


def flip_card():
    canvas.itemconfig(image, image=image_back)
    canvas.itemconfig(title_text_id, text='English', fill=WHITE)
    canvas.itemconfig(word_text_id, text=curr_word['English'], fill=WHITE)


def remove_word():
    words.remove(curr_word)
    new_data = pandas.DataFrame(words)
    new_data.to_csv(TO_LEARN_FILE, index=False)


def is_known():
    remove_word()
    next_card()


# GUI
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, background=BACKGROUND_COLOR)
flip_id = window.after(3000, flip_card)

canvas = Canvas(width=800, height=526, highlightthickness=0, background=BACKGROUND_COLOR)
image_front = PhotoImage(file="images/card_front.png")
image_back = PhotoImage(file="images/card_back.png")
image = canvas.create_image(400, 263, image=image_front)
title_text_id = canvas.create_text(400, 150, text='', font=('Arial', 40, 'italic'))
word_text_id = canvas.create_text(400, 263, text='', font=('Arial', 60, 'bold'))
canvas.grid(column=0, row=0, columnspan=2)

wrong_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=wrong_image, highlightthickness=0, command=next_card)
unknown_button.grid(column=0, row=1)
right_image = PhotoImage(file="images/right.png")
known_button = Button(image=right_image, highlightthickness=0, command=is_known)
known_button.grid(column=1, row=1)

next_card()
window.mainloop()
