import datetime
import sys

log_file= "lvdsl_outputs/log.txt"
write_log = True

def set(option, value):
    ## Set global variable
    ## Variables:
    #### log_file: log file path
    #### write_log: True/False
    for key in option:
        globals()[key] = value

def print_log(message, end="\n"):
    str_date=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{str_date}] {message}", end=end)
    sys.stdout.flush()
    with open("log.txt", "a") as f:
        f.write(f"[{str_date}] {message}{end}")
        f.flush()

