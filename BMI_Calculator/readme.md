
# 🧮 BMI Calculator & Tracker (Tkinter + SQLite)

A simple **Python desktop app** built using **Tkinter** and **SQLite** that allows users to calculate their Body Mass Index (BMI) and store their results with automatic tracking and categorization.

---

## 🚀 Features

- 🧠 **BMI Calculation** based on height and weight  
- 🧾 **Automatic Categorization** (Underweight, Normal, Overweight, Obese)  
- 💾 **Data Storage** in a local SQLite database (`bmi_data.db`)  
- 📅 **Timestamp Tracking** for each entry  
- 📋 **Record Viewer** using `ttk.Treeview`  
- 🔄 **Refresh Button** to view updated data instantly  
- 🎨 **Modern UI** with a light background and styled widgets  

---

## 🧰 Requirements

- Python 3.x  
- Tkinter (comes preinstalled with Python)  
- SQLite3 (comes preinstalled with Python)

---

## ⚙️ How to Run

1. Clone or download the project files.  
2. Make sure Python 3 is installed.  
3. Open a terminal in the project folder and run:

   ```bash
   python bmi_calculator.py
   ```

4. Enter your **name**, **height (cm)**, and **weight (kg)**.  
5. Click **"Calculate BMI"** to see your result and save it automatically.  
6. View your history in the **BMI Records** table below.

---

## 🧮 BMI Formula

\[
BMI = \frac{weight(kg)}{[height(m)]^2}
\]

| BMI Range | Category        |
|------------|----------------|
| < 18.5     | Underweight    |
| 18.5–24.9  | Normal weight  |
| 25–29.9    | Overweight     |
| ≥ 30       | Obese          |

---

## 📂 Database Details

- Database file: `bmi_data.db`  
- Table: `bmi_records`  
- Columns:  
  `id`, `name`, `height`, `weight`, `bmi`, `category`, `date`

---

## 🧑‍💻 Author
Developed by **Atharva A. Chavan**  
A beginner-friendly Tkinter + SQLite project for learning GUI programming and database handling in Python.
