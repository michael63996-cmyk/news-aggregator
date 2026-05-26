#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""汽车行业技术新闻抓取（RSS）"""

import feedparser
import json
import requests
from bs4 import BeautifulSoup
from config import AUTO_NEWS_RSS


def fetch_rss(url: str) -> list:
    """解析 RSS 订阅源"""
    try:
        feed = feedparser.parse(url)
        items = []
        for entry in feed.entries[:10]:  # 最多10条
            items.append({
                "title": entry.get("title", ""),
                "link": entry.get("link", ""),
                "date": entry.get("published", "")[:16],
                "summary": entry.get("summary", "")[:200],
            })
        return items
    except Exception as e:
        return [{"error": str(e), "url": url}]


def fetch_huxiu_auto() -> list:
    """虎嗅汽车（HTML解析）"""
    try:
        resp = requests.get(
            "https://www.huxiu.com/channel/103.html",
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=10
        )
        soup = BeautifulSoup(resp.text, "html.parser")
        items = []
        for art in soup.select(".article-list .item")[:10]:
            title_tag = art.select_one(".article--title")
            link_tag = art.select_one("a")
            if title_tag and link_tag:
                items.append({
                    "title": title_tag.text.strip(),
                    "link": "https://www.huxiu.com" + link_tag.get("href", ""),
                    "date": "",
                    "summary": "",
                })
        return items
    except Exception as e:
        return [{"error": str(e)}]


def fetch_all_news() -> dict:
    """获取所有汽车新闻"""
    results = {}

    for source in AUTO_NEWS_RSS:
        results[source["name"]] = fetch_rss(source["url"])

    # 虎嗅单独处理
    results["虎嗅汽车"] = fetch_huxiu_auto()

    return results


def format_news_md(news: dict, max_per_source: int = 3) -> str:
    """格式化成 Markdown"""
    lines = ["🚗 **汽车行业技术新闻**\n"]

    for name, items in news.items():
        lines.append(f"**{name}**")
        shown = 0
        for item in items:
            if "error" in item:
                lines.append(f"- ⚠️ 获取失败：{item['error']}")
                continue
            if shown >= max_per_source:
                break
            title = item["title"][:40]
            link = item["link"]
            lines.append(f"- [{title}]({link})")
            shown += 1
        lines.append("")

    return "\n".join(lines[:-1])  # 去掉最后多余空行


if __name__ == "__main__":
    news = fetch_all_news()
    print(json.dumps(news, ensure_ascii=False, indent=2))
    print("\n--- Markdown ---\n")
    print(format_news_md(news))