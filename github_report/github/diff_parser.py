#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pprint
import re

def parse(data, path):
    """
    取得したdiffデータをパースし、辞書形式に成形する
    [{filename: <filename>, body: <hunk_text>}, ...]
    """
    add_regex = "^\+\+\+\sb/({path}.*)".format(path=path)
    delete_regex = "^\-\-\-"

    hunk_data = []
    chunk = None
    filename = ''
    lines = data.split('\n')
    # ここも酷いなぁ
    for line in lines:
        diff_chunk = []
        match = re.match("^(diff --git)", line)
        if match is not None:
            chunk = {'filename': '', 'patch': []}
            hunk_data.append(chunk)
        else:
            if re.match(add_regex, line):
                chunk['filename'] = path
                continue
            elif re.match(delete_regex, line):
                continue
            elif re.match("^(index ).*" , line):
                continue
            elif len(chunk['filename']) == 0:
                continue
            else:
                chunk['patch'].append(line)

    data = [data for data in hunk_data if len(data['filename']) > 0]
    return data[0]
