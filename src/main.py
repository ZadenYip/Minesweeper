from PySide6.QtWidgets import QApplication
from gui import CustomRulesWindow
from gui import MineBoard
from gui.start_and_custom_rules_gui import game_config

import sys
game_window:MineBoard = None
rule_window:CustomRulesWindow = None

def start_game(rows, cols, mines):
    global game_window, rule_window
    game_window = MineBoard(rows, cols, mines)
    game_window.show()
    
def reset_game():
    start_game(game_config.rows, game_config.cols, game_config.mines)

def show_rules_window():
    global rule_window
    rule_window = CustomRulesWindow()
    rule_window.confirm_button_signal.connect(start_game)
    rule_window.show()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    show_rules_window()
    sys.exit(app.exec())
    
