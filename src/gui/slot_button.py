
from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt, Signal

class SlotButton(QPushButton):
    # 自定义信号
    right_clicked = Signal()
    
    def __init__(self, row: int, col: int):
        super().__init__()
        self.row = row
        self.col = col
        self.setFixedSize(15, 15)
        self.default_style()
        self.setFlat(True)

    def mousePressEvent(self, event):
        """重写鼠标按下事件"""
        if event.button() == Qt.RightButton:
            self.right_clicked.emit()
        else:
            super().mousePressEvent(event)

    def default_style(self):
        """默认未点击状态"""
        self.setStyleSheet("""
            background-color: #C0C0C0;
            border-top: 2px solid white;
            border-left: 2px solid white;
            border-bottom: 2px solid #808080;
            border-right: 2px solid #808080;
        """)
        self.setText("")

    def show_mine(self, is_clicked_mine=False):
        """显示地雷"""
        bg_color = "red" if is_clicked_mine else "#C0C0C0"
        self.setStyleSheet(f"""
            background-color: {bg_color};
            border: 1px solid #999999;
            font-weight: bold;
            color: black;
        """)
        self.setText("💣")

    def show_number(self, mine_count: int):
        """显示数字"""
        mine_colors = {
            0: "#C0C0C0", 1: "#0000FF", 2: "#008000", 3: "#FF0000",
            4: "#000080", 5: "#800000", 6: "#008080", 7: "#000000", 8: "#808080"
        }
        color = mine_colors.get(mine_count, "#000000")
        
        self.setStyleSheet(f"""
            background-color: white;
            border: 1px solid #999999;
            font-weight: bold;
            font-size: 10px;
            color: {color};
        """)
        
        self.setText(str(mine_count) if mine_count > 0 else "")

    def show_flag(self):
        """显示旗帜"""
        self.setStyleSheet("""
            background-color: #C0C0C0;
            border-top: 2px solid white;
            border-left: 2px solid white;
            border-bottom: 2px solid #808080;
            border-right: 2px solid #808080;
            font-weight: bold;
            color: red;
        """)
        self.setText("🚩")