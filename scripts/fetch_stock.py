#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""股市行情抓取（东方财富）"""

import json
import requests
from config import STOCK_WATCHLIST


def fetch_stock_price(code: str, market: str = "sh") -> dict:
    """
    从东方财富获取股票实时价格
    market: sh=上证, sz=深证, gb_=美股
    """
    # A股：secid格式 1=上证，0=深证
    if market in ("sh", "sz"):
        secid = f"1{code}" if market == "sh" else f"0{code}"
    else:
        secid = code

    url = "https://push2.eastmoney.com/api/qt/stock/get"
    params = {
        "secid": secid,
        "fields": "f43,f170,f171,f169,f116,f117,f162,f163,f164,f165,f166,f167"
    }

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://finance.eastmoney.com/"
    }

    try:
        resp = requests.get(url, params=params, headers=headers, timeout=10)
        data = resp.json()["data"]
        return {
            "code": code,
            "name": data.get("f58", code),
            "price": data.get("f43", 0) / 100,  # 分转元
            "change": data.get("f169", 0) / 100,
            "change_pct": data.get("f170", 0) / 100,
            "volume": data.get("f168", 0),  # 成交量
            "high": data.get("f164", 0) / 100,
            "low": data.get("f165", 0) / 100,
        }
    except Exception as e:
        return {"code": code, "name": code, "error": str(e)}


def fetch_all_stocks() -> list:
    """获取所有自选股行情"""
    results = []

    for market, stocks in STOCK_WATCHLIST.items():
        for stock in stocks:
            # A股用上证或深证
            mkt = "sh" if market == "A股" else "sz"
            item = fetch_stock_price(stock["code"], mkt)
            item["market"] = market
            results.append(item)

    return results


def format_stock_md(stocks: list) -> str:
    """格式化成 Markdown 消息"""
    lines = ["📊 **今日自选股行情**\n"]

    current_market = None
    for s in stocks:
        market = s.get("market", "")
        if market != current_market:
            if current_market is not None:
                lines.append("")
            lines.append(f"**{market}**")
            current_market = market

        if "error" in s:
            lines.append(f"- {s['name']}：获取失败")
            continue

        price = s["price"]
        change = s["change"]
        change_pct = s["change_pct"]
        sign = "+" if change >= 0 else ""
        emoji = "🟢" if change >= 0 else "🔴"

        lines.append(
            f"{emoji} {s['name']}({s['code']}) "
            f"{price:.2f} {sign}{change:+.2f}({sign}{change_pct:+.2f}%)"
        )

    return "\n".join(lines)


if __name__ == "__main__":
    stocks = fetch_all_stocks()
    print(json.dumps(stocks, ensure_ascii=False, indent=2))
    print("\n--- Markdown ---\n")
    print(format_stock_md(stocks))