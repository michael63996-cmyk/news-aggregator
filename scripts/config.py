# 自选股列表（A股，美股）
STOCK_WATCHLIST = {
    "A股": [
        {"code": "601138", "name": "工业富联"},
        {"code": "601727", "name": "上海电气"},
        {"code": "603228", "name": "景旺电子"},
    ],
    "美股": [],
}

# 汽车新闻 RSS 源
AUTO_NEWS_RSS = [
    {"name": "36氪汽车", "url": "https://36kr.com/feed/column/auto"},
    {"name": "虎嗅汽车", "url": "https://www.huxiu.com/channel/103.html"},
    {"name": "Automotive News", "url": "https://www.autonews.com/rss.xml"},
]

# 豆瓣读书 RSS
DOUBAN_BOOK_RSS = "https://www.douban.com/feed/recommend/book"

# 飞书 Webhook（建议放在 GitHub Secrets，此处仅作本地测试）
FEISHU_WEBHOOK = "https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxx"

# 推送时间（UTC，+8小时即北京时间）
CRON_SCHEDULE = "23 23 * * *"  # 北京时间每天 07:30