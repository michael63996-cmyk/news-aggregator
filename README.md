# 资讯聚合器

每天自动抓取股市行情、汽车行业技术新闻、豆瓣书籍推荐，推送到飞书。

## 📦 目录结构

```
├── .github/
│   └── workflows/
│       └── daily-fetch.yml      # GitHub Actions 定时任务
├── scripts/
│   ├── fetch_stock.py          # 股市行情
│   ├── fetch_auto_news.py      # 汽车新闻 RSS
│   ├── fetch_douban.py         # 豆瓣读书
│   └── send_feishu.py          # 飞书推送
├── data/                       # 数据存档
│   ├── stock.json
│   ├── auto_news.json
│   └── douban.json
├── web/                        # GitHub Pages 可视化
│   ├── index.html
│   ├── style.css
│   └── script.js
├── requirements.txt
└── README.md
```

## 🔧 配置步骤

### 1. Fork 此仓库

### 2. 配置飞书 Webhook
在 GitHub 仓库 Settings → Secrets 添加：
- `FEISHU_WEBHOOK`：飞书群机器人 Webhook 地址

获取方式：飞书群 → 群设置 → 群机器人 → 添加机器人 → 复制 Webhook

### 3. 配置自选股
编辑 `scripts/config.py` 中的 `STOCK_WATCHLIST`，填入股票代码：
- A股：如 `601138`（工业富联）
- 美股：如 `AAPL`

### 4. 开启 GitHub Pages
仓库 Settings → Pages → Source: main /docs → Save

### 5. 修改仓库名为你的用户名
Settings → Repository name → 改成 `{your-username}.github.io` 可直接用域名访问

## ⏰ 运行机制

| 触发时间 | 内容 |
|--------|------|
| 每天 07:30 (北京时间) | GitHub Actions 自动抓取并推送飞书 |
| 随时 | 访问 GitHub Pages 查看历史数据 |

## 📡 数据源

- **股市**：东方财富 API
- **汽车新闻**：36氪汽车、虎嗅汽车、Automotive News RSS
- **豆瓣读书**：豆瓣RSS（公开内容）