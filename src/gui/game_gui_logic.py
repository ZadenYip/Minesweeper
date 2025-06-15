import random
from typing import Set, Tuple, List, NamedTuple
from collections import deque
from enum import Enum, auto


class DisplayType(Enum):
    """单元格显示类型枚举"""
    HIDDEN = auto()
    NUMBER = auto()
    MINE = auto()
    FLAG = auto()

class GameResult(Enum):
    """游戏结果类型枚举"""
    NO_ACTION = auto()
    REVEAL = auto()
    GAME_OVER = auto()
    VICTORY = auto()
    FLAG_TOGGLE = auto()
    
class ClickResult:
    """点击结果类"""
    
    def __init__(self, result_type: GameResult, affected_cells: Set[Tuple[int, int]] = set()):
        self.type = result_type
        self.affected_cells = affected_cells
        
class CellState(NamedTuple):
    """单元格显示状态"""
    display_type: DisplayType
    mine_count: int = 0
    is_clicked_mine: bool = False

class MinesweeperGame:
    """扫雷游戏核心逻辑类"""

    
    def __init__(self, rows: int, cols: int, mines: int):
        self.rows = rows
        self.cols = cols
        self.total_mines = mines
        self.game_started = False
        self.game_over = False
        self.game_won = False
        
        # 游戏状态数据
        self.mine_positions: Set[Tuple[int, int]] = set()
        self.revealed_cells: Set[Tuple[int, int]] = set()
        self.flagged_cells: Set[Tuple[int, int]] = set()
        self.clicked_mine_position: Tuple[int, int] = None
    
    def is_valid_position(self, row: int, col: int) -> bool:
        return 0 <= row < self.rows and 0 <= col < self.cols
    
    def get_neighbors(self, row: int, col: int) -> List[Tuple[int, int]]:
        neighbors = []
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if (r, c) != (row, col) and self.is_valid_position(r, c):
                    neighbors.append((r, c))
        return neighbors
    
    def initialize_mines(self, first_click_row: int, first_click_col: int):
        if self.game_started:
            return
            
        safe_area = {(first_click_row, first_click_col)}
        safe_area.update(self.get_neighbors(first_click_row, first_click_col))
        
        all_positions = [(r, c) for r in range(self.rows) for c in range(self.cols)]
        candidate_positions = [pos for pos in all_positions if pos not in safe_area]
        
        self.mine_positions = set(random.sample(candidate_positions, self.total_mines))
        self.game_started = True
    
    def has_mine(self, row: int, col: int) -> bool:
        return (row, col) in self.mine_positions
    
    def get_adjacent_mine_count(self, row: int, col: int) -> int:
        count = 0
        for neighbor_row, neighbor_col in self.get_neighbors(row, col):
            if self.has_mine(neighbor_row, neighbor_col):
                count += 1
        return count
    
    def is_revealed(self, row: int, col: int) -> bool:
        return (row, col) in self.revealed_cells
    
    def is_flagged(self, row: int, col: int) -> bool:
        return (row, col) in self.flagged_cells
    
    def game_end_logic(self) -> dict[Tuple[int, int], CellState]:
        """游戏结束 返回所有地雷以供标记"""
        dict = {}
        for coordinate in self.mine_positions:
            if coordinate == self.clicked_mine_position:
                dict[coordinate] = CellState(DisplayType.MINE, is_clicked_mine=True)
            else:
                dict[coordinate] = CellState(DisplayType.MINE, is_clicked_mine=False)
        return dict
    
    def get_cell_display_state(self, row: int, col: int) -> CellState:
        """获取单元格的状态"""
        
        # 游戏结束时显示所有地雷
        if self.game_over:
            if self.has_mine(row, col):
                is_clicked = (row, col) == self.clicked_mine_position
                return CellState(DisplayType.MINE, is_clicked_mine=is_clicked)
            elif self.is_revealed(row, col):
                mine_count = self.get_adjacent_mine_count(row, col)
                return CellState(DisplayType.NUMBER, mine_count)
        
        # 正常游戏状态
        if self.is_flagged(row, col):
            return CellState(DisplayType.FLAG)
        elif self.is_revealed(row, col):
            mine_count = self.get_adjacent_mine_count(row, col)
            return CellState(DisplayType.NUMBER, mine_count)
        else:
            return CellState(DisplayType.HIDDEN)
    
    def click_cell(self, row: int, col: int) -> ClickResult:
        if self.game_over or self.is_revealed(row, col) or self.is_flagged(row, col):
            return ClickResult(GameResult.NO_ACTION, set())
        
        if not self.game_started:
            self.initialize_mines(row, col)
        
        if self.has_mine(row, col):
            self.game_over = True
            self.clicked_mine_position = (row, col)
            # 返回所有需要更新显示的格子
            all_positions = {(r, c) for r in range(self.rows) for c in range(self.cols)}
            return ClickResult(GameResult.GAME_OVER, all_positions)
        
        newly_revealed = self._reveal_area(row, col)
        
        if self._check_victory():
            self.game_won = True
            return ClickResult(GameResult.VICTORY, newly_revealed)
        
        return ClickResult(GameResult.REVEAL, newly_revealed)
    
    def toggle_flag(self, row: int, col: int) -> ClickResult:
        """切换旗帜状态"""
        if self.game_over or self.is_revealed(row, col):
            return ClickResult(GameResult.NO_ACTION, set())
        
        if self.is_flagged(row, col):
            self.flagged_cells.remove((row, col))
        else:
            self.flagged_cells.add((row, col))
        
        return ClickResult(GameResult.FLAG_TOGGLE, {(row, col)})
    
    def _reveal_area(self, start_row: int, start_col: int) -> Set[Tuple[int, int]]:
        newly_revealed = set()
        queue = deque([(start_row, start_col)])
        
        while queue:
            row, col = queue.popleft()
            
            if (row, col) in self.revealed_cells or self.has_mine(row, col):
                continue
                
            self.revealed_cells.add((row, col))
            newly_revealed.add((row, col))
            
            if self.get_adjacent_mine_count(row, col) == 0:
                for neighbor_row, neighbor_col in self.get_neighbors(row, col):
                    if (neighbor_row, neighbor_col) not in self.revealed_cells:
                        queue.append((neighbor_row, neighbor_col))
        
        return newly_revealed
    
    def _check_victory(self) -> bool:
        total_cells = self.rows * self.cols
        revealed_count = len(self.revealed_cells)
        return revealed_count == total_cells - self.total_mines
