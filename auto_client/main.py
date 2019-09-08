''' Main script of the program '''
import curses
import time

from efficiency.efficiency import Efficiency
from connection.connection import Connection
from status import get_status, display_status


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
        stdscr.addstr('{:<30}{:.2f}%\n'.format('Efficiency', efficiency.get_efficiency()))
        stdscr.addstr('{:<30}{:.5f}s\n'.format('Process time', process_time))
        display_status(stdscr, status)
        stdscr.refresh()
        time.sleep(1)

if __name__ == '__main__':
    curses.wrapper(main)
