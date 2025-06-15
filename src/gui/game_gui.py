
from PySide6.QtWidgets import QWidget, QGridLayout, QMessageBox
from typing import Callable
from .slot_button import SlotButton
from .game_gui_logic import MinesweeperGame, ClickResult, CellState, DisplayType, GameResult

class MineBoard(QWidget):
    """扫雷游戏界面类，只负责UI显示和事件处理"""
    
    def __init__(self, rows: int, cols: int, mines: int):
        super().__init__()
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.game = MinesweeperGame(rows, cols, mines)
        self._init_ui()
    
    def _init_ui(self):
        self.layout: QGridLayout = QGridLayout()
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
        
        self.buttons = {}
        for r in range(self.rows):
            for c in range(self.cols):
                btn = SlotButton(r, c)
                btn.clicked.connect(self._on_left_click)
                btn.right_clicked.connect(self._on_right_click)
                self.layout.addWidget(btn, r, c)
                self.buttons[(r, c)] = btn
        
        self.adjustSize()
        self.setFixedSize(self.size())
        self.setWindowTitle("扫雷游戏")
        
    def _show_end_dialog(self, title: str, content: str):
        dialog = QMessageBox(self)
        dialog.setWindowTitle(title)
        dialog.setText(content)
        restart_button = dialog.addButton("再来一局", QMessageBox.ButtonRole.AcceptRole)
        settings_button = dialog.addButton("重新设置", QMessageBox.ButtonRole.RejectRole)
        dialog.exec()
        
        clicked_button = dialog.clickedButton()
        self.close()
        if clicked_button == restart_button:
            from main import reset_game
            reset_game()
            return
        if clicked_button == settings_button:
            from main import show_rules_window
            show_rules_window()
            return
        
        
        
    def _on_left_click(self):
        """处理左键点击"""
        btn = self.sender()
        
        result = self.game.click_cell(btn.row, btn.col)
        self._update_display(result)
    
    def _on_right_click(self):
        """处理右键点击（插旗）"""
        btn = self.sender()
        
        result = self.game.toggle_flag(btn.row, btn.col)
        self._update_display(result)
    
    def _update_display(self, result: ClickResult):
        self._update_affected_cells(result.affected_cells)
        """根据游戏结果更新显示"""
        if result.type == GameResult.NO_ACTION:
            return
        # 针对不同结果类型采用不同的更新策略
        if result.type == GameResult.GAME_OVER:
            self._handle_game_over()
            return
        if result.type == GameResult.VICTORY:
            self._handle_victory()
            return

    
    def _handle_game_over(self):
        """处理游戏结束 - 只更新地雷格子"""
        self._handle_game_end()
        self._show_end_dialog("游戏结束", "游戏结束，你踩到了地雷！")
    
    def _handle_victory(self):
        """处理胜利 - 更新所有地雷为插旗"""
        self._handle_game_end()
        self._show_end_dialog("游戏胜利", "恭喜你，扫雷游戏胜利！")

    def _handle_game_end(self):
        for coordinate, state in self.game.game_end_logic().items():
           btn = self.buttons.get(coordinate)
           self._apply_cell_display(btn, state)
        
    
    def _update_affected_cells(self, affected_cells):
        """更新受影响的格子"""
        for row, col in affected_cells:
            btn = self.buttons.get((row, col))
            cell_state = self.game.get_cell_display_state(row, col)
            self._apply_cell_display(btn, cell_state)
    
    def _apply_cell_display(self, btn: SlotButton, state: CellState):
        """应用显示状态到按钮"""
        if state.display_type == DisplayType.HIDDEN:
            btn.default_style()
        elif state.display_type == DisplayType.NUMBER:
            btn.show_number(state.mine_count)
        elif state.display_type == DisplayType.MINE:
            btn.show_mine(state.is_clicked_mine)
        elif state.display_type == DisplayType.FLAG:
            btn.show_flag()