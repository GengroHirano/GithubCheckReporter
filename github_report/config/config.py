#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__all__ = ["Config"]

class Config():
    """docstring for Config."""
    def __init__(self, config):
        self._token = config['token']
        self._owner = config['owner']
        self._repo = config['repo']
        self._branch = config['branch']
        self._commit_id = config['commit_id']

    @property
    def token(self):
        return self._token

    @property
    def owner(self):
        return self._owner

    @property
    def repo(self):
        return self._repo

    @property
    def branch(self):
        return self._branch

    @property
    def commit_id(self):
        return self._commit_id

if __name__ == "__main__":
    pass
