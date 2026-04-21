import tkinter as tk
import random
import threading
import time
from PIL import Image, ImageTk
from tkinter import messagebox
import os
class CrashGame(tk.Toplevel):
    def __init__(self, master, wallet_var, round_counter, on_close):

        super().__init__(master)
        self.wallet_var = wallet_var
        self.on_close = on_close
        self.balance = self.wallet_var.get()

        self.title("Crash Game")
        self.configure(bg='black')
        self.attributes("-fullscreen", True)

        # ─── Background Image ──────────────────────
        bg_image = Image.open("images/casinobg.png")
        bg_image = bg_image.resize((self.winfo_screenwidth(), self.winfo_screenheight()))
        self.bg_photo = ImageTk.PhotoImage(bg_image)
        self.bg_label = tk.Label(self, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # ─── State ────────────────────────────────
        self.bet = 0.0
        self.multiplier = 1.0
        self.crash_point = 0.0
        self.running = False
        self.cash_out = False

        # ─── Widgets ──────────────────────────────
        self.exit_button = tk.Button(self, text="Exit", font=("Arial", 16), bg="gray", fg="white", command=self.finish)
        self.exit_button.place(x=10, y=10)

        self.balance_label = tk.Label(self, text=f"Balance: ${self.balance:.2f}", font=("Arial", 20), fg="white", bg="black")
        self.balance_label.pack(pady=20)

        tk.Label(self, text="Enter amount:", font=("Arial", 20), fg="white", bg="black").pack(pady=10)

        self.bet_entry = tk.Entry(self, font=("Arial", 16), justify='center')
        self.bet_entry.pack(pady=10)
        self.bet_entry.insert(0, "0.00")

        self.start_button = tk.Button(self, text="Start Game", font=("Arial", 16), command=self.start_game, bg="green", fg="white")
        self.start_button.pack(pady=10)

        self.cashout_button = tk.Button(self, text="CASH OUT", font=("Arial", 18, "bold"), bg="red", fg="white", command=self.cash_out_now)
        self.cashout_button.pack(pady=10)
        self.cashout_button.config(state='disabled')

        self.multiplier_label = tk.Label(self, text="Multiplier: 0.00x", font=("Courier", 32), fg="lime", bg="black")
        self.multiplier_label.pack(pady=40)

        self.result_label = tk.Label(self, text="", font=("Courier", 18), fg="white", bg="black")
        self.result_label.pack(pady=10)
        self.round_counter = round_counter

    def generate_crash_point(self):
        r = random.random()
        if r < 0.01:
            return round(random.uniform(5.0, 10.0), 2)
        elif r < 0.1:
            return round(random.uniform(3.0, 5.0), 2)
        elif r < 0.5:
            return round(random.uniform(2.0, 3.0), 2)
        else:
            return round(random.uniform(1.0, 2.0), 2)

    def start_game(self):
        try:
            self.bet = float(self.bet_entry.get())
        except ValueError:
            self.result_label.config(text="Enter a valid bet amount.")
            return

        if self.bet <= 0 or self.bet > self.balance:
            self.result_label.config(text="Insufficient balance or invalid bet.")
            return

        
        if self.round_counter.get() >= 30:
            messagebox.showinfo("Limit Reached", "You’ve completed all 20 Crash rounds.")
            self.finish()
            return
        self.round_counter.set(self.round_counter.get() + 1)


        self.balance -= self.bet
        self.update_balance()
        self.result_label.config(text="")
        self.multiplier = 0.0
        self.cash_out = False
        self.crash_point = self.generate_crash_point()
        self.cashout_button.config(state='normal')
        self.start_button.config(state='disabled')
        self.running = True

        
        threading.Thread(target=self.run_multiplier, daemon=True).start()

    def run_multiplier(self):
        while self.multiplier < self.crash_point and not self.cash_out:
            time.sleep(0.1)
            self.multiplier += 0.05 + self.multiplier * 0.015
            self.update_multiplier()
        self.end_round()

    def update_multiplier(self):
        self.multiplier_label.config(text=f"Multiplier: {self.multiplier:.2f}x")

    def update_balance(self):
        self.wallet_var.set(self.balance)
        self.balance_label.config(text=f"Balance: ${self.balance:.2f}")

    def cash_out_now(self):
        if self.running:
            self.cash_out = True

    def end_round(self):
        self.running = False
        self.cashout_button.config(state='disabled')
        self.start_button.config(state='normal')

        if self.cash_out:
            win = self.bet * self.multiplier-self.bet
            self.balance += win+self.bet
            self.result_label.config(text=f"✅ Cashed out at {self.multiplier:.2f}x! Your profit is ${win:.2f}")
        else:
            self.result_label.config(text=f"💥 Crashed at {self.crash_point:.2f}x! You lost ${self.bet:.2f}")

        self.update_balance()
        self.multiplier_label.config(text=f"Max Multiplier: {self.crash_point:.2f}x")

        if self.balance<=0:
            messagebox.showinfo("No Funds", "You have no funds remaining. The game will now exit. ")
            self.wallet_var.set(self.balance)
            self.quit()
            os._exit(0)
            
    def finish(self):
        self.wallet_var.set(self.balance)
        self.destroy()
        self.on_close()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    wallet = tk.DoubleVar(master=root, value=1000.0)
    CrashGame(root, wallet, on_close=lambda: root.destroy())
    root.mainloop()
