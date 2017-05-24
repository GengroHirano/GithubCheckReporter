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
        message = "良いのか〜？\n{0}".format(message)
        github.review_comment(
            path=path,
            comment=message,
            line=line
        )
        # github.dump_infos(path=path, line=line)

        # github.dump_infos(path, line)
        # issue_message = "path: {path} \n line: {line} \n message={message}".format(
        #     path=path,
        #     line=line,
        #     message=message
        # )
        # github.issue_comment(comment=issue_message)
