import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime


conn = sqlite3.connect('bmi_data.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS bmi_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        height REAL,
        weight REAL,
        bmi REAL,
        category TEXT,
        date TEXT
    )
''')
conn.commit()


def calculate_bmi():
    name = name_entry.get().strip()
    try:
        height = float(height_entry.get())
        weight = float(weight_entry.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numbers for height and weight.")
        return

    if not name:
        messagebox.showerror("Input Error", "Please enter a name.")
        return

    height_m = height / 100
    bmi = weight / (height_m ** 2)

    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 25:
        category = "Normal weight"
    elif bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"

    result_label.config(text=f"BMI: {bmi:.2f} ({category})")

    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO bmi_records (name, height, weight, bmi, category, date) VALUES (?, ?, ?, ?, ?, ?)",
                   (name, height, weight, bmi, category, date))
    conn.commit()


    show_records()

def show_records():
    for row in record_tree.get_children():
        record_tree.delete(row)

    cursor.execute("SELECT name, height, weight, bmi, category, date FROM bmi_records ORDER BY id DESC")
    for row in cursor.fetchall():
        record_tree.insert("", tk.END, values=row)


root = tk.Tk()
root.title("BMI Calculator & Tracker")
root.geometry("700x600")
root.configure(bg="#f3f4f6")

style = ttk.Style()
style.configure("Treeview", font=('Arial', 10))
style.configure("Treeview.Heading", font=('Arial', 11, 'bold'))

frame = tk.Frame(root, bg="#e0e7ff", padx=20, pady=20)
frame.pack(pady=10)

tk.Label(frame, text="Name:", bg="#e0e7ff", font=('Arial', 12)).grid(row=0, column=0, sticky="w", pady=5)
name_entry = tk.Entry(frame, font=('Arial', 12))
name_entry.grid(row=0, column=1, pady=5)

tk.Label(frame, text="Height (cm):", bg="#e0e7ff", font=('Arial', 12)).grid(row=1, column=0, sticky="w", pady=5)
height_entry = tk.Entry(frame, font=('Arial', 12))
height_entry.grid(row=1, column=1, pady=5)

tk.Label(frame, text="Weight (kg):", bg="#e0e7ff", font=('Arial', 12)).grid(row=2, column=0, sticky="w", pady=5)
weight_entry = tk.Entry(frame, font=('Arial', 12))
weight_entry.grid(row=2, column=1, pady=5)

tk.Button(frame, text="Calculate BMI", command=calculate_bmi, bg="#4f46e5", fg="white", font=('Arial', 12, 'bold')).grid(row=3, column=0, columnspan=2, pady=10)

result_label = tk.Label(frame, text="", bg="#e0e7ff", font=('Arial', 13, 'bold'))
result_label.grid(row=4, column=0, columnspan=2, pady=10)

record_frame = tk.LabelFrame(root, text="BMI Records", bg="#f3f4f6", font=('Arial', 12, 'bold'))
record_frame.pack(padx=10, pady=10, fill="both", expand=True)

columns = ("Name", "Height (cm)", "Weight (kg)", "BMI", "Category", "Date")
record_tree = ttk.Treeview(record_frame, columns=columns, show="headings", height=8)
for col in columns:
    record_tree.heading(col, text=col)
    record_tree.column(col, width=100)
record_tree.pack(fill="both", expand=True)

tk.Button(root, text="Refresh Data", command=show_records, bg="#10b981", fg="white", font=('Arial', 11, 'bold')).pack(pady=5)

show_records()
root.mainloop()
