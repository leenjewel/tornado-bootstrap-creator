#!/usr/bin/env python

import os
import sys
import json
try :
    reload(sys)
    sys.setdefaultencoding('utf8')
except NameError :
    pass
import argparse
from {{ package }}.web import Application, ApplicationDaemon

def startweb(args):
    settings = {}
    if args.config is not None and os.path.isfile(args.config) :
        with open(args.config, "r") as fp :
            settings = json.load(fp)
        os.chdir(os.path.split(args.config)[0])
    else :
        os.chdir(args.workspace)

    if args.daemon :
        ApplicationDaemon(settings).run(args.port)
    else :
        Application(settings).run(args.port)


def stopweb(args):
    settings = {}
    if args.config is not None and os.path.isfile(args.config) :
        with open(args.config, "r") as fp :
            settings = json.load(fp)
        os.chdir(os.path.split(args.config)[0])
    else :
        os.chdir(args.workspace)
    ApplicationDaemon(settings).stop()



if __name__ == '__main__' :
    parser = argparse.ArgumentParser()
    parser.add_argument("command", nargs = '+', default = [], help = "[ startweb stopweb ]")

    # startweb & stopweb
    parser.add_argument('--config', default = None, help = "Web server configure file path")
    parser.add_argument('--port', default = {{ port }}, help = "Web server listen port")
    parser.add_argument('--daemon', action = 'store_true', default = False, help = "Start web server with daemon")
    parser.add_argument('--workspace', default = os.getcwd(), help = "Web server work dir")

    args = parser.parse_args()

    method_name = args.command[0]
    possibles = globals().copy()
    possibles.update(locals())
    method = possibles.get(method_name)
    method(args)
