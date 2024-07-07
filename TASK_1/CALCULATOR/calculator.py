import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QPushButton, QVBoxLayout, QWidget, QLineEdit, QSizePolicy, QGridLayout, QLabel, QHBoxLayout
from PySide6.QtCore import Qt

class CalculatorApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PySide6 Calculator")
        self.setGeometry(100, 100, 400, 500)

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.stackedWidget = QStackedWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.stackedWidget)

        top_layout = QHBoxLayout()
        layout.addLayout(top_layout)

        self.theme_toggle_button = QPushButton("Toggle Theme")
        self.theme_toggle_button.clicked.connect(self.toggle_theme)
        top_layout.addWidget(self.theme_toggle_button)

        self.tutorial_button = QPushButton("Tutorials")
        self.tutorial_button.clicked.connect(self.switch_to_tutorial_page)
        top_layout.addWidget(self.tutorial_button)

        self.centralWidget.setLayout(layout)

        self.standard_calculator_page = QWidget()
        self.create_standard_calculator_ui(self.standard_calculator_page)
        self.stackedWidget.addWidget(self.standard_calculator_page)

        self.tutorial_page = QWidget()
        self.create_tutorial_ui(self.tutorial_page)
        self.stackedWidget.addWidget(self.tutorial_page)

        self.switch_to_standard_calculator_page()

        self.set_light_theme()

        self.set_button_tooltips()

        self.set_keyboard_shortcuts()

    def create_standard_calculator_ui(self, page):
        page.layout = QVBoxLayout()
        self.result_display = QLineEdit()

        self.result_display.setFixedHeight(50)
        self.result_display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.result_display.setReadOnly(True)
        page.layout.addWidget(self.result_display)

        self.buttons = {
            '0': (5, 0), '1': (4, 0), '2': (4, 1), '3': (4, 2),
            '4': (3, 0), '5': (3, 1), '6': (3, 2), '7': (2, 0),
            '8': (2, 1), '9': (2, 2), '+': (5, 3), '-': (4, 3),
            '*': (3, 3), '/': (2, 3), '=': (5, 2), '.': (5, 1),
            'C': (1, 0), '⌫': (1, 1), '+/-': (1, 2), '%': (1, 3)
        }

        self.grid_layout = QGridLayout()
        for btn_text, pos in self.buttons.items():
            button = QPushButton(btn_text)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding) 
            button.clicked.connect(self.on_button_click)
            button.setCursor(Qt.CursorShape.PointingHandCursor) 
            self.grid_layout.addWidget(button, *pos)

        page.layout.addLayout(self.grid_layout)
        page.setLayout(page.layout)

    def create_tutorial_ui(self, page):
        page.layout = QVBoxLayout()

        tutorial_label = QLabel("Welcome to the Calculator Tutorial!\n\n"
                                "Use the buttons to perform calculations. Here are some tips:\n\n"
                                "- Use numeric buttons (0-9) to input numbers.\n"
                                "- Use operators (+, -, *, /) for basic arithmetic.\n"
                                "- 'C' clears the display.\n"
                                "- '⌫' removes the last digit.\n"
                                "- '=' calculates the result.\n"
                                "- Use keyboard shortcuts for faster input!\n\n"
                                "Enjoy calculating!")
        tutorial_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        page.layout.addWidget(tutorial_label)

        back_button = QPushButton("Back to Calculator")
        back_button.clicked.connect(self.switch_to_standard_calculator_page)
        page.layout.addWidget(back_button)

        page.setLayout(page.layout)

    def on_button_click(self):
        button = self.sender()
        text = button.text()

        if text == 'C':
            self.result_display.clear()
        elif text == '⌫':
            self.result_display.backspace()
        elif text == '=':
            try:
                result = eval(self.result_display.text())
                self.result_display.setText(str(result))
            except Exception as e:
                self.result_display.setText("Error")
        else:
            self.result_display.setText(self.result_display.text() + text)

    def switch_to_standard_calculator_page(self):
        self.stackedWidget.setCurrentWidget(self.standard_calculator_page)

    def switch_to_tutorial_page(self):
        self.stackedWidget.setCurrentWidget(self.tutorial_page)

    def set_light_theme(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QPushButton {
                font-size: 16px;
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: #ffffff;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
            }
            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 10px;
            }
        """)

    def set_dark_theme(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #333;
                color: #fff;
            }
            QPushButton {
                font-size: 16px;
                border: 1px solid #555;
                border-radius: 5px;
                background-color: #444;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #555;
            }
            QPushButton:pressed {
                background-color: #666;
            }
            QLineEdit {
                border: 1px solid #555;
                border-radius: 5px;
                padding: 10px;
                color: #fff;
                background-color: #666;
            }
        """)

    def toggle_theme(self):
        current_stylesheet = self.styleSheet()
        if "background-color: #f0f0f0;" in current_stylesheet:
            self.set_dark_theme()
        else:
            self.set_light_theme()

    def set_button_tooltips(self):
        for btn_text, _ in self.buttons.items():
            button = self.grid_layout.itemAtPosition(*self.buttons[btn_text]).widget()
            button.setToolTip(f"Press '{btn_text}'")

    def set_keyboard_shortcuts(self):
        for btn_text, _ in self.buttons.items():
            button = self.grid_layout.itemAtPosition(*self.buttons[btn_text]).widget()
            button.setShortcut(btn_text)

    def keyPressEvent(self, event):
        key = event.text()
        if key in self.buttons:
            self.on_button_click(self.buttons[key])

def main():
    app = QApplication(sys.argv)
    calculator = CalculatorApp()
    calculator.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
