import tkinter as tk
from tkinter import messagebox
import random
from PIL import Image, ImageTk
import os 
# Sample question data — replace with actual
easy_q = [
    "You are given a string s = 'ProgrammingInPython'. Write the output of the expression s[3:10][::-1] + s[0] + s[-1]. What final string is produced after this slicing, reversing, and concatenation?",
    "Consider the list lst = [10, 20, 30, 40, 50]. If we perform the operations lst.pop(2), followed by lst.insert(1, 99), and then lst.append(lst[0] + lst[-1]), what will be the value at index 3 of the final list?",
    "Given the tuple t = ('a', 'b', 'c', 'd', 'e'), what will be the output of the expression t[1:4][::-1][1]? Explain how slicing and reversing affect the final result.",
    "You are given a dictionary d = {'x': 5, 'y': 10}. If the following operations are performed: d['z'] = d.get('x') + d.get('a',3), and then d['x'] = d['z'] - d['y'], what is the final value of d['x']?",
    "Given the string s = 'banana', what will be the output of the expression s.replace('a', '*', 2).upper()[::-1]?",
    "Consider the list nums = [1, 2, 3, 4, 5]. If we execute nums = nums[::2] + nums[1::2], and then access nums[3], what value is returned?",
    "You are given a dictionary d = dict.fromkeys(['a', 'b', 'c'], 1). If we then execute d['b'] += 4 and d['c'] = d['a'] + d['b'], what is the value of d['c']?",
    "Given the string s = 'PythonIsFun', what is the output of s[::2] + s[::-3]? Provide the final string after both slicing operations and concatenation.",
    "Consider the tuple t = tuple('abcdef'). What will be the result of t.index('d') + len(t[2:5])?",
    "You are given a list l = ['apple', 'banana', 'cherry']. If we execute l[1] = l[1].replace('a', '@'), and then l[2] = l[2][::-1], what is the final value of l[2]?"
]

easy_ans = [
    "nimmargPn",
    '40',
    "c",
    '-2',
    "AN*N*B",
    '2',
    '6',
    "PtoIFnnsoy",
    '6',
    "yrrehc"
]




medium_q = [
    "Given the string s = 'DataStructuresAndAlgorithms', what will be the output of s[s.find('S'):s.find('A')].lower()[::-1]?",
    "You are given a list lst = [1, 2, 3, 4, 5]. If we perform the following operations: lst = lst[1:-1], then lst.insert(1, lst.pop()), and finally lst.append(lst[0] + lst[1]), what is the final value of lst[-1]?",
    "Consider the dictionary d = {'a': 1, 'b': 2, 'c': 3}. If we execute d['b'] = d['a'] + d['c'], and then d['a'] = d['b'] * 2, what is the final value of d['a']?",
    "Given the string s = 'abracadabra', what is the output of s.replace('a', 'X', 3)[::-1][2:7]?",
    "You are given a tuple t = (10, 20, 30, 40, 50). If you convert it to a list, remove the second element, insert 25 at index 1, and then convert it back to a tuple, what is the value at index 2?",
    "Given the dictionary d = {'x': 1, 'y': 2}, if we execute d['z'] = d['x'] * d['y'] + len(d), and then d['x'] = d['z'] - d['y'], what is the final value of d['x']?",
    "Consider the string s = 'abcdefghij'. What is the output of s[1::3] + s[::-4]?",
    "You are given a list l = [5, 10, 15, 20]. If we execute l = l[::-1], then l[1] = l[1] + l[2], and finally l.pop(0), what is the new first element of the list?",
    "Given the dictionary d = {'a': 1, 'b': 2, 'c': 3}, what is the output of sum([v for k, v in d.items() if k != 'b'])?",
    "You are given a string s = 'MachineLearning'. What is the output of s[s.index('L'):].replace('n', '*')[::-1]?"
]

medium_ans = [
    "serutcurts",
    '6',
    '8',
    "badXc",
    '30',
    '2',
    "behjgb",
    '25',
    '4',
    "g*i*raeL"
]




hard_q = [
    "You are given a string s = 'ArtificialIntelligence'. Perform the following operations in sequence: convert the string to lowercase, extract all characters from index 2 to index 15 (inclusive of 2, exclusive of 16), reverse the extracted substring, and from the reversed string, extract every second character starting from index 1. Finally, return the resulting string.",
    "You are given a list l = [1, 2, 3, 4, 5]. If we perform l = [x**2 for x in l if x % 2 == 1], then l.insert(1, l.pop()), and finally l.append(sum(l)), what is the final value of l[-1]?",
    "Consider the dictionary d = {'a': 5, 'b': 10, 'c': 15}. If we execute d['d'] = d['a'] + d['c'], then d['b'] = d['d'] - d['b'], and finally d['a'] = d['b'] * 2, what is the final value of d['a']?",
    "Given the string s = 'DataScienceWithPython', what is the output of ''.join([s[i] for i in range(len(s)) if i % 4 == 0])[::-1]?",
    "You are given a tuple t = tuple(range(1, 11)). If we convert it to a list, remove all even numbers, reverse the list, and then access the second element, what is the result?",
    "Consider the dictionary d = {'x': 2, 'y': 4, 'z': 6}. If we execute d['x'] = d['y'] * d['z'], then d['z'] = d['x'] // d['y'], and finally d['y'] = d['z'] + d['x'], what is the final value of d['y']?",
    "Given the string s = 'abcdefghijklmno', what is the output of s[::3] + s[::-5]?",
    "You are given a list l = [10, 20, 30, 40, 50]. If we slice it as l[1:4], reverse that slice, insert the sum of the slice at the beginning, and then access the last element, what is the result?",
    "You are given a dictionary d = {'alpha': 3, 'beta': 6, 'gamma': 9}. Perform the following operations: add a new key 'delta' whose value is the product of 'alpha' and 'beta'; update the value of 'beta' to be the difference between 'delta' and 'gamma'; replace the value of 'alpha' with the sum of all current values in the dictionary. What is the final value of the key 'alpha'?",
    "You are given a string s = 'DeepLearningModels' and asked to perform the following transformations: extract every second character starting from index 1 and store it in a variable a; reverse the original string and extract every third character starting from index 0, storing it in variable b; concatenate a and b, then return the character at index 10 of the resulting string. What is the final character at that position?"
]

hard_ans = [
    "ltiacft",
    '35',
    '20',
    "nyinSD",
    '7',
    '30',
    "adgjmoje",
    '50',
    '39',
    "d"
]

total_rounds = 10

class QuizApp:


    def __init__(self, root):
        self.root = root
        self.root.title("Round 1 Quiz")
        self.root.attributes("-fullscreen", True)
        self.credits = 0
        self.round = 0
        self.correct_answer = None
        self.difficulty = None

        #tracking variables
        self.question_history = []
        self.current_question_index = -1
        self.answered_questions = set()

        # Load and display background image
        bg_image = Image.open("images/casinobg.png")
        bg_image = bg_image.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()))
        self.bg_photo = ImageTk.PhotoImage(bg_image)

        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)


        # === Layout Frames ===
        self.main_frame = tk.Frame(root, bg="#3f42d6", padx=40, pady=40)
        self.main_frame.place(relx=0.5,rely=0.5,anchor="center")
        self.main_frame.pack(expand=True, fill='both')

        self.question_label = tk.Label(self.main_frame, text="Click on Next to get your first question",
                                       font=('Consolas', 22), fg="white", bg="#3f42d6", wraplength=1000, justify='center')
        self.question_label.pack(pady=(0, 30))

        self.answer_entry = tk.Entry(self.main_frame, font=('Consolas', 18), width=40, justify='center')
        self.answer_entry.pack(pady=(0, 20))

        self.submit_button = tk.Button(self.main_frame, text="Submit Answer", font=('Consolas', 16),
                                       command=self.check_answer, bg="#28a745", fg="white", padx=20, pady=10)
        self.submit_button.pack(pady=(0, 30))

        self.difficulty_frame = tk.Frame(self.main_frame, bg="#3f42d6")
        self.difficulty_frame.pack(pady=(0, 20))
        self.previous_btn = tk.Button(self.difficulty_frame, text="Previous", font=('Consolas', 14),
                               command=self.load_previous_question, bg="#ffc107", fg="black", padx=20, pady=10)
        self.previous_btn.pack(side='left', padx=20)

        self.next_btn = tk.Button(self.difficulty_frame, text="Next", font=('Consolas', 14),
                               command=self.load_next_question, bg="#6f42c1", fg="white", padx=20, pady=10)
        self.next_btn.pack(side='left', padx=20)

        self.balance_label = tk.Label(self.main_frame, text=f"Balance: {self.credits} credits",
                                      font=('Consolas', 18, 'bold'), fg="white", bg="#3f42d6")
        self.balance_label.pack(pady=(30, 10))

        self.exit_button = tk.Button(self.main_frame, text="Press This Button To Exit", font=('Consolas', 12),
                                     command=root.quit, bg="#a72828", fg="white")
        self.exit_button.pack(pady=30)


        
   
        self.instructions_label = tk.Label(self.root,
        text="Instructions:\n"
            "+50 for Easy, +100 for Medium, +250 for Hard\n"
             "-100 for any wrong answer\n"
             "To view next question, click Next\n" 
             "To view previous question, click Previous\n"
             "Once an answer has been submitted, there is no resubmission\n",
        font=('Consolas', 12), fg="white", bg="#3f42d6", justify='left')
        self.instructions_label.place(relx=0.02, rely=0.8, anchor='w')


    def load_question(self, difficulty):
        if self.round >= total_rounds:
            messagebox.showinfo("Done", f"Round over! Total credits: {self.credits}")

            return

        self.difficulty = difficulty

        if difficulty == "easy" and easy_q:
            idx = random.randint(0, len(easy_q) - 1)
            question = easy_q.pop(idx)
            self.correct_answer = easy_ans.pop(idx)
        elif difficulty == "medium" and medium_q:
            idx = random.randint(0, len(medium_q) - 1)
            question = medium_q.pop(idx)
            self.correct_answer = medium_ans.pop(idx)
        elif difficulty == "hard" and hard_q:
            idx = random.randint(0, len(hard_q) - 1)
            question = hard_q.pop(idx)
            self.correct_answer = hard_ans.pop(idx)
        else:
            messagebox.showwarning("Out of Questions", f"No more {difficulty} questions!")
            return

        self.round += 1
        self.question_label.config(text=f"{difficulty.capitalize()} Question ({self.round}/{total_rounds}):\n\n{question}")
        self.answer_entry.delete(0, tk.END)
        self.answer_entry.focus()

    def load_next_question(self):
        if self.current_question_index < len(self.question_history) - 1:
            # Move forward in history
            self.current_question_index += 1
            difficulty, question, answer = self.question_history[self.current_question_index]
        else:
            if self.round >= total_rounds:
                messagebox.showinfo("Done", f"Round over! Total credits: {self.credits}")
                return

            # Generate a new question
            available = []
            if easy_q: available.append("easy")
            if medium_q: available.append("medium")
            if hard_q: available.append("hard")

            if not available:
                messagebox.showwarning("Out of Questions", "No questions left in any category.")
                return

            difficulty = random.choice(available)

            if difficulty == "easy" and easy_q:
                idx = random.randint(0, len(easy_q) - 1)
                question = easy_q.pop(idx)
                answer = easy_ans.pop(idx)
            elif difficulty == "medium" and medium_q:
                idx = random.randint(0, len(medium_q) - 1)
                question = medium_q.pop(idx)
                answer = medium_ans.pop(idx)
            elif difficulty == "hard" and hard_q:
                idx = random.randint(0, len(hard_q) - 1)
                question = hard_q.pop(idx)
                answer = hard_ans.pop(idx)
            else:
                return

            self.round += 1
            self.question_history.append((difficulty, question, answer))
            self.current_question_index += 1

        self.difficulty = difficulty
        self.correct_answer = answer
        self.question_label.config(
            text=f"{difficulty.capitalize()} Question ({self.round}/{total_rounds}):\n\n{question}"
        )
        if self.current_question_index in self.answered_questions:
            self.answer_entry.config(state='disabled')
            self.submit_button.config(state='disabled')
            self.answer_overlay.place(relx=0.5, rely=0.46, anchor='center')
        else:
            self.submit_button.config(state='normal')
            self.answer_entry.config(state='normal')
            self.answer_overlay.place_forget()
            self.answer_entry.delete(0, tk.END)
        self.answer_entry.delete(0, tk.END)
        self.answer_entry.focus()
        self.balance_label.config(text=f"Balance: {self.credits} credits")


    def load_previous_question(self):
        if self.current_question_index > 0:
            self.current_question_index -= 1
            difficulty, question, answer = self.question_history[self.current_question_index]
            self.difficulty = difficulty
            self.correct_answer = answer
            self.question_label.config(
                text=f"{difficulty.capitalize()} Question ({self.current_question_index+1}/{total_rounds}):\n\n{question}"
            )
            if self.current_question_index in self.answered_questions:
                self.answer_entry.config(state='disabled')
                self.submit_button.config(state='disabled')
            else:
                self.submit_button.config(state='normal')
                self.answer_entry.config(state='normal')
                self.answer_overlay.place_forget()  
                self.answer_entry.delete(0, tk.END)
            self.answer_entry.delete(0, tk.END)
        else:
            messagebox.showinfo("Start", "This is your first question.")
        self.balance_label.config(text=f"Balance: {self.credits} credits")

    def load_random_question(self):
        available = []
        if easy_q: available.append("easy")
        if medium_q: available.append("medium")
        if hard_q: available.append("hard")

        if not available:
            messagebox.showwarning("Out of Questions", "No questions left in any category.")
            return

        difficulty = random.choice(available)
        self.load_question(difficulty)

    def check_answer(self):
        answer = self.answer_entry.get().strip()
        if not self.correct_answer:
            messagebox.showwarning("No Question", "Please click on Next to get question.")
            return

        if answer == self.correct_answer:
            if self.difficulty == "easy":
                self.credits += 50
            elif self.difficulty == "medium":
                self.credits += 100
            elif self.difficulty == "hard":
                self.credits += 250
            messagebox.showinfo("Correct!", "That's correct!")
            self.balance_label.config(text=f"Balance: {self.credits} credits")
        else:
            self.credits -= 100
            messagebox.showinfo("Incorrect!", f"Wrong answer. Correct was: {self.correct_answer}")
            self.balance_label.config(text=f"Balance: {self.credits} credits")
        self.answered_questions.add(self.current_question_index)
        self.answer_entry.config(state='disabled')
        self.answer_overlay.place(relx=0.5, rely=0.46, anchor='center')
        self.correct_answer = None
        self.difficulty = None
        self.question_label.config(text="Press Next for Next Question")
        self.answer_entry.delete(0, tk.END)
        

        if len(self.answered_questions) == total_rounds:
            messagebox.showinfo("Completed", f"All {total_rounds} rounds complete!\nFinal Balance: {self.credits}")
            self.balance_label.config(text=f"Your final balance is : {self.credits} credits")


            
        


# === Run the App ===
root = tk.Tk()
app = QuizApp(root)
root.mainloop()
