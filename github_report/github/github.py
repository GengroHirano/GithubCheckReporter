#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
wercker専用のレポーターになってる。誰か直してくれるとありがたいなぁ
(丸写s)参考: http://qiita.com/giwa/items/a4c9395b895000407634
"""

import os
import json

import requests
import pprint

from . import diff_parser
from . import hunk_parser
from config import mock_config


__all__ = ['Github']

BASE_URL = "https://api.github.com"
GET_PULLURL_TMP = "{base_url}/repos/{org}/{repo}/pulls"
CACHE_FILE = '/tmp/github_pull_info'
CACHE_DIFF_DATA = '/tmp/github_diff'

class Github():
    def __init__(self, config):

        self.TOKEN = config.token
        self.ORG = config.owner
        self.REPO = config.repo
        self.COMMIT_ID = config.commit_id
        self.branch = config.branch

        self._pull_info = None
        self._diff_info = None
        self._pull_files_info = None

        self._headers = {'Content-Type': 'application/json',
                         'Authorization': 'token ' + self.TOKEN}
        if os.path.isfile(CACHE_FILE):
            self._read_pull_info_cache()
        else:
            self._get_pull_info()
            self._write_cache(CACHE_FILE, json.dumps(self._pull_info))

        if os.path.isfile(CACHE_DIFF_DATA):
            self._read_diff_cache()
        else:
            self._get_diff_data()
            self._write_cache(CACHE_DIFF_DATA, self._diff_info)

    def _generate_pulls_url(self):
        """
        Generate pull url
        HOST/repos/:owner/:repo/pulls
        """
        return GET_PULLURL_TMP.format(base_url=BASE_URL, org=self.ORG, repo=self.REPO)

    def _get_pull_info(self):
        """
        Get pull infor using pull API
        There is an assumption that one branch is used for one PR
        """
        url = self._generate_pulls_url()
        params = {'head': self.ORG + ":" + self.branch}
        r = requests.get(url, headers=self._headers, params=params)
        print(r.text)
        if r.status_code == 200:
            self._pull_info = json.loads(r.text)

    def _generate_pull_files_url(self):
        """
        Generate pull files url
        HOST/repos/:owner/:repo/pulls/:num/files
        """
        return "{pulls_url}/{num}".format(
            pulls_url=self._generate_pulls_url(),
            num=self._pull_info[0]['number']
        )
        # return "{0}".format(self._pull_info[0]['_links']['commits']['href'])

    def _get_pulls_file(self):
        url = self._generate_pull_files_url()
        r = requests.get(url, headers=self._headers)
        if r.status_code == 200:
            self._pull_files_info = json.loads(r.text)
            # pprint.pprint(self._pull_files_info)

    def _generate_self_url(self):
        """
        Generate review comment url
        HOST/repos/:owner/:repo/pulls/:num
        """
        return self._pull_info[0]['_links']['self']['href']

    def _get_diff_data(self):
        url = self._generate_self_url()
        r = requests.get(url, headers=self._headers)

        diff_url = None
        if r.status_code == 200:
            data = json.loads(r.text)
            diff_url = data['diff_url']

        if diff_url is not None:
            r = requests.get(diff_url, headers=self._headers)
            if r.status_code == 200:
                self._diff_info = r.text

    def _generate_review_comment_url(self):
        """
        Generate review comment url
        HOST/repos/:owner/:repo/pulls/:num/comments
        """
        return self._pull_info[0]['_links']['comments']['href']
        # return "{base}/repos/{owner}/{repos}/pulls/9/reviews".format(base=BASE_URL, owner=ORG, repos=REPO)

    def _generate_comment_url(self):
        """
        Generate comment url
        HOST/repos/:owner/:repo/issues/:num/comments
        """
        return self._pull_info[0]['issue_url'] + '/comments'

    def _write_cache(self, cache, data):
        with open(cache, 'w') as f:
            f.write(data)
            f.flush()

    def _read_pull_info_cache(self):
        l = None
        with open(CACHE_FILE, 'r') as f:
            l = f.readlines()[0]
        if l and self._pull_info == None:
            self._pull_info = json.loads(l)

    def _read_diff_cache(self):
        l = None
        with open(CACHE_DIFF_DATA, 'r') as f:
            l = "".join(f.readlines())
        print(l)
        if l and self._diff_info == None:
            self._diff_info = l

    def dump_infos(self, path, line):
        data = self._diff_info
        hunk_data = diff_parser.parse(data, path)
        relative_line = hunk_parser.parse(path, line, hunk_data)
        print("=====================")
        hunk_parser.print_hunk_graph(hunk_data)
        print("relative_line {0}".format(relative_line))

    def review_comment(self, comment, line, path):
        """ Post review comment for this PR """
        url = self._generate_review_comment_url()
        commit_id = self.COMMIT_ID
        data = self._diff_info
        hunk_data = diff_parser.parse(data, path)
        relative_line = hunk_parser.parse(path, line, hunk_data)
        if relative_line <= 0:
            print("line not fund")
            return
        data = json.dumps({'body': comment, 'commit_id': commit_id, 'path': path, 'position':relative_line})
        r = requests.post(url, headers=self._headers, data=data)

    def issue_comment(self, comment):
        """ Post issue comment for this PR """
        url = self._generate_comment_url()
        data = json.dumps({'body': comment})
        r = requests.post(url, headers=self._headers, data=data)

if __name__ == "__main__":
    github = GitHub()
    comment = 'test'
    github.issues_comment()
