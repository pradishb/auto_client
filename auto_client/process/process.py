'''
Module that handles tasks related to processes
'''
import psutil

def is_running(process_name):
    '''
    Check if there is any running process that contains the given name process_name.
    '''
    #Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if process_name.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

