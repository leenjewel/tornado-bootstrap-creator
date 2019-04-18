import os
import sys
import time
import subprocess
import datetime

def gen_datetime_for(dt_from, dt_to = None, level = 'day', fmt = None):
    ts_from = string_to_timestamp(dt_from)
    if dt_to is None :
        dt_to = timestamp_to_string(ts_from + 86400)
    ts_to = string_to_timestamp(dt_to)
    t = 86400
    if level == 'hour' :
        t = 3600
    elif level == 'week' :
        t = 7*86400
    if ts_to < ts_from + t :
        ts_to = ts_from + t
    for fr in range(ts_from, ts_to, t):
        yield timestamp_to_string(fr, fmt)


def timestamp_to_string(ts = None, level = None):
    if ts is None:
        ts = time.time()
    ts = int(ts)
    if ts <= 0 :
        return ""
    d = datetime.datetime.fromtimestamp((ts))
    f = '%Y-%m-%d %H:%M:%S'
    if level == 'day' :
        f = '%Y-%m-%d'
    elif level == 'hour' :
        f = '%Y-%m-%d %H:00:00'
    elif level == 'minutes' :
        f = '%Y-%m-%d %H:%M:00'
    elif level is not None:
        f = level
    return d.strftime(f)


def date_to_string(ts = None):
    if ts is None:
        ts = time.time()
    d = datetime.datetime.fromtimestamp(int(ts))
    return d.strftime('%Y-%m-%d')


def string_to_datetime(dstr):
    dts = dstr.split(' ')
    dl = [int(x) for x in dts[0].split('-')]
    if len(dts) > 1 :
        dl += [int(x) for x in dts[1].split(':')]
    return datetime.datetime(*dl[:4])


def string_to_timestamp(dstr):
    if dstr.strip() == "" :
        return 0
    dt = string_to_datetime(dstr)
    return int(time.mktime(dt.timetuple()))


def is_exe(file_path) :
    return (os.path.isfile(file_path) and os.access(file_path, os.X_OK))


def which(exe, path = None):
    file_path, _ = os.path.split(exe)
    if file_path and is_exe(exe):
        return exe
    else :
        if None == path :
            path = os.environ["PATH"]
        for file_path in path.split(os.pathsep) :
            file_path = file_path.strip('"')
            exe_file = os.path.join(file_path, exe)
            if is_exe(exe_file) :
                return exe_file
    return None


def runcommand(*command_list, **options):
    stdout = options.get("stdout")
    if not stdout :
        stdout = subprocess.PIPE
    stderr = options.get("stderr")
    if not stderr :
        stderr = subprocess.PIPE
    pipe = subprocess.Popen(command_list, stdout = stdout, stderr = stderr)

    has_run_time = 0
    sleep_time = options.get("sleep", 5)
    max_wait_time = options.get("wait", 120)

    if options.get("showcommand", False) :
        stdout.write(" ".join(command_list) + "\n")
        stdout.flush()

    while None is pipe.poll():
        time.sleep(sleep_time)
        has_run_time += sleep_time
        if has_run_time >= max_wait_time :
            stderr.write("subprocess has run more "+str(has_run_time)+" seconds, need to be killed")
            pipe.kill()
            break
    return pipe.poll()

