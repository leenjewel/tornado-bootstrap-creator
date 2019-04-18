#!/usr/bin/env python

import argparse
from tornado_bootstrap_creator.creator import run

if __name__ == '__main__' :
    parser = argparse.ArgumentParser()
    parser.add_argument("command", nargs = '+', default = [], help = "[new_project]")

    parser.add_argument("--prefix", default = ".", help = "New project path")
    parser.add_argument('--force', action = 'store_true', default = False, help = 'Create project mandatory')
    parser.add_argument("--package", default = None, help = 'Project package name')
    parser.add_argument('--author', default = 'anonymous', help = 'Project author name')
    parser.add_argument('--email', default = 'anonymous@anonymous.com', help = 'Project author email')
    parser.add_argument('--url', default = '', help = 'Project python package url')
    parser.add_argument('--license', default = 'http://www.apache.org/licenses/LICENSE-2.0', help = 'Project license url')
    parser.add_argument('--name', default = 'project name', help = 'Project display name')
    parser.add_argument('--descript', default = 'project description', help = 'Project display description')
    parser.add_argument('--logo', default = None, help = 'Project logo image path')
    parser.add_argument('--admin_user', default = 'admin', help = 'Project administrator name')
    parser.add_argument('--admin_password', default = 'admin', help = 'Project administrator password')
    parser.add_argument('--routes', default = None, help = 'Project routes configure like: your/url/path:YourHandler.name;')
    parser.add_argument('--port', default = 8080, help = 'Project web server listen port')
    
    args = parser.parse_args()
    run(args)
