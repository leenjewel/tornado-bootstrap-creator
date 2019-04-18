#!/usr/bin/env python

import os
from setuptools import setup

package_data = []
setup_dir = os.path.split(os.path.realpath(__file__))[0]
package_dir = os.path.join(setup_dir, 'tornado_bootstrap_creator')

for root, dirs, files in os.walk(package_dir) :
    for data_file in files :
        if not data_file.startswith('.') and \
            not data_file.endswith('.py') and \
            not data_file.endswith('.pyc') :
            package_data.append('.' + os.path.join(root.replace(package_dir, ''), data_file))

setup(
    name = "tornado_bootstrap_creator",
    version = "1.0.0",
    keywords = ("tornado", "bootstrap", "web"),
    description = "Tornado bootstrap style project creator",
    license = "http://www.apache.org/licenses/LICENSE-2.0",
    url = "https://github.com/leenjewel/tornado-bootstrap-creator",
    author = "leenjewel",
    author_email = "leenjewel@gmail.com",
    packages = ["tornado_bootstrap_creator"],
    package_data = {
        "tornado_bootstrap_creator" : package_data,
    },
    include_package_data = True,
    platforms = "any",
    install_requires = [
        "Jinja2",
        "tornado",
    ],
    scripts = [
        "tornado-bootstrap-creator.py",
    ],
)

