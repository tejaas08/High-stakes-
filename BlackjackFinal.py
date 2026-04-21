import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import os

def get_card():
    ranks = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
    face = random.choice(ranks)
    value = 10 if face in ['J','Q','K'] else 11 if face == 'A' else int(face)
    return face, value

def calculate_total(cards):
    total = sum(v for _, v in cards)
    aces  = sum(1 for f, v in cards if f == 'A')
    while total > 21 and aces:
        total -= 10
        aces  -= 1
    return total

class BlackjackGame(tk.Toplevel):
    def __init__(self, master, wallet_var, round_counter, on_close):

        super().__init__(master)
        self.wallet_var = wallet_var
        self.on_close = on_close
        self.balance = self.wallet_var.get()

        self.title("21")
        self.attributes("-fullscreen", True)
        self.configure(bg="lightblue")

        self.bet = 0
        self.player_cards = []
        self.dealer_cards = []
        self.card_dir = r"D:\HighStakes\images\cards"
        self.icon_path = r"D:\HighStakes\images\blackjack_icon.png"

        self.player_imgs = []
        self.dealer_imgs = []

        self._build_header()
        self._build_table()
        self._build_controls()
        self.info_lbl.config(text="Place your bet to start")
        self.round_counter = round_counter

    def _build_header(self):
        hdr = tk.Frame(self, bg="lightblue")
        hdr.pack(fill="x", pady=10)
        try:
            icon = Image.open(self.icon_path).resize((40, 40), Image.LANCZOS)
            self.icon_photo = ImageTk.PhotoImage(icon)
            tk.Label(hdr, image=self.icon_photo, bg="lightblue").pack(side="left", padx=(20, 5))
        except Exception as e:
            print("Icon load error:", e)
        tk.Label(hdr, text="21", font=("Lexend", 32, "bold"), fg="black", bg="lightblue").pack(side="left", padx=(0, 20))
        self.balance_lbl = tk.Label(hdr, text=f"Credit Balance: {round(self.balance,2)}", font=("Lexend", 24), fg="black", bg="lightblue")
        self.balance_lbl.pack(side="right", padx=20)

    def _build_table(self):
        tbl = tk.Frame(self, bg="lightblue")
        tbl.pack(expand=True)
        tk.Label(tbl, text="Player:", font=("Lexend", 20), fg="black", bg="lightblue").grid(row=0, column=0, sticky="w", padx=20)
        self.player_frame = tk.Frame(tbl, bg="lightblue")
        self.player_frame.grid(row=1, column=0, padx=20, pady=10)
        tk.Label(tbl, text="Dealer:", font=("Lexend", 20), fg="black", bg="lightblue").grid(row=0, column=1, sticky="w", padx=20)
        self.dealer_frame = tk.Frame(tbl, bg="lightblue")
        self.dealer_frame.grid(row=1, column=1, padx=20, pady=10)
        self.info_lbl = tk.Label(self, text="", font=("Lexend", 18), fg="darkblue", bg="lightblue")
        self.info_lbl.pack(pady=5)

    def _build_controls(self):
        ctl = tk.Frame(self, bg="lightblue")
        ctl.pack(pady=20)
        tk.Label(ctl, text="Bet:", font=("Lexend", 18), fg="black", bg="lightblue").grid(row=0, column=0, padx=5)
        self.bet_entry = tk.Entry(ctl, font=("Lexend", 18), width=6)
        self.bet_entry.grid(row=0, column=1, padx=5)
        tk.Button(ctl, text="Place Bet", font=("Lexend", 18), command=self._place_bet).grid(row=0, column=2, padx=10)

        self.hit_btn = tk.Button(ctl, text="Hit", font=("Lexend", 18), state="disabled", command=self._hit)
        self.hit_btn.grid(row=0, column=3, padx=10)
        self.stand_btn = tk.Button(ctl, text="Stand", font=("Lexend", 18), state="disabled", command=self._stand)
        self.stand_btn.grid(row=0, column=4, padx=10)
        self.new_btn = tk.Button(ctl, text="New Hand", font=("Lexend", 18), state="disabled", command=self._new_hand)
        self.new_btn.grid(row=0, column=5, padx=10)
        tk.Button(ctl, text="Exit", font=("Lexend", 18), command=self.finish).grid(row=0, column=6, padx=10)

    def _place_bet(self):
        try:
            amt = int(self.bet_entry.get())
        except ValueError:
            messagebox.showerror("Invalid", "Enter an integer bet.")
        if amt <= 0 or amt > self.balance:
            messagebox.showerror("Invalid", "Bet must be ≥1 and ≤ your balance.")
            self.wallet_var.set(self.balance)
            

        self.bet = amt
        self.balance -= amt
        self.balance_lbl.config(text=f"Credit Balance: {round(self.balance,2)}")
        self.bet_entry.config(state="disabled")
        self.hit_btn.config(state="normal")
        self.stand_btn.config(state="normal")

        self.player_cards = [get_card(), get_card()]
        self.dealer_cards = [get_card(), get_card()]
        self._refresh_table()

        if calculate_total(self.player_cards) == 21:
            self._stand()
        
        if self.round_counter.get() == 20:
            messagebox.showinfo("Limit Reached", "You’ve completed all 20 Blackjack rounds.")
            self.finish()
            return

        self.round_counter.set(self.round_counter.get() + 1)


    def _refresh_table(self):
        for w in self.player_frame.winfo_children(): w.destroy()
        for w in self.dealer_frame.winfo_children(): w.destroy()
        self.player_imgs.clear()
        self.dealer_imgs.clear()

        for face, _ in self.player_cards:
            img = Image.open(os.path.join(self.card_dir, f"{face}.png")).resize((100, 145), Image.LANCZOS)
            p = ImageTk.PhotoImage(img)
            self.player_imgs.append(p)
            tk.Label(self.player_frame, image=p, bg="lightblue").pack(side="left", padx=5)

        for i, (face, _) in enumerate(self.dealer_cards):
            fn = "back.png" if (i == 1 and self.hit_btn["state"] == "normal") else f"{face}.png"
            img = Image.open(os.path.join(self.card_dir, fn)).resize((100, 145), Image.LANCZOS)
            q = ImageTk.PhotoImage(img)
            self.dealer_imgs.append(q)
            tk.Label(self.dealer_frame, image=q, bg="lightblue").pack(side="left", padx=5)

        pt = calculate_total(self.player_cards)
        dt = calculate_total(self.dealer_cards) if self.hit_btn["state"] == "disabled" else "?"
        self.info_lbl.config(text=f"Player: {pt}    Dealer: {dt}")

    def _hit(self):
        self.player_cards.append(get_card())
        self._refresh_table()
        if calculate_total(self.player_cards) > 21:
            self._end_round()

    def _stand(self):
        self.hit_btn.config(state="disabled")
        self.stand_btn.config(state="disabled")
        while calculate_total(self.dealer_cards) < 17:
            self.dealer_cards.append(get_card())
        self._end_round()

    def _end_round(self):
        p_total = calculate_total(self.player_cards)
        d_total = calculate_total(self.dealer_cards)

        if p_total > 21:
            res = "Bust! You lose."
        elif d_total > 21 or p_total > d_total:
            res = "You win!"
            self.balance += self.bet * 2
        elif p_total == d_total:
            res = "Push."
            self.balance += self.bet
        else:
            res = "You lose."

        self.balance_lbl.config(text=f"Credit Balance: {round(self.balance,2)}")
        self.info_lbl.config(text=f"Player: {p_total}    Dealer: {d_total}    {res}")

        self.hit_btn.config(state="disabled")
        self.stand_btn.config(state="disabled")
        self.new_btn.config(state="normal")

        self._refresh_table()

        if self.balance<=0:
            messagebox.showinfo("No Funds", "You have no funds remaining. The game will now exit. ")
            self.wallet_var.set(self.balance)
            self.quit()
            os._exit(0)

    def _new_hand(self):
        self.bet = 0
        self.player_cards = []
        self.dealer_cards = []
        self.bet_entry.config(state="normal")
        self.bet_entry.delete(0, tk.END)
        self.new_btn.config(state="disabled")
        self.info_lbl.config(text="Place your bet to start")
        self._refresh_table()

    def finish(self):
        self.wallet_var.set(self.balance)
        super().destroy()
        self.on_close()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    wallet = tk.DoubleVar(master=root, value=1000.0)
    app =BlackjackGame(root, wallet, on_close=lambda: root.destroy())
    app.mainloop()
