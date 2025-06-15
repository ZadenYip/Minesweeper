from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QSpinBox, QPushButton
)
from dataclasses import dataclass
from PySide6.QtCore import Signal
MAX_ROWS = int(16)
MAX_COLS = int(30)

@dataclass
class GameConfig:
    rows: int = 9
    cols: int = 9
    mines: int = 10
game_config = GameConfig()

class CustomRulesWindow(QWidget):
    confirm_button_signal = Signal(int, int, int)
    def __init__(self):
        super().__init__()
        self.rows = -1
        self.cols = -1
        self.mines = -1
        self.setWindowTitle("自定义扫雷规则")
        self.setFixedSize(300, 200)

        layout = QVBoxLayout()

        # 行数设置
        self.rows_label = QLabel(f"行数 (最多{MAX_ROWS}):")
        self.rows_spinbox = QSpinBox()
        self.rows_spinbox.setRange(1, MAX_ROWS)
        self.rows_spinbox.setValue(game_config.rows)
        layout.addWidget(self.rows_label)
        layout.addWidget(self.rows_spinbox)

        # 列数设置
        self.cols_label = QLabel(f"列数 (最多{MAX_COLS}):")
        self.cols_spinbox = QSpinBox()
        self.cols_spinbox.setRange(1, MAX_COLS)
        self.cols_spinbox.setValue(game_config.cols)
        layout.addWidget(self.cols_label)
        layout.addWidget(self.cols_spinbox)

        # 雷数设置
        self.mines_label = QLabel("雷数 (最多 行×列 - 9):")
        self.mines_spinbox = QSpinBox()
        self.mines_spinbox.setMinimum(1)
        self.mines_spinbox.setValue(game_config.mines)
        layout.addWidget(self.mines_label)
        layout.addWidget(self.mines_spinbox)

        # 更新雷数最大值
        self.rows_spinbox.valueChanged.connect(self.update_max_mines)
        self.cols_spinbox.valueChanged.connect(self.update_max_mines)

        # 确认按钮
        self.confirm_button = QPushButton("开始游戏")
        self.confirm_button.clicked.connect(self.confirm_settings)
        layout.addWidget(self.confirm_button)

        self.setLayout(layout)
        self.update_max_mines()

    def update_max_mines(self):
        rows = self.rows_spinbox.value()
        cols = self.cols_spinbox.value()
        
        max_mines = rows * cols - 9
        self.mines_spinbox.setMaximum(max_mines)

    def confirm_settings(self):
        self.rows = self.rows_spinbox.value()
        self.cols = self.cols_spinbox.value()
        self.mines = self.mines_spinbox.value()
        game_config.rows = self.rows
        game_config.cols = self.cols
        game_config.mines = self.mines
        self.confirm_button_signal.emit(self.rows, self.cols, self.mines)
        self.close()
