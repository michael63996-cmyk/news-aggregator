#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""主脚本：抓取所有数据并推送"""

import json
import sys
import os
from datetime import datetime

# 确保脚本目录在 path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fetch_stock import fetch_all_stocks, format_stock_md
from fetch_auto_news import fetch_all_news, format_news_md
from fetch_douban import fetch_douban_books, format_douban_md
from send_feishu import send_markdown


def main():
    print(f"🔄 开始抓取... {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # 1. 股市
    print("📊 抓取股市行情...")
    stocks = fetch_all_stocks()
    print(f"   成功 {sum(1 for s in stocks if 'error' not in s)}/{len(stocks)} 条")

    # 2. 汽车新闻
    print("🚗 抓取汽车新闻...")
    news = fetch_all_news()
    total_news = sum(len(v) for v in news.values())
    print(f"   成功 {sum(len(v) for v in news.values())} 条")

    # 3. 豆瓣
    print("📚 抓取豆瓣读书...")
    books = fetch_douban_books()
    print(f"   成功 {sum(1 for b in books if 'error' not in b)}/{len(books)} 条")

    # 4. 汇总
    print("\n📦 组装消息...")
    stock_md = format_stock_md(stocks)
    news_md = format_news_md(news)
    douban_md = format_douban_md(books)

    date_str = datetime.now().strftime("%Y-%m-%d")
    full_md = f"**📅 {date_str} 资讯日报**\n\n" + stock_md + "\n\n" + news_md + "\n\n" + douban_md

    # 5. 存档到 data/
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    os.makedirs(data_dir, exist_ok=True)

    archive = {
        "updated": datetime.now().isoformat(),
        "stocks": stocks,
        "news": news,
        "books": books
    }

    archive_path = os.path.join(data_dir, "latest.json")
    with open(archive_path, "w", encoding="utf-8") as f:
        json.dump(archive, f, ensure_ascii=False, indent=2)
    print(f"   已存档到 data/latest.json")

    # 6. 推送飞书
    print("\n📨 推送飞书...")
    send_markdown(full_md)

    print("\n✅ 完成！")


if __name__ == "__main__":
    main()