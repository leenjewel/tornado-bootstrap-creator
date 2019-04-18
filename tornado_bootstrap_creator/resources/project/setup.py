#!/usr/bin/env python

import os
from setuptools import setup

package_data = []
setup_dir = os.path.split(os.path.realpath(__file__))[0]
package_dir = os.path.join(setup_dir, '{{ package }}')

for root, dirs, files in os.walk(package_dir) :
    for data_file in files :
        if not data_file.startswith('.') and \
            not data_file.endswith('.py') and \
            not data_file.endswith('.pyc') :
            package_data.append('.' + os.path.join(root.replace(package_dir, ''), data_file))

setup(
    name = "{{ project_name }}",
    version = "1.0.0",
    keywords = ("tornado", "bootstrap", "web"),
    description = "{{ project_description }}",
    license = "{{ project_license }}",
    url = "{{ project_url }}",
    author = "{{ project_author }}",
    author_email = "{{ project_author_email }}",
    packages = ["{{ package }}"],
    package_data = {
        "{{ package }}" : package_data,
    },
    include_package_data = True,
    platforms = "any",
    install_requires = [
        "tornado",
    ],
    scripts = [
        "{{ project_command }}.py",
    ],
)

