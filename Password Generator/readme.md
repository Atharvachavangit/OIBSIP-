# 🔐 Password Generator (PyQt5)

A powerful and secure **Password Generator GUI** built using **Python** and **PyQt5**.  
This application allows users to create strong, customizable passwords with adjustable length, character types, exclusions, and automatic strength analysis.

---

## 🚀 Features

- 🧩 **Customizable Options**
  - Choose from lowercase, uppercase, digits, and symbols  
  - Exclude specific characters manually  
  - Option to remove ambiguous characters (`I`, `l`, `1`, `O`, `0`)  
  - Ensure at least one of each selected type is included  

- 🧠 **Password Strength Estimation**
  - Calculates entropy (in bits) and classifies strength from *Very Weak → Very Strong*  

- 🧾 **History Panel**
  - Displays the last 50 generated passwords  
  - Double-click to copy a password from history  

- 💾 **Save & Copy**
  - Copy generated password to clipboard  
  - Save passwords with timestamps to `passwords.txt`  

- 🎨 **Modern GUI**
  - Scrollable, clean interface with logical grouping of controls  
  - Responsive layout for better usability  

---

## 🧰 Requirements

- Python 3.7 or higher  
- PyQt5

To install dependencies, run:
```bash
pip install PyQt5
```

---

## ⚙️ How to Run

1. Clone or download this project.  
2. Navigate to the folder containing `password_generator.py`.  
3. Run the app:

   ```bash
   python password_generator.py
   ```

4. Adjust password settings → click **Generate** → copy or save your password.  

---

## 🧮 Password Entropy Formula

The entropy of a password is estimated using:

\[
Entropy = Length \times \log_2(Pool\ Size)
\]

| Bits of Entropy | Strength       |
|------------------|----------------|
| < 28             | Very Weak      |
| 28–35            | Weak           |
| 36–59            | Reasonable     |
| 60–79            | Strong         |
| ≥ 80             | Very Strong    |

---

## 🗂️ Output Files

- **`passwords.txt`** → Stores generated passwords with timestamps.  

---

## 🧑‍💻 Author

Developed by **Atharva A. Chavan**  
A simple yet powerful GUI-based password generator using Python’s secure `secrets` module and PyQt5 framework.

---
