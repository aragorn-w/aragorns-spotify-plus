import sys
sys.dont_write_bytecode = True
from time import time, sleep

from utils.library_getter import *
from utils.library_tools import *


LIBRARY_UPDATE_PAUSE_TIME = 6


# Main loop for updating the saved playlist library JSONs
def update_library_tracks_loop(printout: bool=False):
    global LIBRARY_UPDATE_PAUSE_TIME, GET_LIBRARY_TIMEOUT

    running_times = []

    while True:
        if printout: print("\nNew library-update iteration...")
        total_start = time()

        if printout: print("Started getting new libraries...")
        start = time()
        get_libraries_thread = Thread(target=get_libraries)
        get_libraries_thread.start()
        get_libraries_thread.join(timeout=GET_LIBRARY_TIMEOUT)
        if get_libraries_thread.is_alive():
            print("!!! GET LIBRARIES TIMED OUT !!!")
        else:
            if printout: print(f"Got new libraries ({round(time() - start, 3)}s)")

        if printout: print(f"Running manual API sleep for ({LIBRARY_UPDATE_PAUSE_TIME}s)...")
        sleep(LIBRARY_UPDATE_PAUSE_TIME)

        total_iteration_time = time() - total_start
        running_times.append(total_iteration_time)
        if printout: print(f"Finished loop iteration ({round(total_iteration_time, 3)}s)")
        if len(running_times) == 6:
            running_times.pop(0)
        if len(running_times) == 5:
            if printout: print(f"~~~5-point moving average ({round(sum(running_times)/5, 3)}s)~~~")