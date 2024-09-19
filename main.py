from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}

try:
    data = pandas.read_csv(filepath_or_buffer="data/words_to_know.csv")
except FileNotFoundError:
    original_data = pandas.read_csv(filepath_or_buffer="data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    french_word = (current_card.get("French"))
    canvas.itemconfig(dic_title, text="French", fill="black")
    canvas.itemconfig(dic_word, text=french_word, fill="black")
    canvas.itemconfig(front_bg, image=front_image)

    flip_timer = window.after(3000, flip_card)


def unknown_card():
    to_learn.remove(current_card)
    print(to_learn)
    new_data = pandas.DataFrame(to_learn)
    new_data.to_csv("data/words_to_know.csv", index=False)
    next_card()


def flip_card():
    canvas.itemconfig(dic_title, text="English", fill="white")
    canvas.itemconfig(dic_word, text=current_card.get("English"), fill="white")
    canvas.itemconfig(front_bg, image=back_image)


window = Tk()
window.title("Flasky")
window.config(padx=30, pady=30, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, flip_card)

canvas = Canvas(width=800, height=578)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
front_image = PhotoImage(file="images/card_front.png")
back_image = PhotoImage(file="images/card_back.png")

front_bg = canvas.create_image(400, 289, image=front_image)

dic_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
dic_word = canvas.create_text(400, 265, text="", font=("Ariel", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

unknown_button_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=unknown_button_image, command=next_card)

right_button_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_button_image, command=unknown_card)

unknown_button.grid(column=0, row=1)
right_button.grid(column=1, row=1)

next_card()

window.mainloop()
