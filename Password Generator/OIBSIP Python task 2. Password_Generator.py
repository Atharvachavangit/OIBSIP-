import sys
import math
import secrets
import string
from datetime import datetime
from PyQt5 import QtWidgets, QtCore, QtGui

AMBIGUOUS = set("Il1O0")




def build_pools(lower, upper, digits, symbols, exclude_chars: set, remove_ambiguous: bool):
    pools = {}
    if lower:
        pools['lower'] = ''.join(ch for ch in string.ascii_lowercase if ch not in exclude_chars)
    if upper:
        pools['upper'] = ''.join(ch for ch in string.ascii_uppercase if ch not in exclude_chars)
    if digits:
        pools['digits'] = ''.join(ch for ch in string.digits if ch not in exclude_chars)
    if symbols:
        pools['symbols'] = ''.join(ch for ch in string.punctuation if ch not in exclude_chars)

    if remove_ambiguous:
        for key in list(pools.keys()):
            pools[key] = ''.join(ch for ch in pools[key] if ch not in AMBIGUOUS)

    return {k: v for k, v in pools.items() if v}


def estimate_entropy(length: int, pool_size: int) -> float:
    if pool_size <= 0 or length <= 0:
        return 0.0
    return length * math.log2(pool_size)


def strength_label(bits: float) -> str:
    if bits < 28:
        return "Very Weak"
    if bits < 36:
        return "Weak"
    if bits < 60:
        return "Reasonable"
    if bits < 80:
        return "Strong"
    return "Very Strong"


def generate_password(length: int, pools: dict, ensure_each: bool) -> str:
    if not pools:
        raise ValueError("No character pools available.")
    combined = ''.join(pools.values())
    if not combined:
        raise ValueError("Character set is empty after exclusions.")

    pwd_chars = []
    if ensure_each:
        for pool in pools.values():
            pwd_chars.append(secrets.choice(pool))

    remaining = length - len(pwd_chars)
    if remaining < 0:
        raise ValueError("Length too small to include one of each selected type.")

    for _ in range(remaining):
        pwd_chars.append(secrets.choice(combined))

    secrets.SystemRandom().shuffle(pwd_chars)
    return ''.join(pwd_chars)




class PasswordGeneratorWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Password Generator")
        self.resize(900, 650)
        self.history = []
        self.init_ui()

    def init_ui(self):
        main_widget = QtWidgets.QWidget()
        main_layout = QtWidgets.QVBoxLayout()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)


        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setMinimumHeight(320)  # makes it taller by default

        scroll_content = QtWidgets.QWidget()
        scroll_layout = QtWidgets.QVBoxLayout(scroll_content)

        opts_group = QtWidgets.QGroupBox("Password Options")
        opts_layout = QtWidgets.QVBoxLayout()
        opts_group.setLayout(opts_layout)



        length_layout = QtWidgets.QHBoxLayout()
        length_label = QtWidgets.QLabel("Password Length:")
        self.length_spin = QtWidgets.QSpinBox()
        self.length_spin.setRange(4, 128)
        self.length_spin.setValue(16)
        self.length_spin.setFixedWidth(90)
        length_layout.addWidget(length_label)
        length_layout.addWidget(self.length_spin)
        length_layout.addStretch()
        opts_layout.addLayout(length_layout)
        opts_layout.addSpacing(10)


        opts_layout.addWidget(QtWidgets.QLabel("<b>Character Types:</b>"))

        self.cb_lower = QtWidgets.QCheckBox("Lowercase (a–z)")
        self.cb_lower.setChecked(True)
        self.cb_upper = QtWidgets.QCheckBox("Uppercase (A–Z)")
        self.cb_upper.setChecked(True)
        self.cb_digits = QtWidgets.QCheckBox("Digits (0–9)")
        self.cb_digits.setChecked(True)
        self.cb_symbols = QtWidgets.QCheckBox("Symbols (!@#...)")
        self.cb_symbols.setChecked(True)

        char_type_layout = QtWidgets.QHBoxLayout()
        char_type_layout.addWidget(self.cb_lower)
        char_type_layout.addWidget(self.cb_upper)
        char_type_layout.addWidget(self.cb_digits)
        char_type_layout.addWidget(self.cb_symbols)
        opts_layout.addLayout(char_type_layout)
        opts_layout.addSpacing(15)


        opts_layout.addWidget(QtWidgets.QLabel("<b>Filters:</b>"))
        self.cb_ambiguous = QtWidgets.QCheckBox("Remove ambiguous characters (Il1O0)")
        self.cb_ambiguous.setChecked(True)
        opts_layout.addWidget(self.cb_ambiguous)

        exclude_layout = QtWidgets.QHBoxLayout()
        exclude_layout.addWidget(QtWidgets.QLabel("Exclude characters:"))
        self.exclude_edit = QtWidgets.QLineEdit()
        self.exclude_edit.setPlaceholderText("Type characters to exclude (e.g. (){}[]/)")
        exclude_layout.addWidget(self.exclude_edit)
        opts_layout.addLayout(exclude_layout)
        opts_layout.addSpacing(15)


        opts_layout.addWidget(QtWidgets.QLabel("<b>Rules:</b>"))
        self.cb_ensure_each = QtWidgets.QCheckBox("Ensure at least one of each selected type")
        self.cb_ensure_each.setChecked(True)
        opts_layout.addWidget(self.cb_ensure_each)
        opts_layout.addStretch(1)


        scroll_layout.addWidget(opts_group)
        scroll_content.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area, stretch=2)


        res_group = QtWidgets.QGroupBox("Generated Password")
        res_layout = QtWidgets.QGridLayout()
        res_group.setLayout(res_layout)

        self.result_edit = QtWidgets.QLineEdit()
        self.result_edit.setReadOnly(True)
        self.result_edit.setFont(QtGui.QFont("Consolas", 12))
        res_layout.addWidget(self.result_edit, 0, 0, 1, 3)

        self.generate_btn = QtWidgets.QPushButton("Generate")
        self.generate_btn.clicked.connect(self.on_generate)
        res_layout.addWidget(self.generate_btn, 1, 0)

        self.copy_btn = QtWidgets.QPushButton("Copy")
        self.copy_btn.clicked.connect(self.on_copy)
        res_layout.addWidget(self.copy_btn, 1, 1)

        self.save_btn = QtWidgets.QPushButton("Save")
        self.save_btn.clicked.connect(self.on_save)
        res_layout.addWidget(self.save_btn, 1, 2)

        self.entropy_label = QtWidgets.QLabel("Entropy: - bits")
        self.strength_label = QtWidgets.QLabel("Strength: -")
        res_layout.addWidget(self.entropy_label, 2, 0, 1, 2)
        res_layout.addWidget(self.strength_label, 2, 2)

        main_layout.addWidget(res_group, stretch=1)


        hist_group = QtWidgets.QGroupBox("History (double-click to copy)")
        hist_layout = QtWidgets.QHBoxLayout()
        hist_group.setLayout(hist_layout)

        self.history_list = QtWidgets.QListWidget()
        self.history_list.itemDoubleClicked.connect(self.on_history_double)
        hist_layout.addWidget(self.history_list)
        main_layout.addWidget(hist_group, stretch=1)


        footer = QtWidgets.QLabel(
            "Tip: Use passwords ≥ 12 chars and multiple character types for better security."
        )
        footer.setStyleSheet("color: gray;")
        main_layout.addWidget(footer)



    def on_generate(self):
        length = int(self.length_spin.value())
        exclude_chars = set(self.exclude_edit.text() or "")
        pools = build_pools(
            lower=self.cb_lower.isChecked(),
            upper=self.cb_upper.isChecked(),
            digits=self.cb_digits.isChecked(),
            symbols=self.cb_symbols.isChecked(),
            exclude_chars=exclude_chars,
            remove_ambiguous=self.cb_ambiguous.isChecked(),
        )

        if not pools:
            QtWidgets.QMessageBox.warning(
                self, "Error", "Select at least one character type and ensure exclusions are valid."
            )
            return

        try:
            pwd = generate_password(length, pools, ensure_each=self.cb_ensure_each.isChecked())
        except ValueError as e:
            QtWidgets.QMessageBox.warning(self, "Error", str(e))
            return

        self.result_edit.setText(pwd)
        pool_size = len(''.join(pools.values()))
        bits = estimate_entropy(len(pwd), pool_size)
        self.entropy_label.setText(f"Entropy: {bits:.1f} bits (pool {pool_size})")
        self.strength_label.setText(f"Strength: {strength_label(bits)}")
        self.add_history(pwd)

    def on_copy(self):
        pwd = self.result_edit.text()
        if not pwd:
            QtWidgets.QMessageBox.information(self, "No Password", "Generate a password first.")
            return
        QtWidgets.QApplication.clipboard().setText(pwd)
        QtWidgets.QMessageBox.information(self, "Copied", "Password copied to clipboard!")

    def on_save(self):
        pwd = self.result_edit.text()
        if not pwd:
            QtWidgets.QMessageBox.information(self, "No Password", "Generate a password first.")
            return
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            with open("passwords.txt", "a", encoding="utf-8") as f:
                f.write(f"{now}\t{pwd}\n")
            QtWidgets.QMessageBox.information(self, "Saved", "Password saved to passwords.txt")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Save Error", f"Error saving file: {e}")

    def on_history_double(self, item: QtWidgets.QListWidgetItem):
        idx = self.history_list.row(item)
        if idx < 0 or idx >= len(self.history):
            return
        pwd = self.history[idx]
        QtWidgets.QApplication.clipboard().setText(pwd)
        QtWidgets.QMessageBox.information(self, "Copied", "Password copied from history!")

    def add_history(self, pwd: str):
        if pwd in self.history:
            self.history.remove(pwd)
        self.history.insert(0, pwd)
        if len(self.history) > 50:
            self.history.pop()
        self.history_list.clear()
        for p in self.history:
            display = p if len(p) <= 50 else p[:47] + "..."
            self.history_list.addItem(display)




def main():
    app = QtWidgets.QApplication(sys.argv)
    window = PasswordGeneratorWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
