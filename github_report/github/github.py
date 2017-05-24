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

from . import hunk_parser
from config import mock_config


__all__ = ['Github']

BASE_URL = "https://api.github.com"
GET_PULLURL_TMP = "{base_url}/repos/{org}/{repo}/pulls"
CACHE_FILE = '/tmp/github_pull_info'

class Github():
    def __init__(self, config):

        self.TOKEN = config.token
        self.ORG = config.owner
        self.REPO = config.repo
        self.COMMIT_ID = config.commit_id
        self.branch = config.branch

        self._pull_info = None
        self._pull_files_info = None

        self._headers = {'Content-Type': 'application/json',
                         'Authorization': 'token ' + self.TOKEN}
        if os.path.isfile(CACHE_FILE):
            self._read_cache()
        else:
            self._get_pull_info()
            self._write_cache()

        self._get_pulls_file()

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
        return "{pulls_url}/{num}/files".format(
            pulls_url=self._generate_pulls_url(),
            num=self._pull_info[0]['number']
        )
        # return "{0}".format(self._pull_info[0]['_links']['commits']['href'])

    def _get_pulls_file(self):
        url = self._generate_pull_files_url()
        print(url)
        r = requests.get(url, headers=self._headers)
        if r.status_code == 200:
            self._pull_files_info = json.loads(r.text)
            # pprint.pprint(self._pull_files_info)

    def _generate_review_comment_url(self):
        """
        Generate review comment url
        HOST/repos/:owner/:repo/pulls/:num/comments
        """
        return self._pull_info[0]['_links']['commits']['href']
        # return "{base}/repos/{owner}/{repos}/pulls/9/reviews".format(base=BASE_URL, owner=ORG, repos=REPO)

    def _generate_comment_url(self):
        """
        Generate comment url
        HOST/repos/:owner/:repo/issues/:num/comments
        """
        return self._pull_info[0]['issue_url'] + '/comments'

    def _write_cache(self):
        with open(CACHE_FILE, 'w') as f:
            f.write(json.dumps(self._pull_info))
            f.flush()

    def _read_cache(self):
        l = None
        with open(CACHE_FILE, 'r') as f:
            l = f.readlines()[0]
        if l and self._pull_info == None:
            self._pull_info = json.loads(l)


    def dump_infos(self, path, line):
        # hunk_parser.prity_print(self._pull_info)
        # relative_line = hunk_parser.parse(path, line, self._pull_files_info)
        hunk_parser.print_hunk_graph(self._pull_files_info)
        print(relative_line)

    def review_comment(self, comment, line, path):
        """ Post review comment for this PR """
        url = self._generate_review_comment_url()
        commit_id = self.COMMIT_ID
        relative_line = hunk_parser.parse(path, line, self._pull_files_info)
        if relative_line <= 0:
            print("line not fund")
            return
        print(relative_line)
        # data = json.dumps({'body': comment, 'commit_id': commit_id, 'path': path, 'position':relative_line})
        # r = requests.post(url, headers=self._headers, data=data)
        # print(r.text)

    def issue_comment(self, comment):
        """ Post issue comment for this PR """
        url = self._generate_comment_url()
        data = json.dumps({'body': comment})
        r = requests.post(url, headers=self._headers, data=data)

if __name__ == "__main__":
    github = GitHub()
    comment = 'test'
    github.issues_comment()
