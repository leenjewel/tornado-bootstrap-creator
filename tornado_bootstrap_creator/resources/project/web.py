import sys
import os
import atexit
import time
from signal import SIGTERM
import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.httpclient
import tornado.locale
import operator
from {{ package }}.routes import routes
import {{ package }}.uimodules

pwd = os.path.split(os.path.realpath(__file__))[0]
default_settings = {
    "debug" : False,
}
app_settings = {
    "ui_modules" : {{ package }}.uimodules,
    "template_path" : os.path.join(pwd, "templates"),
    "static_path" : os.path.join(pwd, "resources"),
}

class Application(tornado.web.Application):

    def __init__(self, user_settings):
        self.settings = {
            "login_url" : "/login",
            "cookie_secret" : "{{ secret }}",
            "login_user" : "{{ admin_user }}",
            "login_password" : "{{ admin_password }}",
        }
        self.settings.update(default_settings)
        self.settings.update(user_settings)
        self.settings.update(app_settings)

        i18n_path = os.path.join(os.path.dirname(__file__), 'locales')
        # tornado.locale.load_gettext_translations(i18n_path, 'en_US')
        tornado.locale.load_translations(i18n_path)
        tornado.locale.set_default_locale('zh_CN')

        tornado.web.Application.__init__(self, routes, **self.settings)


    def run(self, port = 8080) :
        http_server = tornado.httpserver.HTTPServer(self)
        http_server.listen(port)
        tornado.ioloop.IOLoop.current().start()


class ApplicationDaemon(object) :

    def __init__(self, user_settings) :
        self.settings = user_settings


    def pidfile(self) :
        pid_file = self.settings.get("pidfile")
        if None is pid_file or len(pid_file) == 0 :
            pid_file = os.path.join(os.getcwd(), "{{ package }}.pid")
        return pid_file


    def daemonize(self) :
        try :
            if os.fork() > 0 :
                sys.exit(0)
        except OSError as e :
            sys.stderr.write("fork #1 failed : %d %s\n"  %(e.errno, e.strerror))
            sys.exit(1)

        os.setsid()
        os.umask(0)

        try :
            if os.fork() > 0 :
                sys.exit(0)
        except OSError as e:
            sys.stderr.write("fork #2 failed : %d %s\n"  %(e.errno, e.strerror))
            sys.exit(1)

        sys.stdout.flush()
        sys.stderr.flush()

        stdout_file = self.settings.get("stdout")
        if None is stdout_file or len(stdout_file) == 0 :
            stdout_file = os.path.join(os.getcwd(), "std.out")
        stdout = open(stdout_file, "a+")
        os.dup2(stdout.fileno(), sys.stdout.fileno())

        stderr_file = self.settings.get("stderr")
        if None is stderr_file or len(stderr_file) == 0 :
            stderr_file = os.path.join(os.getcwd(), "std.err")
        stderr = open(stderr_file, "a+", 1)
        os.dup2(stderr.fileno(), sys.stderr.fileno())

        atexit.register(self.delpid)
        pid = str(os.getpid())
        pid_file = self.pidfile()
        pid_fp = open(pid_file, 'w+')
        pid_fp.write("%s\n"  %(pid))
        pid_fp.close()


    def delpid(self) :
        os.remove(self.pidfile())


    def getpid(self) :
        try :
            with open(self.pidfile(), "r") as pid_fp :
                pid = int(pid_fp.read().strip())
        except IOError :
            pid = None
        return pid


    def start(self) :
        pid = self.getpid()
        if pid :
            sys.stderr.write("pid file %s already exist. Daemon already running?\n"  %(self.pidfile()))
            sys.exit(1)

        self.daemonize()

        Application(self.settings).run(self.settings.get("port", 8080))


    def stop(self) :
        pid = self.getpid()
        if not pid :
            sys.stderr.write("pid file %s not exists. Daemon not running?\n"  %(self.pidfile()))
            return

        try :
            while True :
                os.kill(pid, SIGTERM)
                time.sleep(0.1)
        except OSError as e :
            error = str(e)
            if error.find("No such process") > 0 :
                if os.path.exists(self.pidfile()) :
                    os.remove(self.pidfile())
            else :
                sys.stderr.write(error)
                sys.exit(1)


    def restart(self) :
        self.stop()
        time.sleep(0.5)
        self.start()


    def run(self, port = None) :
        if port :
            self.settings["port"] = port
        self.start()



if __name__ == "__main__" :
    import json, argparse
    parser = argparse.ArgumentParser()

    parser.add_argument('config', help = "Config file path")

    parser.add_argument('--port', default=8080, help = "Listen port")

    parser.add_argument('--daemon', action = 'store_true', default = False, help = "Start server with daemon")

    args = parser.parse_args()

    if not os.path.isfile(args.config) :
        raise Exception("%s not found."  %(args.config))
    fp = open(args.config, "r")
    settings = json.load(fp)
    fp.close()
    os.chdir(os.path.split(args.config)[0])

    if args.daemon :
        ApplicationDaemon(settings).run(args.port)
    else :
        Application(settings).run(args.port)

