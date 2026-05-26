#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GitHub Actions 环境下读取存档，生成 GitHub Pages 需要的 JSON"""

import json
import os
import sys

data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
archive_path = os.path.join(data_dir, "latest.json")

if os.path.exists(archive_path):
    with open(archive_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(json.dumps(data, ensure_ascii=False, indent=2))
else:
    print(json.dumps({"error": "no data"}))
    sys.exit(1)