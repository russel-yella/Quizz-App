from tkinter import *
from quiz_brain import QuizBrain

BG_COLOR = "#1E1E2F"
CARD_COLOR = "#2A2A40"
ACCENT = "#6C63FF"
TEXT_COLOR = "#FFFFFF"
SUCCESS = "#4CAF50"
ERROR = "#E63946"

class QuizInterface:

    def __init__(self, quiz_brain: QuizBrain):

        self.quiz = quiz_brain

        self.window = Tk()
        self.window.title("Quiz App")
        self.window.config(bg=BG_COLOR, padx=40, pady=40)

        # ===== TOP BAR =====

        self.timer_label = Label(
            text="⏱ 10",
            font=("Segoe UI", 12, "bold"),
            bg=BG_COLOR,
            fg=ACCENT
        )
        self.timer_label.grid(row=0, column=0, sticky="w")

        self.score_label = Label(
            text="Score 0",
            font=("Segoe UI", 12, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR
        )
        self.score_label.grid(row=0, column=1, sticky="e")

        # ===== QUESTION CARD =====

        self.canvas = Canvas(
            width=480,
            height=240,
            bg=CARD_COLOR,
            highlightthickness=0
        )

        self.question_text = self.canvas.create_text(
            240,
            120,
            width=420,
            text="Question appears here",
            fill=TEXT_COLOR,
            font=("Segoe UI", 18, "bold"),
            justify="center"
        )

        self.canvas.grid(row=1, column=0, columnspan=2, pady=50)

        # ===== BUTTONS =====

        button_frame = Frame(self.window, bg=BG_COLOR)
        button_frame.grid(row=2, column=0, columnspan=2)

        self.true_button = Button(
            button_frame,
            text="✔ TRUE",
            font=("Segoe UI", 13, "bold"),
            bg=ACCENT,
            fg="white",
            activebackground="#5750d4",
            width=14,
            height=2,
            bd=0,
            cursor="hand2",
            command=self.true_pressed
        )

        self.true_button.grid(row=0, column=0, padx=20)

        self.false_button = Button(
            button_frame,
            text="✖ FALSE",
            font=("Segoe UI", 13, "bold"),
            bg="#3A3A55",
            fg="white",
            activebackground="#2E2E44",
            width=14,
            height=2,
            bd=0,
            cursor="hand2",
            command=self.false_pressed
        )

        self.false_button.grid(row=0, column=1, padx=20)

        # hover effects
        self.true_button.bind("<Enter>", lambda e: self.true_button.config(bg="#5750d4"))
        self.true_button.bind("<Leave>", lambda e: self.true_button.config(bg=ACCENT))

        self.false_button.bind("<Enter>", lambda e: self.false_button.config(bg="#2E2E44"))
        self.false_button.bind("<Leave>", lambda e: self.false_button.config(bg="#3A3A55"))

        # ===== TIMER =====

        self.time_left = 10
        self.timer_id = None

        self.get_next_question()

        self.window.mainloop()

    def get_next_question(self):

        self.canvas.config(bg=CARD_COLOR)

        if self.quiz.still_has_questions():

            self.score_label.config(
                text=f"Score {self.quiz.score}"
            )

            q_text = self.quiz.next_question()

            self.canvas.itemconfig(
                self.question_text,
                text=q_text
            )

            self.time_left = 10
            self.update_timer()

        else:

            self.canvas.itemconfig(
                self.question_text,
                text=f"Quiz Complete 🎉\nFinal Score: {self.quiz.score}"
            )

            self.true_button.config(state="disabled")
            self.false_button.config(state="disabled")

    def update_timer(self):

        self.timer_label.config(
            text=f"⏱ {self.time_left}"
        )

        if self.time_left > 0:

            self.time_left -= 1

            self.timer_id = self.window.after(
                1000,
                self.update_timer
            )

        else:

            self.give_feedback(False)

    def true_pressed(self):

        if self.timer_id:
            self.window.after_cancel(self.timer_id)

        self.give_feedback(
            self.quiz.check_answer("True")
        )

    def false_pressed(self):

        if self.timer_id:
            self.window.after_cancel(self.timer_id)

        self.give_feedback(
            self.quiz.check_answer("False")
        )

    def give_feedback(self, is_right):

        if is_right:
            self.canvas.config(bg=SUCCESS)
        else:
            self.canvas.config(bg=ERROR)

        self.window.after(
            700,
            self.get_next_question
        )