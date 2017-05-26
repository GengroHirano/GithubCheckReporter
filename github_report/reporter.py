#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import xml.etree.ElementTree as et
from github import github
from config import mock_config as config

github = github.Github(config.MockConfig())
for line in sys.stdin:
    if 'error' in line != 0:
        element = et.fromstring(line)
        line = element.get('line')
        path = element.get('path')
        message = element.get('message')
        level = element.get('severity')
        body = "指摘点です\n[{0}]: {1}".format(level.upper(), message)
        github.review_comment(
            path=path,
            comment=body,
            line=line
        )
        # github.dump_infos(path=path, line=line)
