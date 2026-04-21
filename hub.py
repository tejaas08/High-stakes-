import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import tkinter as tk
from tkinter import messagebox
from BlackjackFinal import BlackjackGame
from crash import CrashGame
from PIL import Image, ImageTk

class GameHub(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Game Hub")
        self.attributes("-fullscreen", True)
        self.configure(bg="lightblue")

        self.wallet = tk.DoubleVar(value=300.0)
        self.crash_rounds = tk.IntVar(value=0)      
        self.blackjack_rounds = tk.IntVar(value=0)

        # ─── Background Image ──────────────────────
        bg_image = Image.open("images/casinobg.png")
        bg_image = bg_image.resize((self.winfo_screenwidth(), self.winfo_screenheight()))
        self.bg_photo = ImageTk.PhotoImage(bg_image)
        self.bg_label = tk.Label(self, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # ─── Overlay Widgets ───────────────────────
        self.main_frame = tk.Frame(self, bg="black")
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(self.main_frame, text="🎰 Welcome to High Stakes", font=("Arial", 30, "bold"),
                 fg="white", bg="black").pack(pady=40)

        self.balance_lbl = tk.Label(self.main_frame, text=f"Balance: ${self.wallet.get():.2f}",
                                    font=("Arial", 20), fg="lime", bg="black")
        self.balance_lbl.pack(pady=10)

        self.round_lbl = tk.Label(self.main_frame, text=self.get_round_text(),
                                  font=("Arial", 18), fg="white", bg="black")
        self.round_lbl.pack(pady=10)

        tk.Button(self.main_frame, text="Play Blackjack", font=("Arial", 20),
                  command=self.launch_blackjack, width=20).pack(pady=10)

        tk.Button(self.main_frame, text="Play Crash", font=("Arial", 20),
                  command=self.launch_crash, width=20).pack(pady=10)

        tk.Button(self.main_frame, text="Exit", font=("Arial", 16), command=self.destroy).pack(pady=40)

        self.update_status_loop()

    def get_round_text(self):
        return (f"🃏 Blackjack Rounds Played: {self.blackjack_rounds.get()}/20    "
                f"💥 Crash Rounds Played: {self.crash_rounds.get()}/30")

    def update_status_loop(self):
        self.balance_lbl.config(text=f"Balance: ${self.wallet.get():.2f}")
        self.round_lbl.config(text=self.get_round_text())
        self.after(500, self.update_status_loop)
        if self.crash_rounds.get() == 30 and self.blackjack_rounds.get() == 20:
            messagebox.showinfo("Game Over", f"🎉 You've completed all 50 rounds!\nFinal Balance: ${self.wallet.get():.2f}")
        

    def launch_blackjack(self):
        if self.blackjack_rounds.get() < 20:
            BlackjackGame(self, self.wallet, self.blackjack_rounds, self.focus_force)
        else:
            messagebox.showinfo("Limit Reached", "You’ve completed all 20 rounds of Blackjack.")

    def launch_crash(self):
        if self.crash_rounds.get() < 20:
            CrashGame(self, self.wallet, self.crash_rounds, self.focus_force)
        else:
            messagebox.showinfo("Limit Reached", "You’ve completed all 20 rounds of Crash.")

if __name__ == "__main__":
    app = GameHub()
    app.mainloop()
