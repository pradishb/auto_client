''' Module to handle efficiency of the program '''
from process.process import is_running
from settings import GAME_PROCESS_NAME

class Efficiency:
    ''' Efficiency class '''
    def __init__(self):
        self.game_time = 0
        self.total_time = 0

    def change(self):
        ''' Increases the value of game time if game process is available '''
        self.total_time += 1
        if is_running(GAME_PROCESS_NAME):
            self.game_time += 1

    def get_efficiency(self):
        ''' Calcuates the effiency in percentage '''
        return self.game_time * 100 / self.total_time
