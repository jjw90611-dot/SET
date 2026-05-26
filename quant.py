import streamlit as st
import streamlit.components.v1 as components
import requests
from bs4 import BeautifulSoup
import datetime
import time
import random
import ssl
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime

# 보안(SSL) 차단 무시
if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context

# 화면 넓게 쓰기 & 기본 테마 설정
st.set_page_config(page_title="조선생의 SET", layout="wide")

# ==========================================
# [자동 업데이트 엔진] 5분(300,000ms)마다 페이지 자동 새로고침
# ==========================================
components.html(
    """
    <script>
    setTimeout(function() {
        window.parent.location.reload();
    }, 300000);
    </script>
    """,
    height=0
)

# ==========================================
# [CSS] 첨단 미래 비전 (High-Tech / Cyber) 테마
# ==========================================
st.markdown("""
<style>
    .stApp { background-color: #070b14; color: #e2e8f0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    
    .main-title { 
        font-size: 42px; font-weight: 900; 
        background: -webkit-linear-gradient(45deg, #00f2fe, #4facfe);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-shadow: 0px 0px 15px rgba(0, 242, 254, 0.4);
        margin-bottom: 5px; letter-spacing: 2px;
    }
    .sub-title { color: #94a3b8; font-size: 18px; margin-bottom: 30px; font-weight: 500; }
    
    .briefing-box {
        background: rgba(15, 23, 42, 0.6); backdrop-filter: blur(10px);
        border-left: 4px solid #00f2fe; border-radius: 12px; padding: 25px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5); margin-bottom: 30px;
    }
    .briefing-title { color: #00f2fe; font-size: 22px; font-weight: 800; margin-bottom: 15px; display: flex; justify-content: space-between; align-items: center;}
    .news-title { color: #ffffff; font-weight: bold; font-size: 18px; text-decoration: none; transition: all 0.3s; }
    .news-title:hover { color: #f43f5e; text-shadow: 0px 0px 8px rgba(244, 63, 94, 0.6); }
    
    .market-card {
        background: linear-gradient(145deg, #111827, #1f2937);
        border: 1px solid #374151; border-radius: 12px; padding: 20px 15px; 
        text-align: center; transition: all 0.3s ease-in-out; cursor: pointer; 
        text-decoration: none; display: block; box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .market-card:hover { transform: translateY(-5px); border-color: #00f2fe; box-shadow: 0 0 20px rgba(0, 242, 254, 0.3); }
    .market-title { color: #94a3b8; font-size: 16px; font-weight: 700; margin-bottom: 10px; letter-spacing: 1px; }
    .market-price { color: #ffffff; font-size: 28px; font-weight: 900; margin: 0; text-shadow: 0px 0px 10px rgba(255,255,255,0.2); }
    .market-up { color: #f43f5e; font-size: 16px; font-weight: bold; margin-top: 8px; } 
    .market-down { color: #00f2fe; font-size: 16px; font-weight: bold; margin-top: 8px; } 
    .market-flat { color: #94a3b8; font-size: 16px; font-weight: bold; margin-top: 8px; }
    
    .cyber-table { width: 100%; border-collapse: collapse; text-align: center; color: #e2e8f0; font-size: 16px; margin-top: 10px; background: rgba(15, 23, 42, 0.4); border-radius: 10px; overflow: hidden; }
    .cyber-table th { background-color: #1e293b; padding: 15px; border-bottom: 2px solid #00f2fe; color: #00f2fe; font-weight: 800; letter-spacing: 1px; }
    .cyber-table td { padding: 15px; border-bottom: 1px solid #334155; }
    .cyber-table tr:hover { background-color: rgba(30, 41, 59, 0.8); }
    .stock-link { color: #ffffff; text-decoration: none; font-weight: 900; font-size: 18px; transition: 0.2s; }
    .stock-link:hover { color: #00f2fe; text-shadow: 0px 0px 10px rgba(0, 242, 254, 0.5); }
    .highlight-val { color: #f43f5e; font-weight: 900; text-shadow: 0px 0px 8px rgba(244, 63, 94, 0.4); }
    
    /* 새로고침 버튼 CSS */
    div.stButton > button {
        background-color: #1e293b; color: #00f2fe; border: 1px solid #00f2fe; 
        border-radius: 8px; font-weight: bold; transition: all 0.3s; width: 100%; height: 45px;
    }
    div.stButton > button:hover {
        background-color: #00f2fe; color: #070b14; box-shadow: 0 0 15px rgba(0, 242, 254, 0.5);
    }
    
    /* 면책 조항 CSS */
    .disclaimer {
        text-align: center; color: #94a3b8; font-size: 15px; 
        margin-top: 60px; padding-top: 25px; border-top: 1px solid #1e293b;
        line-height: 1.8; font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# [헤더] 타이틀 & 새로고침 버튼 & 실시간 시계
# ==========================================
col_title, col_btn, col_clock = st.columns([5.5, 1.5, 3])
with col_title:
    st.markdown("<div class='main-title'>조선생의 Stock ETF Trader (SET)</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>⚡ 글로벌 실시간 증시 · 환율 · 유가 · 금 · 비트코인 · AI 기반 성장주 발굴 시스템</div>", unsafe_allow_html=True)
with col_btn:
    st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
    if st.button("🔄 즉시 새로고침"):
        st.rerun()
with col_clock:
    clock_html = """
    <div id="clock" style="font-family: 'Consolas', monospace; font-size: 18px; color: #00f2fe; text-align: right; margin-top: 20px; font-weight: bold; text-shadow: 0px 0px 8px rgba(0,242,254,0.5);"></div>
    <script>
    function updateTime() {
        const now = new Date();
        const days = ['일', '월', '화', '수', '목', '금', '토'];
        const dayName = days[now.getDay()];
        const timeString = now.getFullYear() + "." + String(now.getMonth() + 1).padStart(2, '0') + "." + String(now.getDate()).padStart(2, '0') + " (" + dayName + ") " + 
                           String(now.getHours()).padStart(2, '0') + ":" + String(now.getMinutes()).padStart(2, '0') + ":" + String(now.getSeconds()).padStart(2, '0');
        document.getElementById('clock').innerText = "LIVE 🔴 " + timeString;
    }
    setInterval(updateTime, 1000); updateTime();
    </script>
    """
    components.html(clock_html, height=50)

# ==========================================
# [섹션 1] 실시간 시장 핵심 브리핑 (국제/경제 듀얼 매크로 엔진)
# ==========================================
def get_dynamic_briefing():
    try:
        urls = [
            "https://news.google.com/rss/headlines/section/topic/WORLD?hl=ko&gl=KR&ceid=KR:ko",
            "https://news.google.com/rss/headlines/section/topic/BUSINESS?hl=ko&gl=KR&ceid=KR:ko"
        ]
        
        news_items = []
        for url in urls:
            res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            res.encoding = 'utf-8'
            root = ET.fromstring(res.text)
            
            for item in root.findall('.//item')[:10]:
                title = item.find('title').text
                link = item.find('link').text
                pub_date_str = item.find('pubDate').text
                
                try:
                    dt = parsedate_to_datetime(pub_date_str)
                except:
                    dt = datetime.datetime.now()
                    
                news_items.append({'title': title, 'link': link, 'dt': dt})
        
        news_items.sort(key=lambda x: x['dt'], reverse=True)
        
        briefing_html = ""
        for count, item in enumerate(news_items[:5]):
            formatted_date = item['dt'].strftime("%Y-%m-%d %H:%M")
            briefing_html += f"<a href='{item['link']}' target='_blank' class='news-title'>[{count+1}] {item['title']}</a><br>"
            briefing_html += f"<span style='color: #94a3b8; font-size: 14px; display: block; margin-top: 5px; margin-bottom: 22px;'>🕒 기사 송고 시간: {formatted_date}</span>"
                
        return briefing_html if briefing_html else "현재 실시간 주요 뉴스를 불러올 수 없습니다."
    except:
        return "실시간 브리핑 업데이트 중 오류가 발생했습니다."

st.markdown(f"""
<div class="briefing-box">
    <div class="briefing-title">
        <span>🚨 실시간 글로벌 경제·국제 긴급 속보 (클릭 시 원문 이동)</span>
    </div>
    <div>{get_dynamic_briefing()}</div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# [섹션 2] 글로벌 증시 & 환율 & 유가 & 금 & 비트코인 (다이렉트 API)
# ==========================================
def get_direct_realtime(ticker):
    try:
        url = f"https://query2.finance.yahoo.com/v8/finance/chart/{ticker}?interval=1m&range=1d&_={int(time.time() * 1000)}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache'
        }
        res = requests.get(url, headers=headers, timeout=5)
        data = res.json()
        
        meta = data['chart']['result'][0]['meta']
        curr = meta['regularMarketPrice']
        prev = meta['chartPreviousClose']
        
        diff = curr - prev
        pct = (diff / prev) * 100 if prev != 0 else 0
        
        diff_str = f"▲ {diff:,.2f}" if diff > 0 else f"▼ {abs(diff):,.2f}" if diff < 0 else "0.00"
        curr_str = f"{curr:,.2f}"
        pct_str = f"+{pct:.2f}%" if pct > 0 else f"{pct:.2f}%"
        color = "market-up" if diff > 0 else "market-down" if diff < 0 else "market-flat"
        
        return curr_str, diff_str, pct_str, color
    except Exception as e:
        return "0.00", "0.00", "0.00%", "market-flat"

def make_card(title, price, diff, pct, color, link):
    pct_html = f"({pct})" if pct else ""
    return f"""
    <a href="{link}" target="_blank" class="market-card">
        <div class="market-title">{title}</div>
        <div class="market-price">{price}</div>
        <div class="{color}">{diff} {pct_html}</div>
    </a>
    """

kp_p, kp_d, kp_pct, kp_c = get_direct_realtime("^KS11")
kq_p, kq_d, kq_pct, kq_c = get_direct_realtime("^KQ11")
sp_p, sp_d, sp_pct, sp_c = get_direct_realtime("^GSPC")
nd_p, nd_d, nd_pct, nd_c = get_direct_realtime("^IXIC")
usd_p, usd_d, usd_pct, usd_c = get_direct_realtime("KRW=X")
wti_p, wti_d, wti_pct, wti_c = get_direct_realtime("CL=F")
gold_p, gold_d, gold_pct, gold_c = get_direct_realtime("GC=F")
btc_p, btc_d, btc_pct, btc_c = get_direct_realtime("BTC-USD")

c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(make_card("KOSPI", kp_p, kp_d, kp_pct, kp_c, "https://finance.yahoo.com/quote/%5EKS11"), unsafe_allow_html=True)
with c2: st.markdown(make_card("KOSDAQ", kq_p, kq_d, kq_pct, kq_c, "https://finance.yahoo.com/quote/%5EKQ11"), unsafe_allow_html=True)
with c3: st.markdown(make_card("S&P 500", sp_p, sp_d, sp_pct, sp_c, "https://finance.yahoo.com/quote/%5EGSPC"), unsafe_allow_html=True)
with c4: st.markdown(make_card("NASDAQ", nd_p, nd_d, nd_pct, nd_c, "https://finance.yahoo.com/quote/%5EIXIC"), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

c5, c6, c7, c8 = st.columns(4)
with c5: st.markdown(make_card("USD/KRW (환율)", usd_p, usd_d, usd_pct, usd_c, "https://finance.yahoo.com/quote/KRW=X"), unsafe_allow_html=True)
with c6: st.markdown(make_card("WTI (유가)", wti_p, wti_d, wti_pct, wti_c, "https://finance.yahoo.com/quote/CL=F"), unsafe_allow_html=True)
with c7: st.markdown(make_card("Gold (금)", gold_p, gold_d, gold_pct, gold_c, "https://finance.yahoo.com/quote/GC=F"), unsafe_allow_html=True)
with c8: st.markdown(make_card("Bitcoin (비트코인)", btc_p, btc_d, btc_pct, btc_c, "https://finance.yahoo.com/quote/BTC-USD"), unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# ==========================================
# [섹션 3] AI 기반 중소형 성장주 자동 발굴 (다이렉트 가격 엔진)
# ==========================================
st.markdown("<h3 style='color: #00f2fe; margin-bottom: 5px; font-weight: 800;'>💎 오늘의 저평가 중소형 성장주 (3년 연속 영업이익 증가 & PBR 2.0 이하)</h3>", unsafe_allow_html=True)
st.markdown("<p style='color: #94a3b8; font-size: 14px; margin-bottom: 15px;'>※ 아래 종목의 현재가 및 링크는 5분 단위로 자동 업데이트됩니다.</p>", unsafe_allow_html=True)

@st.cache_data(ttl=86400)
def get_target_stock_codes():
    # 재무제표 분석(발굴)은 1일 1회만 수행
    today = datetime.date.today()
    random.seed(today.toordinal())
    
    candidates = []
    for page in range(2, 6):
        try:
            url = f"https://finance.naver.com/sise/sise_market_sum.naver?sosok=0&page={page}"
            res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(res.text, 'html.parser')
            links = soup.select('a.tltle')
            for link in links:
                code = link['href'].split('code=')[1]
                name = link.text.strip()
                candidates.append((name, code))
        except: pass
        
    random.shuffle(candidates)
    results = []
    
    for name, code in candidates:
        if len(results) >= 5: break
        try:
            url = f"https://finance.naver.com/item/main.naver?code={code}"
            res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(res.text, 'html.parser')
            
            pbr_tag = soup.find('em', id='_pbr')
            if not pbr_tag: continue
            pbr = float(pbr_tag.text.strip())
            if pbr > 2.0: continue 
            
            table = soup.find('table', class_='tb_type1 tb_num tb_type1_ifrs')
            if not table: continue
            rows = table.find('tbody').find_all('tr')
            
            op_cols = rows[1].find_all('td')[:3]
            ops = []
            for c in op_cols:
                txt = c.text.strip().replace(',', '')
                if txt and txt != '-': ops.append(int(txt))
                
            rev_cols = rows[0].find_all('td')[:3]
            revs = []
            for c in rev_cols:
                txt = c.text.strip().replace(',', '')
                if txt and txt != '-': revs.append(int(txt))
            
            if len(ops) == 3 and len(revs) == 3:
                if ops[0] > 0 and ops[0] < ops[1] < ops[2]:
                    roe = rows[5].find_all('td')[2].text.strip() + "%"
                    debt = rows[6].find_all('td')[2].text.strip() + "%"
                    reserve = rows[8].find_all('td')[2].text.strip() + "%"
                    
                    rev_str = f"{revs[0]:,} ➔ {revs[1]:,} ➔ {revs[2]:,}억"
                    op_str = f"{ops[0]:,} ➔ {ops[1]:,} ➔ {ops[2]:,}억"
                    
                    results.append({
                        "name": name, "code": code, "pbr": str(pbr),
                        "roe": roe, "debt": debt, "reserve": reserve,
                        "rev": rev_str, "op": op_str
                    })
        except: continue
        
    return results

# 다이렉트 API로 가격 가져오기
def get_realtime_prices_direct(stock_data):
    updated_data = []
    for s in stock_data:
        new_s = s.copy()
        try:
            ticker = f"{s['code']}.KS"
            url = f"https://query2.finance.yahoo.com/v8/finance/chart/{ticker}?interval=1m&range=1d&_={int(time.time() * 1000)}"
            headers = {'User-Agent': 'Mozilla/5.0', 'Cache-Control': 'no-cache'}
            res = requests.get(url, headers=headers, timeout=5)
            data = res.json()
            
            price = data['chart']['result'][0]['meta']['regularMarketPrice']
            new_s['price'] = f"{int(price):,}"
        except:
            new_s['price'] = "-"
        updated_data.append(new_s)
    return updated_data

with st.spinner("AI가 오늘의 3년 연속 성장 기업을 발굴하고 있습니다... (최초 1회 약 10초 소요)"):
    base_stock_data = get_target_stock_codes()
    final_stock_data = get_realtime_prices_direct(base_stock_data)

html_lines = [
    "<div style='overflow-x: auto;'>",
    "<table class='cyber-table'>",
    "<tr><th>종목명 (클릭)</th><th>현재가 (실시간)</th><th>PBR</th><th>ROE</th><th>유보율</th><th>부채비율</th><th>최근 3개년 매출액 추이</th><th>최근 3개년 영업이익 추이</th></tr>"
]

for s in final_stock_data:
    link = f"https://finance.yahoo.com/quote/{s['code']}.KS"
    pbr_styled = f"<span class='highlight-val'>{s['pbr']}</span>" if s['pbr'] != "-" and float(s['pbr']) < 1.0 else s['pbr']
    
    row_html = f"<tr><td><a href='{link}' target='_blank' class='stock-link'>{s['name']}</a></td>"
    row_html += f"<td style='font-weight: bold; color: #ffffff;'>{s['price']}원</td>"
    row_html += f"<td>{pbr_styled}</td><td>{s['roe']}</td><td>{s['reserve']}</td><td>{s['debt']}</td>"
    row_html += f"<td style='color: #94a3b8;'>{s['rev']}</td><td style='color: #f43f5e; font-weight: bold;'>{s['op']}</td></tr>"
    html_lines.append(row_html)

html_lines.append("</table></div>")

st.markdown("".join(html_lines), unsafe_allow_html=True)

# ==========================================
# [푸터] 투자 면책 조항 (Disclaimer)
# ==========================================
st.markdown("""
<div class="disclaimer">
    ⚠️ <b>본 대시보드에서 제공하는 모든 정보는 참고용일 뿐이며, 어떠한 경우에도 매수·매도 추천이나 투자 권유가 아닙니다.</b><br>
    <b>투자에 대한 모든 결정과 판단, 그리고 그에 따른 책임은 전적으로 투자자 본인에게 있습니다.</b>
</div>
""", unsafe_allow_html=True)
