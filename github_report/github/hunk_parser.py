#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pprint
import re


def _hunk_graph(patch_data):

    """
    相対的な行数(hunk内での行数), 追加変更の行数(add), 削除変更の行数(delete)を求める
    他にもpath_dataに対してhunk headerを求める処理も入れているのでLineクラスを作ったほうが良いかも
    """
    diff_text = patch_data
    relative_line = []
    additional_line = []
    delete_line = []
    real_line_section = []
    offset_hunk = []

    hunk_header_hit_count = 0
    for line_number in range(0, len(diff_text)):
        # print(diff_text[line_number])
        """
        hunkデータをもとにhunk graph(仮名)を作る
        print_hunk_graphで確認してみると良い
        """
        relative_line.append(line_number)
        if re.match("^\+(?!\+|\+)",diff_text[line_number]):
            additional_line.append(line_number)
        elif re.match("^\-(?!\-|\-)",diff_text[line_number]):
            delete_line.append(line_number)
        else:
            additional_line.append(line_number)
            delete_line.append(line_number)

        """
        hunk headerとhunk header間の行数と
        hunk headerに含まれているheaderが挿入されている実際の行数を取り出す

        hunk headerはこのようなフォーマット
        @@ -47,10 +47,10 @@

        一行ずつ探索しリスト形式にした後に数値を取り出す
        [@@ -47,10 +47,10 @@, @@ -77,7 +77,7 @@]
        section = [47, 77]

        hunk headerはoffsetを割り出すための行数に含めない
        offset_hunk = [0, {15 - hunk_header_hit_count}, ..., {n - hunk_header_hit_count}]
        """
        result = re.search("@@.+?@@", diff_text[line_number])
        if result is not None:
            real_line_number = re.search("(?<=\+)(.*)", result.group(0))
            real_line_section.append(real_line_number.group(0).split(",")[0])
            if line_number == 0:
                offset_hunk.append(0)
            else:
                hunk_header_hit_count += 1
                offset_hunk.append(line_number - hunk_header_hit_count)
            continue


    # print(relative_line)
    # print(additional_line)
    # print(delete_line)
    return relative_line, additional_line, delete_line, real_line_section, offset_hunk

# TODO ロジックに無駄が有りすぎて…助けてくれ
def parse(path, real_line_number, hunk_data):
    hunk = hunk_data
    if hunk == None:
        return
    if hunk['filename'] != path:
        return

    print("filename {0}".format(hunk['filename']))
    relative_line, additional_line, delete_line, real_line_section, offset_hunk = _hunk_graph(hunk['patch'])

    """
    実際に変更があった行数から変更があった行数を差し引き相対的な行数を求める
    print_hunk_graphで確認してみると良い
    """
    offset_index = 0
    for section_index in range(0, len(real_line_section)):
        if section_index == len(real_line_section):
            offset_index = section_index
            break
        if int(real_line_number) in range(int(real_line_section[section_index])):
            break
        offset_index += 1

    line_index = int(real_line_number) - int(real_line_section[offset_index -1])
    offset = offset_hunk[offset_index - 1]
    if offset == 0:
        line_index += 1
    else:
        line_index += offset
    return additional_line[relative_line[line_index]]

def print_hunk_graph(hunk_data):
    hunk = hunk_data
    if hunk == None:
        return
    print("filename {0}".format(hunk['filename']))

    diff_text = hunk['patch']
    relative_line = []

    additional_line = []
    offset_additional_line = []
    additional_offset = 0

    delete_line = []
    offset_delete_line = []
    delete_offset = 0

    for line_number in range(0, len(diff_text)):
        relative_line.append(line_number)
        print(diff_text[line_number])
        if re.match("^\+(?!\+|\+)",diff_text[line_number]):
            # 本ちゃん
            additional_line.append(line_number)
            # デバッグ用に見やすくしてるやつ
            offset_additional_line.append(line_number - additional_offset)
            offset_delete_line.append('-')
            delete_offset += 1
        elif re.match("^\-(?!\-|\-)",diff_text[line_number]):
            # 本ちゃん
            delete_line.append(line_number)
            # デバッグ用に見やすくしてるやつ
            offset_delete_line.append(line_number - delete_offset)
            offset_additional_line.append('+')
            additional_offset += 1
        else:
            # 本ちゃん
            additional_line.append(line_number)
            delete_line.append(line_number)
            # デバッグ用に見やすくしてるやつ
            offset_additional_line.append(line_number - additional_offset)
            offset_delete_line.append(line_number - delete_offset)

    print("_付きはデバッグ用だったりするのねん")
    print("line: {line}".format(line=relative_line))
    print("add_: {line}".format(line=offset_additional_line))
    print("del_: {line}".format(line=offset_delete_line))
    print("add : {line}".format(line=additional_line))
    print("del : {line}".format(line=delete_line))
