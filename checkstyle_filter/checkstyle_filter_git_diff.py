#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import xml.etree.ElementTree as et

import click

from git import diff

@click.command()
@click.option('--branch', '-b', default='origin/master', help="target branch. default origin/master")
def process(branch):
    # catで吐き出される標準出力のやつを一本にまとめる
    xml = [line for line in sys.stdin]
    xml = map(str, xml)
    xml_text = "".join(xml)

    # xmlをパースする
    parser = et.fromstring(xml_text)
    # 差分が見られるファイルを取り出す
    diff_files = diff.diff(branch)
    if not diff_files:
        return # 差分が取れなければ何もしない

    # xmlの編集
    for element in parser.iter():
        if 'name' not in element.attrib.keys():
            continue

        # name属性を持つエレメントは変更されたファイルのlocationを持っているのでファイル名を取得
        attr_file = element.get('name')
        contains_path = [s for s in diff_files if s in attr_file]
        if len(contains_path) == 0:
            remove_element = element.findall('error')
            for dispose in remove_element:
                element.remove(dispose)
        else:
            child_element = element.findall('error')
            for child in child_element:
                child.set("path", contains_path[0])

    print(et.tostring(parser, encoding="unicode"))

def main():
    process()

if __name__ == '__main__':
    main()
