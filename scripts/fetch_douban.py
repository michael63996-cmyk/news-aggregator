#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""豆瓣读书推荐抓取（RSS）"""

import feedparser
import json
from config import DOUBAN_BOOK_RSS


def fetch_douban_books() -> list:
    """获取豆瓣读书推荐（公开RSS，无需登录）"""
    try:
        feed = feedparser.parse(DOUBAN_BOOK_RSS)

        items = []
        for entry in feed.entries[:10]:
            # 标题可能包含书名
            title = entry.get("title", "")
            link = entry.get("link", "")
            # 豆瓣RSS的summary是HTML描述
            summary = ""
            if hasattr(entry, "summary"):
                # 去掉HTML标签，取纯文本前100字
                import re
                summary = re.sub(r"<[^>]+>", "", entry.summary)[:100]

            items.append({
                "title": title,
                "link": link,
                "date": entry.get("published", "")[:16],
                "summary": summary,
            })
        return items
    except Exception as e:
        return [{"error": str(e)}]


def format_douban_md(books: list, max_books: int = 5) -> str:
    """格式化成 Markdown"""
    lines = ["📚 **豆瓣读书推荐**\n"]

    for i, book in enumerate(books[:max_books]):
        if "error" in book:
            lines.append(f"- ⚠️ 获取失败：{book['error']}")
            continue
        title = book["title"][:40]
        link = book["link"]
        lines.append(f"- [{title}]({link})")
        if book.get("summary"):
            lines.append(f"  _{book['summary'][:60]}..._")

    return "\n".join(lines)


if __name__ == "__main__":
    books = fetch_douban_books()
    print(json.dumps(books, ensure_ascii=False, indent=2))
    print("\n--- Markdown ---\n")
    print(format_douban_md(books))