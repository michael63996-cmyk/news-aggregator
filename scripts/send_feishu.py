#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""飞书推送"""

import json
import requests
import sys
from config import FEISHU_WEBHOOK


def send_text(text: str, webhook: str = None) -> bool:
    """发送文本消息到飞书"""
    webhook = webhook or FEISHU_WEBHOOK

    payload = {
        "msg_type": "text",
        "content": {"text": text}
    }

    try:
        resp = requests.post(webhook, json=payload, timeout=10)
        result = resp.json()
        if result.get("code") == 0:
            print("✅ 飞书消息发送成功")
            return True
        else:
            print(f"❌ 发送失败：{result}")
            return False
    except Exception as e:
        print(f"❌ 请求异常：{e}")
        return False


def send_markdown(md: str, webhook: str = None) -> bool:
    """发送 Markdown 消息到飞书（富文本）"""
    webhook = webhook or FEISHU_WEBHOOK

    payload = {
        "msg_type": "interactive",
        "card": {
            "header": {
                "title": {"tag": "plain_text", "content": "📬 今日资讯汇总"},
                "template": "blue"
            },
            "elements": [
                {
                    "tag": "markdown",
                    "content": md
                }
            ]
        }
    }

    try:
        resp = requests.post(webhook, json=payload, timeout=10)
        result = resp.json()
        if result.get("code") == 0:
            print("✅ 飞书消息发送成功")
            return True
        else:
            print(f"❌ 发送失败：{result}")
            return False
    except Exception as e:
        print(f"❌ 请求异常：{e}")
        return False


if __name__ == "__main__":
    # 支持命令行调用：python send_feishu.py "消息内容"
    if len(sys.argv) > 1:
        send_text(sys.argv[1])
    else:
        # 从 stdin 读取
        text = sys.stdin.read()
        send_text(text)