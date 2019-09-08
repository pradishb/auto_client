''' Main script of the program '''
import curses
import time

from efficiency.efficiency import Efficiency
from connection.connection import Connection, ClientConnectionException

def main(stdscr):
    ''' Main function of the program '''
    efficiency = Efficiency()
    connection = Connection()
    while True:
        start_time = time.time()
        client_conenction = "Connected"
        stdscr.clear()
        efficiency.change()
        try:
            lcu_status = connection.request("/lol-service-status/v1/lcu-status", "get")
        except ClientConnectionException:
            client_conenction = "Not connected"
            lcu_status = "Not connected"
        process_time = time.time() - start_time
        stdscr.addstr('Efficiency: {:.2f} %\n'.format(efficiency.get_efficiency()))
        stdscr.addstr('Process time: {:.5f} s\n'.format(process_time))
        stdscr.addstr('Client connection: {}\n'.format(client_conenction))
        stdscr.addstr('Lcu status: {}\n'.format(lcu_status))
        stdscr.refresh()
        time.sleep(1)

if __name__ == '__main__':
    curses.wrapper(main)
