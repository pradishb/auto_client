''' Main script of the program '''
import curses
import time

from efficiency.efficiency import Efficiency
from connection.connection import Connection
from status.status import get_status, display_status


def main(stdscr):
    ''' Main function of the program '''
    efficiency = Efficiency()
    connection = Connection()
    while True:
        start_time = time.time()
        stdscr.clear()
        efficiency.change()
        status = get_status(connection)
        process_time = time.time() - start_time
        stdscr.addstr('Efficiency: {:.2f}%\n'.format(efficiency.get_efficiency()))
        stdscr.addstr('Process time: {:.5f}s\n'.format(process_time))
        display_status(stdscr, status)
        stdscr.refresh()
        time.sleep(1)

if __name__ == '__main__':
    curses.wrapper(main)
