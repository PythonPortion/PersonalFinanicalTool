import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QDateEdit, QVBoxLayout
from PyQt5.QtCore import QDate


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.text_input = None
        self.date_selector = None
        self.button = None
        self.label = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("LoanTool")
        self.resize(800, 500)

        # 创建组件
        self.label = QLabel("请输入内容：")
        self.text_input = QLineEdit()
        self.button = QPushButton("提交")
        self.date_selector = QDateEdit()
        self.date_selector.setCalendarPopup(True)  # 显示日历弹出窗口
        self.date_selector.setDate(QDate.currentDate())  # 设置初始日期为当前日期

        # 连接按钮点击事件
        self.button.clicked.connect(self.on_button_click)

        # 布局
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.text_input)
        layout.addWidget(self.date_selector)
        layout.addWidget(self.button)

        # 设置窗口布局
        self.setLayout(layout)

    def on_button_click(self):
        input_text = self.text_input.text()
        selected_date = self.date_selector.date().toString("yyyy-MM-dd")
        print(f"输入的文本: {input_text}, 选择的日期: {selected_date}")


if __name__ == "__main__":
    # 创建应用程序实例
    app = QApplication(sys.argv)

    # 创建主窗口
    window = MainWindow()
    window.show()

    # 运行应用程序事件循环
    sys.exit(app.exec_())
