#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from . import config

__all__ = ["MockConfig"]

class MockConfig(config.Config):
    """docstring for MockConfig."""
    def __init__(self):
        config = {
            "token": "xxx",
            "owner": "xxx",
            "repo": "xxx",
            "branch": "xxx",
            "commit_id": "xxx"
        }
        super().__init__(config)

if __name__ == "__main__":
    pass
