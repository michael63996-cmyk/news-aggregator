// 资讯日报 - 前端脚本
(async function() {
  const content = document.getElementById('content');
  const updateTime = document.getElementById('update-time');

  // 尝试从多个位置加载数据
  let data = null;
  const sources = [
    '../data/latest.json',
    'data/latest.json',
    '../data/latest.json?' + Date.now()
  ];

  for (const src of sources) {
    try {
      const resp = await fetch(src);
      if (resp.ok) {
        data = await resp.json();
        break;
      }
    } catch(e) {}
  }

  // GitHub Actions 环境：从存档JSON构建的数据读取
  if (!data) {
    try {
      const resp = await fetch('https://raw.githubusercontent.com/' + 
        window.location.pathname.split('/')[1] + '/' + 
        window.location.pathname.split('/')[2] + '/main/data/latest.json');
      if (resp.ok) data = await resp.json();
    } catch(e) {}
  }

  if (!data) {
    content.innerHTML = '<p class="error">⚠️ 无法加载数据，请稍后刷新</p>';
    return;
  }

  // 更新时间
  if (data.updated) {
    const d = new Date(data.updated);
    updateTime.textContent = '最后更新：' + d.toLocaleString('zh-CN', {timeZone: 'Asia/Shanghai'});
  }

  // 渲染
  let html = '';
  const params = new URLSearchParams(window.location.search);
  const tab = params.get('tab') || 'all';

  function renderStock() {
    if (!data.stocks) return '';
    let s = '<div class="card-section"><div class="card-section-title">📊 自选股行情</div>';
    for (const stock of data.stocks) {
      if (stock.error) continue;
      const cls = stock.change >= 0 ? 'up' : 'down';
      const sign = stock.change >= 0 ? '+' : '';
      s += `<div class="stock-item">
        <div><div class="stock-name">${stock.name}</div><div class="stock-code">${stock.code}</div></div>
        <div><span class="stock-price ${cls}">${stock.price.toFixed(2)}</span>
        <span class="${cls}">${sign}${stock.change.toFixed(2)}(${sign}${stock.change_pct.toFixed(2)}%)</span></div>
      </div>`;
    }
    return s + '</div>';
  }

  function renderNews() {
    if (!data.news) return '';
    let s = '<div class="card-section"><div class="card-section-title">🚗 汽车技术新闻</div>';
    for (const [source, items] of Object.entries(data.news)) {
      for (const item of (items || []).slice(0, 3)) {
        if (item.error) continue;
        s += `<div class="news-item">
          <a href="${item.link}" target="_blank">${item.title}</a>
          <div class="news-source">${source}</div>
        </div>`;
      }
    }
    return s + '</div>';
  }

  function renderBooks() {
    if (!data.books) return '';
    let s = '<div class="card-section"><div class="card-section-title">📚 豆瓣读书推荐</div>';
    for (const book of (data.books || []).slice(0, 5)) {
      if (book.error) continue;
      s += `<div class="news-item">
        <a href="${book.link}" target="_blank">${book.title}</a>
      </div>`;
    }
    return s + '</div>';
  }

  if (tab === 'all' || tab === 'stock') html += renderStock();
  if (tab === 'all' || tab === 'auto') html += renderNews();
  if (tab === 'all' || tab === 'book') html += renderBooks();

  content.innerHTML = '<div class="card">' + html + '</div>';

  // Tab 切换
  document.querySelectorAll('.tab').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.tab').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const t = btn.dataset.tab;
      window.location.search = '?tab=' + t;
    });
  });
})();