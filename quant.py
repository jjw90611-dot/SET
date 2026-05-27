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
# [CSS] 모바일 반응형 & 첨단 미래 비전 테마
# ==========================================
st.markdown("""
<style>
    .stApp { background-color: #070b14; color: #e2e8f0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    
    .main-title { 
        font-size: 38px; font-weight: 900; 
        background: -webkit-linear-gradient(45deg, #00f2fe, #4facfe);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-shadow: 0px 0px 15px rgba(0, 242, 254, 0.4);
        margin-bottom: 5px; letter-spacing: 1px;
    }
    .sub-title { color: #94a3b8; font-size: 16px; margin-bottom: 20px; font-weight: 500; }
    
    .briefing-box {
        background: rgba(15, 23, 42, 0.6); backdrop-filter: blur(10px);
        border-left: 4px solid #00f2fe; border-radius: 12px; padding: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5); margin-bottom: 25px;
    }
    .briefing-title { color: #00f2fe; font-size: 18px; font-weight: 800; margin-bottom: 15px; }
    .news-title { color: #ffffff; font-weight: bold; font-size: 16px; text-decoration: none; transition: all 0.3s; display: block; line-height: 1.4; }
    .news-title:hover { color: #f43f5e; }
    .news-time { color: #64748b; font-size: 12px; display: block; margin-top: 4px; margin-bottom: 15px; }
    
    .market-card {
        background: linear-gradient(145deg, #111827, #1f2937);
        border: 1px solid #374151; border-radius: 12px; padding: 15px; 
        text-align: center; transition: all 0.3s ease-in-out; cursor: pointer; 
        text-decoration: none; display: block; box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        margin-bottom: 10px;
    }
    .market-title { color: #94a3b8; font-size: 14px; font-weight: 700; margin-bottom: 5px; }
    .market-price { color: #ffffff; font-size: 24px; font-weight: 900; margin: 0; }
    .market-up { color: #f43f5e; font-size: 14px; font-weight: bold; margin-top: 5px; } 
    .market-down { color: #00f2fe; font-size: 14px; font-weight: bold; margin-top: 5px; } 
    .market-flat { color: #94a3b8; font-size: 14px; font-weight: bold; margin-top: 5px; }
    
    .stock-card {
        background: rgba(15, 23, 42, 0.5); border: 1px solid #1e293b;
        border-radius: 12px; padding: 18px; margin-bottom: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .stock-header {
        display: flex; justify-content: space-between; align-items: center;
        border-bottom: 1px solid #334155; padding-bottom: 12px; margin-bottom: 12px;
    }
    .stock-name { color: #ffffff; font-size: 20px; font-weight: 900; text-decoration: none; }
    .stock-price { color: #00f2fe; font-size: 20px; font-weight: 900; }
    .stock-info-row { display: flex; justify-content: space-between; font-size: 14px; margin-bottom: 6px; }
    .info-label { color: #94a3b8; }
    .info-val { color: #e2e8f0; font-weight: bold; }
    .highlight-val { color: #f43f5e; font-weight: 900; }
    .stock-trend-box {
        background: rgba(0,0,0,0.3); border-radius: 8px; padding: 12px; margin-top: 12px;
    }
    .trend-text { font-size: 13px; color: #cbd5e1; margin-bottom: 4px; }
    .trend-val { color: #f43f5e; font-weight: bold; font-size: 14px; }
    
    .disclosure-box {
        background: rgba(15, 23, 42, 0.5); border: 1px solid #1e293b;
        border-radius: 12px; padding: 15px; max-height: 350px; overflow-y: auto;
        box-shadow: inset 0 2px 10px rgba(0,0,0,0.5); margin-bottom: 20px;
    }
    .disclosure-item { border-bottom: 1px solid #334155; padding: 12px 0; }
    .disclosure-item:last-child { border-bottom: none; }
    .disclosure-time { color: #00f2fe; font-size: 12px; font-weight: bold; margin-bottom: 4px; }
    .disclosure-title { color: #e2e8f0; font-size: 14px; text-decoration: none; display: block; line-height: 1.4; }
    .disclosure-title:hover { color: #f43f5e; }

    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: #0f172a; border-radius: 4px; }
    ::-webkit-scrollbar-thumb { background: #334155; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #475569; }

    div.stButton > button {
        background-color: #1e293b; color: #00f2fe; border: 1px solid #00f2fe; 
        border-radius: 8px; font-weight: bold; width: 100%; height: 45px;
    }
    .disclaimer { text-align: center; color: #64748b; font-size: 13px; margin-top: 40px; padding-top: 20px; border-top: 1px solid #1e293b; line-height: 1.6; }

    @media (max-width: 768px) {
        .main-title { font-size: 26px; }
        .sub-title { font-size: 13px; }
        .market-price { font-size: 20px; }
        .stock-name, .stock-price { font-size: 18px; }
        .briefing-title { font-size: 16px; }
        .news-title { font-size: 14px; }
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# [헤더] 타이틀 & 새로고침 버튼 & 실시간 시계
# ==========================================
st.markdown("<div class='main-title'>조선생의 SET 대시보드</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>⚡ 글로벌 실시간 증시 · 환율 · 유가 · AI 성장주 발굴</div>", unsafe_allow_html=True)

col_btn, col_clock = st.columns([1, 2])
with col_btn:
    if st.button("🔄 즉시 새로고침"):
        st.rerun()
with col_clock:
    clock_html = """
    <div id="clock" style="font-family: 'Consolas', monospace; font-size: 14px; color: #00f2fe; text-align: right; margin-top: 12px; font-weight: bold;"></div>
    <script>
    function updateTime() {
        const now = new Date();
        const timeString = now.getFullYear() + "." + String(now.getMonth() + 1).padStart(2, '0') + "." + String(now.getDate()).padStart(2, '0') + " " + 
                           String(now.getHours()).padStart(2, '0') + ":" + String(now.getMinutes()).padStart(2, '0') + ":" + String(now.getSeconds()).padStart(2, '0');
        document.getElementById('clock').innerText = "LIVE 🔴 " + timeString;
    }
    setInterval(updateTime, 1000); updateTime();
    </script>
    """
    components.html(clock_html, height=40)

# ==========================================
# [섹션 1] 실시간 시장 핵심 브리핑
# ==========================================
def get_dynamic_briefing():
    try:
        urls = [
            "https://news.google.com/rss/headlines/section/topic/WORLD?hl=ko&gl=KR&ceid=KR:ko",
            "https://news.google.com/rss/headlines/section/topic/BUSINESS?hl=ko&gl=KR&ceid=KR:ko"
        ]
        news_items = []
        for url in urls:
            res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
            res.encoding = 'utf-8'
            root = ET.fromstring(res.text)
            for item in root.findall('.//item')[:10]:
                title = item.find('title').text
                link = item.find('link').text
                pub_date_str = item.find('pubDate').text
                try: dt = parsedate_to_datetime(pub_date_str)
                except: dt = datetime.datetime.now()
                news_items.append({'title': title, 'link': link, 'dt': dt})
        
        news_items.sort(key=lambda x: x['dt'], reverse=True)
        briefing_html = ""
        for count, item in enumerate(news_items[:4]):
            formatted_date = item['dt'].strftime("%Y-%m-%d %H:%M")
            briefing_html += f"<a href='{item['link']}' target='_blank' class='news-title'>[{count+1}] {item['title']}</a>"
            briefing_html += f"<span class='news-time'>🕒 {formatted_date}</span>"
        return briefing_html if briefing_html else "뉴스를 불러올 수 없습니다."
    except:
        return "업데이트 중 오류가 발생했습니다."

st.markdown(f"""
<div class="briefing-box">
    <div class="briefing-title">🚨 실시간 글로벌 경제 속보</div>
    <div>{get_dynamic_briefing()}</div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# [섹션 1.5] CNN 공포·탐욕 지수
# ==========================================
def get_fear_and_greed():
    try:
        url = "https://production.dataviz.cnn.io/index/fearandgreed/graphdata"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Accept': 'application/json'
        }
        res = requests.get(url, headers=headers, timeout=5)
        data = res.json()
        score = int(data['fear_and_greed']['score'])
        
        if score < 25: state, color = "극단적 공포 (Extreme Fear)", "#ef4444"
        elif score < 45: state, color = "공포 (Fear)", "#f97316"
        elif score <= 55: state, color = "중립 (Neutral)", "#eab308"
        elif score <= 75: state, color = "탐욕 (Greed)", "#22c55e"
        else: state, color = "극단적 탐욕 (Extreme Greed)", "#14b8a6"
        return score, state, color
    except:
        return 50, "데이터 확인 불가", "#94a3b8"

fg_score, fg_state, fg_color = get_fear_and_greed()

st.markdown(f"""
<a href="https://edition.cnn.com/markets/fear-and-greed" target="_blank" style="text-decoration: none; display: block;">
    <div style="background: rgba(15, 23, 42, 0.6); border: 1px solid #374151; border-radius: 12px; padding: 20px; margin-bottom: 25px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.2); transition: transform 0.2s;">
        <div style="color: #94a3b8; font-size: 15px; font-weight: bold; margin-bottom: 5px;">CNN 공포·탐욕 지수 (클릭 시 상세이동)</div>
        <div style="font-size: 38px; font-weight: 900; color: {fg_color}; margin-bottom: -5px;">{fg_score}</div>
        <div style="font-size: 16px; font-weight: bold; color: {fg_color}; margin-bottom: 15px;">{fg_state}</div>
        <div style="width: 100%; background-color: #1e293b; border-radius: 10px; height: 14px; overflow: hidden; border: 1px solid #334155;">
            <div style="width: {fg_score}%; background-color: {fg_color}; height: 100%; border-radius: 10px; transition: width 1s ease-in-out;"></div>
        </div>
        <div style="display: flex; justify-content: space-between; margin-top: 8px; font-size: 12px; color: #64748b; font-weight: bold;">
            <span>0 (극단적 공포)</span>
            <span>50 (중립)</span>
            <span>100 (극단적 탐욕)</span>
        </div>
    </div>
</a>
""", unsafe_allow_html=True)

# ==========================================
# [섹션 2] 글로벌 증시 & 지표 (코스피/코스닥 네이버 실시간 연동)
# ==========================================
def get_naver_realtime_index(code):
    """네이버 금융 모바일 API를 통한 코스피/코스닥 1초 단위 실시간 데이터"""
    try:
        url = f"https://m.stock.naver.com/api/index/{code}/basic"
        res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
        data = res.json()
        
        curr_str = data.get('closePrice', '0.00')
        diff_raw = data.get('compareToPreviousClosePrice', '0').replace(',', '')
        pct_raw = data.get('fluctuationsRatio', '0').replace('%', '')
        compare = data.get('compare', '3')
        
        diff = float(diff_raw)
        pct = float(pct_raw)
        
        if compare in ['1', '2']: # 상승
            diff_str = f"▲ {diff:,.2f}"
            pct_str = f"+{pct:.2f}%"
            color = "market-up"
        elif compare in ['4', '5']: # 하락
            diff_str = f"▼ {diff:,.2f}"
            pct_str = f"-{pct:.2f}%"
            color = "market-down"
        else: # 보합
            diff_str = "0.00"
            pct_str = "0.00%"
            color = "market-flat"
            
        return curr_str, diff_str, pct_str, color
    except:
        return "0.00", "0.00", "0.00%", "market-flat"

def get_yahoo_realtime(ticker):
    """야후 파이낸스를 통한 해외 지수 실시간 데이터"""
    try:
        url = f"https://query2.finance.yahoo.com/v8/finance/chart/{ticker}?interval=1m&range=1d&_={int(time.time() * 1000)}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers, timeout=5)
        data = res.json()
        meta = data['chart']['result'][0]['meta']
        curr = meta.get('regularMarketPrice', 0)
        prev = meta.get('chartPreviousClose', 0)
        diff = curr - prev
        pct = (diff / prev) * 100 if prev != 0 else 0
        diff_str = f"▲ {diff:,.2f}" if diff > 0 else f"▼ {abs(diff):,.2f}" if diff < 0 else "0.00"
        curr_str = f"{curr:,.2f}"
        pct_str = f"+{pct:.2f}%" if pct > 0 else f"{pct:.2f}%"
        color = "market-up" if diff > 0 else "market-down" if diff < 0 else "market-flat"
        return curr_str, diff_str, pct_str, color
    except:
        return "0.00", "0.00", "0.00%", "market-flat"

def make_card(title, price, diff, pct, color, link):
    return f"""
    <a href="{link}" target="_blank" class="market-card">
        <div class="market-title">{title}</div>
        <div class="market-price">{price}</div>
        <div class="{color}">{diff} ({pct})</div>
    </a>
    """

# 국내 증시는 네이버 API 사용
kp_p, kp_d, kp_pct, kp_c = get_naver_realtime_index("KOSPI")
kq_p, kq_d, kq_pct, kq_c = get_naver_realtime_index("KOSDAQ")

# 해외 증시 및 지표는 야후 파이낸스 사용
sp_p, sp_d, sp_pct, sp_c = get_yahoo_realtime("^GSPC")
nd_p, nd_d, nd_pct, nd_c = get_yahoo_realtime("^IXIC")
usd_p, usd_d, usd_pct, usd_c = get_yahoo_realtime("KRW=X")
wti_p, wti_d, wti_pct, wti_c = get_yahoo_realtime("CL=F")
gold_p, gold_d, gold_pct, gold_c = get_yahoo_realtime("GC=F")
btc_p, btc_d, btc_pct, btc_c = get_yahoo_realtime("BTC-USD")

c1, c2 = st.columns(2)
with c1: st.markdown(make_card("KOSPI", kp_p, kp_d, kp_pct, kp_c, "https://finance.naver.com/sise/sise_index.naver?code=KOSPI"), unsafe_allow_html=True)
with c2: st.markdown(make_card("KOSDAQ", kq_p, kq_d, kq_pct, kq_c, "https://finance.naver.com/sise/sise_index.naver?code=KOSDAQ"), unsafe_allow_html=True)

c3, c4 = st.columns(2)
with c3: st.markdown(make_card("S&P 500", sp_p, sp_d, sp_pct, sp_c, "https://finance.yahoo.com/quote/%5EGSPC"), unsafe_allow_html=True)
with c4: st.markdown(make_card("NASDAQ", nd_p, nd_d, nd_pct, nd_c, "https://finance.yahoo.com/quote/%5EIXIC"), unsafe_allow_html=True)

c5, c6 = st.columns(2)
with c5: st.markdown(make_card("환율 (USD/KRW)", usd_p, usd_d, usd_pct, usd_c, "https://finance.yahoo.com/quote/KRW=X"), unsafe_allow_html=True)
with c6: st.markdown(make_card("유가 (WTI)", wti_p, wti_d, wti_pct, wti_c, "https://finance.yahoo.com/quote/CL=F"), unsafe_allow_html=True)

c7, c8 = st.columns(2)
with c7: st.markdown(make_card("금 (Gold)", gold_p, gold_d, gold_pct, gold_c, "https://finance.yahoo.com/quote/GC=F"), unsafe_allow_html=True)
with c8: st.markdown(make_card("비트코인 (BTC)", btc_p, btc_d, btc_pct, btc_c, "https://finance.yahoo.com/quote/BTC-USD"), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# [섹션 3] AI 기반 중소형 성장주
# ==========================================
st.markdown("<h4 style='color: #00f2fe; margin-bottom: 5px; font-weight: 800;'>💎 오늘의 저평가 중소형 성장주</h4>", unsafe_allow_html=True)
st.markdown("<p style='color: #94a3b8; font-size: 13px; margin-bottom: 15px;'>※ 3년 연속 영업이익 증가 & PBR 2.0 이하</p>", unsafe_allow_html=True)

@st.cache_data(ttl=86400)
def get_target_stock_codes():
    today = datetime.date.today()
    random.seed(today.toordinal())
    candidates = []
    for page in range(2, 6):
        try:
            url = f"https://finance.naver.com/sise/sise_market_sum.naver?sosok=0&page={page}"
            res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
            res.encoding = 'euc-kr'
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
        if len(results) >= 3: break
        try:
            url = f"https://finance.naver.com/item/main.naver?code={code}"
            res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
            res.encoding = 'euc-kr'
            soup = BeautifulSoup(res.text, 'html.parser')
            
            price_tag = soup.select_one('.no_today .blind')
            curr_price = price_tag.text.strip() + "원" if price_tag else "확인불가"
            
            pbr_tag = soup.find('em', id='_pbr')
            if not pbr_tag: continue
            pbr = float(pbr_tag.text.strip())
            if pbr > 2.0: continue 
            
            table = soup.find('table', class_='tb_type1 tb_num tb_type1_ifrs')
            if not table: continue
            rows = table.find('tbody').find_all('tr')
            
            op_cols = rows[1].find_all('td')[:3]
            ops = [int(c.text.strip().replace(',', '')) for c in op_cols if c.text.strip() and c.text.strip() != '-']
            rev_cols = rows[0].find_all('td')[:3]
            revs = [int(c.text.strip().replace(',', '')) for c in rev_cols if c.text.strip() and c.text.strip() != '-']
            
            if len(ops) == 3 and len(revs) == 3:
                if ops[0] > 0 and ops[0] < ops[1] < ops[2]:
                    roe = rows[5].find_all('td')[2].text.strip() + "%"
                    debt = rows[6].find_all('td')[2].text.strip() + "%"
                    reserve = rows[8].find_all('td')[2].text.strip() + "%"
                    rev_str = f"{revs[0]:,} ➔ {revs[1]:,} ➔ {revs[2]:,}억"
                    op_str = f"{ops[0]:,} ➔ {ops[1]:,} ➔ {ops[2]:,}억"
                    
                    results.append({
                        "name": name, "code": code, "price": curr_price, "pbr": str(pbr),
                        "roe": roe, "debt": debt, "reserve": reserve,
                        "rev": rev_str, "op": op_str
                    })
        except: continue
    return results

with st.spinner("AI가 오늘의 성장 기업을 발굴하고 있습니다..."):
    final_stock_data = get_target_stock_codes()

if not final_stock_data:
    st.markdown("<div class='stock-card' style='text-align:center; color:#94a3b8;'>조건에 맞는 종목을 검색 중입니다. 잠시 후 새로고침 해주세요.</div>", unsafe_allow_html=True)
else:
    for s in final_stock_data:
        link = f"https://finance.naver.com/item/main.naver?code={s['code']}"
        pbr_styled = f"<span class='highlight-val'>{s['pbr']}</span>" if s['pbr'] != "-" and float(s['pbr']) < 1.0 else s['pbr']
        
        card_html = f"""
        <div class="stock-card">
            <div class="stock-header">
                <a href="{link}" target="_blank" class="stock-name">{s['name']}</a>
                <span class="stock-price">{s['price']}</span>
            </div>
            <div class="stock-info-row">
                <span class="info-label">PBR</span> <span class="info-val">{pbr_styled}</span>
            </div>
            <div class="stock-info-row">
                <span class="info-label">ROE</span> <span class="info-val">{s['roe']}</span>
            </div>
            <div class="stock-info-row">
                <span class="info-label">부채비율 / 유보율</span> <span class="info-val">{s['debt']} / {s['reserve']}</span>
            </div>
            <div class="stock-trend-box">
                <div class="trend-text">📈 최근 3년 매출액 추이</div>
                <div class="trend-val" style="color: #94a3b8; margin-bottom: 8px;">{s['rev']}</div>
                <div class="trend-text">🔥 최근 3년 영업이익 추이</div>
                <div class="trend-val">{s['op']}</div>
            </div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# [섹션 4] 저점 주식 공략 (비밀 조건 적용, 최대 10개)
# ==========================================
st.markdown("<h4 style='color: #f43f5e; margin-bottom: 15px; font-weight: 800;'>🎯 오늘의 바닥 탈출 (저점 공략주)</h4>", unsafe_allow_html=True)

@st.cache_data(ttl=3600)
def get_bottom_fishing_stocks():
    candidates = []
    for page in range(1, 6):
        try:
            url = f"https://finance.naver.com/sise/sise_market_sum.naver?sosok=0&page={page}"
            res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
            res.encoding = 'euc-kr'
            soup = BeautifulSoup(res.text, 'html.parser')
            links = soup.select('a.tltle')
            for link in links:
                candidates.append((link.text.strip(), link['href'].split('code=')[1]))
        except: pass
    
    random.shuffle(candidates)
    results = []
    
    for name, code in candidates:
        if len(results) >= 10: break
        try:
            url = f"https://query2.finance.yahoo.com/v8/finance/chart/{code}.KS?interval=1d&range=1y"
            res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=3)
            data = res.json()
            closes = data['chart']['result'][0]['indicators']['quote'][0]['close']
            closes = [c for c in closes if c is not None]
            
            if len(closes) < 20: continue
            
            curr_price = closes[-1]
            high_52w = max(closes)
            low_52w = min(closes)
            mid_52w = (high_52w + low_52w) / 2
            
            ma5 = sum(closes[-5:]) / 5
            ma20 = sum(closes[-20:]) / 20
            
            if curr_price <= mid_52w and ma5 >= ma20:
                results.append({
                    "name": name, "code": code,
                    "price": f"{int(curr_price):,}원",
                    "high": f"{int(high_52w):,}", "low": f"{int(low_52w):,}",
                    "ma5": f"{int(ma5):,}", "ma20": f"{int(ma20):,}"
                })
        except: continue
    return results

with st.spinner("AI가 바닥을 다지고 상승하는 종목을 찾고 있습니다..."):
    bottom_stocks = get_bottom_fishing_stocks()

if not bottom_stocks:
    st.markdown("<div class='stock-card' style='text-align:center; color:#94a3b8;'>현재 조건에 완벽히 부합하는 종목이 없습니다.</div>", unsafe_allow_html=True)
else:
    for s in bottom_stocks:
        link = f"https://finance.naver.com/item/main.naver?code={s['code']}"
        card_html = f"""
        <div class="stock-card" style="border-left: 4px solid #f43f5e;">
            <div class="stock-header">
                <a href="{link}" target="_blank" class="stock-name">{s['name']}</a>
                <span class="stock-price" style="color: #f43f5e;">{s['price']}</span>
            </div>
            <div class="stock-info-row">
                <span class="info-label">52주 최고 / 최저</span> 
                <span class="info-val">{s['high']} / {s['low']}</span>
            </div>
            <div class="stock-info-row">
                <span class="info-label">5일선 / 20일선</span> 
                <span class="info-val" style="color: #22c55e;">{s['ma5']} / {s['ma20']}</span>
            </div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# [섹션 5] 실시간 기업 공시 전광판 (DART 연동)
# ==========================================
st.markdown("<h4 style='color: #00f2fe; margin-bottom: 5px; font-weight: 800;'>📢 실시간 기업 공시 (DART)</h4>", unsafe_allow_html=True)
st.markdown("<p style='color: #94a3b8; font-size: 13px; margin-bottom: 15px;'>※ 금융감독원 전자공시시스템 실시간 연동</p>", unsafe_allow_html=True)

def get_dart_disclosures():
    try:
        url = "https://dart.fss.or.kr/api/todayRSS.xml"
        res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
        res.encoding = 'utf-8'
        root = ET.fromstring(res.text)
        
        html = "<div class='disclosure-box'>"
        items = root.findall('.//item')
        
        if not items:
            return "<div class='disclosure-box' style='text-align:center; color:#94a3b8; padding: 20px;'>현재 업데이트된 공시가 없습니다.</div>"
            
        for item in items[:30]:
            title_elem = item.find('title')
            link_elem = item.find('link')
            author_elem = item.find('author')
            pub_date_elem = item.find('pubDate')
            
            title = title_elem.text if title_elem is not None else "제목 없음"
            link = link_elem.text if link_elem is not None else "#"
            author = author_elem.text if author_elem is not None else ""
            pub_date_str = pub_date_elem.text if pub_date_elem is not None else ""
            
            try: 
                dt = parsedate_to_datetime(pub_date_str)
                date_str = dt.strftime("%H:%M")
            except: 
                date_str = "방금 전"
                
            display_title = f"[{author}] {title}" if author else title
            
            html += f"""
            <div class="disclosure-item">
                <div class="disclosure-time">🔔 {date_str}</div>
                <a href="{link}" target="_blank" class="disclosure-title">{display_title}</a>
            </div>
            """
        html += "</div>"
        return html
    except Exception as e:
        return "<div class='disclosure-box' style='text-align:center; color:#94a3b8; padding: 20px;'>공시 데이터를 불러올 수 없습니다. (DART 서버 응답 지연)</div>"

st.markdown(get_dart_disclosures(), unsafe_allow_html=True)

# ==========================================
# [푸터] 투자 면책 조항
# ==========================================
st.markdown("""
<div class="disclaimer">
    ⚠️ <b>본 대시보드의 정보는 참고용이며, 매수·매도 추천이 아닙니다.</b><br>
    투자에 대한 모든 결정과 책임은 전적으로 투자자 본인에게 있습니다.
</div>
""", unsafe_allow_html=True)
