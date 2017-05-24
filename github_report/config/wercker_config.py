#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from . import config

__all__ = ["WerckerConfig"]

class WerckerConfig(config.Config):
    """docstring for WerckerConfig."""
    def __init__(self):
        config = {
            "token": os.environ['GITHUB_ACCESS_TOKEN'],
            "owner": os.environ['WERCKER_GIT_OWNER'],
            "repo": os.environ['WERCKER_GIT_REPOSITORY'],
            "branch": os.environ['WERCKER_GIT_BRANCH'],
            "commit_id": os.environ['WERCKER_GIT_COMMIT']
        }
        super().__init__(config)

if __name__ == "__main__":
    pass
