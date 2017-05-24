#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess

# 差分があったファイル名のみを抽出する
def diff(target_branch):
    diff = subprocess.getoutput("git diff --name-only {branch}".format(branch=target_branch))
    if not diff:
        return []
    else:
        # この分け方はセンス無いよなぁ...
        return [x for x in diff.split('\n')]
