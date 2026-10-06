import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime

# ==========================================
# 0. 系統層級設定 (強制全螢幕無留白，並保留側邊欄展開按鈕)
# ==========================================
st.set_page_config(page_title="JARVIS 頂級操盤工作站", page_icon="⚡", layout="wide", initial_sidebar_state="expanded")

# --- 溫潤米色護眼版 (Warm Beige & Soft Morandi Colors) CSS 注入 ---
custom_css = """
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header[data-testid="stHeader"] {background: transparent !important; visibility: visible !important;}
    
    .block-container {
        padding-top: 0rem !important; 
        padding-bottom: 0rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 100% !important;
    }
    
    /* 全局背景：溫潤羊絨米色 */
    .stApp { background-color: #f7f4ee !important; color: #38322c !important; }

    /* 側邊欄：暖米灰 */
    [data-testid="stSidebar"] { background-color: #e8e2da !important; border-right: 1px solid #d4ccc2 !important; }
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] span, [data-testid="stSidebar"] h3 { color: #38322c !important; }
    
    /* 數據面板：溫潤卡片與琥珀棕邊條 */
    .stMetric {
        background-color: #ede7df !important; 
        padding: 15px !important; 
        border-radius: 8px !important; 
        border: 1px solid #d9d0c7 !important;
        border-left: 4px solid #b45309 !important;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.05) !important;
    }
    .stMetric label { color: #6b6257 !important; font-size: 13px !important; font-weight: 600 !important; }
    .stMetric div[data-testid="stMetricValue"] { color: #1c1917 !important; font-size: 24px !important; font-weight: 700 !important; }
    
    /* 頁籤 (Tabs) 重構 */
    .stTabs [data-baseweb="tab-list"] { gap: 12px; background-color: transparent; margin-bottom: 15px; }
    .stTabs [data-baseweb="tab"] {
        height: 45px; background-color: #e8e2da;
        border-radius: 6px 6px 0px 0px; padding: 5px 25px; color: #57534e;
        border: 1px solid #d4ccc2; border-bottom: none; font-weight: 700; font-size: 15px;
    }
    .stTabs [aria-selected="true"] { background-color: #b45309 !important; color: #ffffff !important; border-color: #b45309 !important; }
    
    /* AI 柔和標籤面板 (低彩度莫蘭迪色) */
    .ai-panel {
        background-color: #ede7df; padding: 15px 20px; border-radius: 8px;
        border: 1px solid #d9d0c7; display: flex; justify-content: space-between;
        align-items: center; margin-bottom: 15px; color: #38322c;
    }
    .ai-tag { background-color: #b85c50; color: #fffdf9; padding: 5px 12px; border-radius: 4px; font-weight: bold; font-size: 14px;}
    .ai-tag.green { background-color: #5c8374; }

    /* 文字標題全面適應米色系 */
    h1, h2, h3, h4, h5, h6, p, span { color: #292524 !important; }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ==========================================
# 1. 頂部狀態列
# ==========================================
now = datetime.datetime.now()
st.markdown(f"<div style='color:#78716c; font-size:12px; margin-top:10px; margin-bottom:-15px;'>⚡ JARVIS 智能核心連線正常 ｜ 今日開盤基準: {now.strftime('%Y-%m-%d')} 09:00:00 ｜ 最後資料同步: {now.strftime('%H:%M:%S')}</div>", unsafe_allow_html=True)
st.markdown("<hr style='border-color:#d4ccc2;'>", unsafe_allow_html=True)

# ==========================================
# 2. 側邊欄控制中心
# ==========================================
st.sidebar.markdown("### ⚙️ 控制中心")
menu = st.sidebar.radio(
    "核心模組", 
    [
        "🏠 系統首頁 (戰情大廳)", 
        "🎯 個股深度戰情與法人同步工作站", 
        "🌊 產業資金與起漲雷達",
        "🛡️ 大盤系統風險濾網"
    ]
)

st.sidebar.markdown("<hr style='border-color:#d4ccc2;'>", unsafe_allow_html=True)
with st.sidebar.expander("📂 自選股監控 (Watchlist)", expanded=True):
    st.caption("點擊快速切換群組")
    st.button("🔥 短線爆量沖銷組 (4)")
    st.button("🛡️ 投信波段認養組 (6)")
    st.button("💰 ETF 被動資金池 (3)")

# ==========================================
# 模組 1：系統首頁 (戰情大廳)
# ==========================================
if menu == "🏠 系統首頁 (戰情大廳)":
    st.markdown("<h2>🏠 JARVIS 機構級台股戰情大廳</h2>", unsafe_allow_html=True)
    col_main, col_sop = st.columns([2.5, 1])
    
    with col_main:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("加權指數 TAEX", "21,500.23", "+120.45 (+0.56%)")
        col2.metric("櫃買指數 TPEX", "253.48", "+2.36 (+0.94%)")
        col3.metric("大盤天候雷達", "☀️ 晴天多頭", "持股上限 80%")
        col4.metric("法人今日合計", "買超 +219.7 億", "🔥 外資投信聯手")

        st.markdown("<h4 style='margin-top:20px;'>🌍 國際股市與總經風向</h4>", unsafe_allow_html=True)
        g1, g2, g3, g4 = st.columns(4)
        g1.metric("道瓊指數 (DJI)", "42,352.75", "+341.16 (+0.81%)")
        g2.metric("那斯達克 (IXIC)", "18,137.85", "+142.50 (+0.79%)")
        g3.metric("費半 (SOX)", "5,214.33", "+84.21 (+1.64%)")
        g4.metric("美元/台幣 (USD/TWD)", "31.852", "-0.045 (升值)", delta_color="inverse")
        
        col_heat, col_news = st.columns([1, 1.2])
        with col_heat:
            st.success("**📈 強勢吸金族群：**\n1. 矽光子概念 (佔 12%)\n2. 設備廠 (佔 9%)")
            st.error("**📉 弱勢提款族群：**\n1. 塑化類股 (報價跌)\n2. 鋼鐵 (外資調節)")
        with col_news:
            st.info("⚡ **[快訊 09:15]** 台積電 ADR 溢價，開盤跳空站上月線。\n⚡ **[快訊 10:30]** 投信連 8 加碼，鎖定散熱。")
        
    with col_sop:
        st.markdown("<h4>☑️ 交易員 SOP 紀律檢核</h4>", unsafe_allow_html=True)
        st.markdown("<div style='background-color:#ede7df; padding:15px; border-radius:8px; border:1px solid #d9d0c7;'>", unsafe_allow_html=True)
        
        c1 = st.checkbox("清晨 07:10 檢視夜盤與報告")
        c2 = st.checkbox("開盤前 09:00 嚴禁盲目追高")
        c3 = st.checkbox("盤中嚴守協議「量<1000張禁當沖」")
        c4 = st.checkbox("下班 20:30 更新數據")
        c5 = st.checkbox("夜間 21:00 覆核戰略目標")
        
        checked_count = sum([c1, c2, c3, c4, c5])
        progress_val = checked_count / 5.0
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.caption(f"🎯 SOP 執行進度 ({checked_count}/5)")
        st.progress(progress_val)
        
        if checked_count == 5:
            st.success("🟢 戰備就緒！今日操盤紀律 100% 達標！")
        else:
            st.warning("🔴 戰備整備中... 請落實各項紀律。")
            
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 模組 2：個股深度戰情與法人同步工作站
# ==========================================
elif menu == "🎯 個股深度戰情與法人同步工作站":
    col_search, col_space = st.columns([1, 2])
    with col_search:
        search_query = st.text_input("輸入代號:", "", label_visibility="collapsed", placeholder="🔍 輸入要查詢的股票代號 (例: 2330, 2317)...")

    if search_query:
        clean_code = search_query.strip()
        hist = pd.DataFrame()
        
        stock_name_map = {
            "2330": "台灣積體電路製造 (台積電)",
            "2317": "鴻海精密工業 (鴻海)",
            "2454": "聯發科技 (聯發科)",
            "3008": "大立光電 (大立光)",
            "2308": "台達電子 (台達電)",
            "2881": "富邦金融控股 (富邦金)",
            "2882": "國泰金融控股 (國泰金)",
            "2603": "長榮海運 (長榮)"
        }
        stock_name = stock_name_map.get(clean_code, f"台股上市櫃代號 {clean_code}")
        
        with st.spinner(f"正在同步代號 [{clean_code}] 的所有戰情與法人大數據..."):
            for suffix in ['.TW', '.TWO']:
                try:
                    ticker = yf.Ticker(f"{clean_code}{suffix}")
                    temp_hist = ticker.history(period="3mo")
                    if not temp_hist.empty:
                        hist = temp_hist
                        break
                except: pass

        if not hist.empty and len(hist) >= 30:
            today_close = hist['Close'].iloc[-1]
            change = today_close - hist['Close'].iloc[-2]
            change_pct = (change / hist['Close'].iloc[-2]) * 100
            ma5 = hist['Close'].tail(5).mean()
            ma20 = hist['Close'].tail(20).mean()
            is_strong = today_close > ma5 > ma20
            
            color = "#b85c50" if change >= 0 else "#5c8374"
            sign = "+" if change > 0 else ""
            
            st.markdown(f"""
            <div style="background-color: #ede7df; padding: 18px 22px; border-radius: 8px; border: 1px solid #d9d0c7; margin-bottom: 15px;">
                <div style="font-size: 13px; color: #78716c; font-weight: 600; margin-bottom: 6px;">📌 目前鎖定操盤標的與即時報價：</div>
                <div style="display: flex; align-items: baseline; flex-wrap: wrap; gap: 20px;">
                    <h2 style="margin: 0; color: #1c1917; font-size: 28px; font-weight: 800;">{clean_code} ｜ {stock_name}</h2>
                    <div>
                        <span style="font-size: 13px; color: #78716c; margin-right: 6px; font-weight: 600;">最新收盤價:</span>
                        <span style="color: {color}; font-size: 26px; font-weight: 700;">{today_close:.2f}</span>
                    </div>
                    <div>
                        <span style="font-size: 13px; color: #78716c; margin-right: 6px; font-weight: 600;">今日漲跌:</span>
                        <span style="color: {color}; font-size: 18px; font-weight: 700;">{sign}{change:.2f} ({sign}{change_pct:.2f}%)</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            ai_std = hist['Close'].pct_change().std() * today_close
            est_high = today_close + ai_std
            est_low = today_close - ai_std
            
            st.markdown(f"""
            <div class="ai-panel">
                <div>
                    <span class="ai-tag {'green' if not is_strong else ''}">{'🔴 真龍起漲 / 準備發動' if is_strong else '🟢 均線下彎 / 震盪洗盤'}</span>
                    <span style="color:#57534e; margin-left:15px; font-size:14px; font-weight:600;">🎯 AI 信心度: {88 if is_strong else 72}% ｜ 預估壓力區: {est_high:.1f} ｜ 預估支撐價: {est_low:.1f}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            sub_tab1, sub_tab2, sub_tab3 = st.tabs([
                "📈 1. K線工作站與主力分點", 
                "🏛️ 2. 三大法人籌碼雙軌透視 (5日/30日)", 
                "🌊 3. 產業資金流向與起漲雷達"
            ])

            with sub_tab1:
                df_chart = hist.tail(150) 
                fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.03, row_heights=[0.75, 0.25])
                
                fig.add_trace(go.Candlestick(
                    x=df_chart.index, open=df_chart['Open'], high=df_chart['High'], low=df_chart['Low'], close=df_chart['Close'],
                    increasing_line_color='#b85c50', increasing_fillcolor='#b85c50',
                    decreasing_line_color='#5c8374', decreasing_fillcolor='#5c8374', name='K線'
                ), row=1, col=1)
                
                fig.add_trace(go.Scatter(x=df_chart.index, y=df_chart['Close'].rolling(5).mean(), line=dict(color='#2563eb', width=1.5), name='5MA'), row=1, col=1)
                fig.add_trace(go.Scatter(x=df_chart.index, y=df_chart['Close'].rolling(20).mean(), line=dict(color='#d97706', width=1.5), name='20MA'), row=1, col=1)

                dummy_vol = [int(v * (1 if c >= 0 else -1) * 0.1) for v, c in zip(df_chart['Volume'], df_chart['Close'].diff().fillna(1))]
                vol_colors = ['#b85c50' if val >= 0 else '#5c8374' for val in dummy_vol]
                fig.add_trace(go.Bar(x=df_chart.index, y=dummy_vol, marker_color=vol_colors, name='買賣超'), row=2, col=1)

                fig.update_layout(
                    plot_bgcolor='#ede7df', paper_bgcolor='#ede7df', height=500, margin=dict(l=5, r=5, t=5, b=5), 
                    hovermode="x unified", showlegend=False, xaxis_rangeslider_visible=False, font=dict(color="#57534e")
                )
                fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#d9d0c7', showspikes=True, spikecolor="#78716c", spikethickness=1, spikemode="across")
                fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#d9d0c7', showspikes=True, spikecolor="#78716c", spikethickness=1, spikemode="across")
                fig.update_traces(xhoverformat="%Y-%m-%d", hovertemplate="<b>%{x}</b><br>高 %{high:.2f} ｜ 低 %{low:.2f}<br>開 %{open:.2f} ｜ 收 %{close:.2f}<extra></extra>", selector=dict(type='candlestick'))
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
                
                with st.expander("🏦 展開：前 20 大主力分點與外資進出雷達 (免換頁)"):
                    vol_today = int(hist['Volume'].iloc[-1] / 1000)
                    top_buyers = ["摩根士丹利", "美林", "摩根大通", "高盛", "瑞銀", "富邦-信義", "凱基-台北", "元大-台南", "群益-桃園", "永豐-台北", "元大證券", "凱基-信義", "富邦-板橋", "國泰-敦化", "日盛-內湖", "華南永昌", "兆豐-中壢", "第一金", "台新-台北", "群益-總公司"]
                    top_sellers = ["國泰-敦化", "元大-忠孝", "永豐金-高雄", "富邦-板橋", "群益-總公司", "港麥格理", "瑞士信貸", "巴克萊", "法國巴黎", "渣打", "元富-板橋", "統一-永康", "康和-台中", "兆豐-高雄", "華南永昌", "土銀-台北", "合庫", "彰銀", "土地銀行", "元大-信義"]
                    
                    buy_shares = [int(vol_today * (0.15 - i * 0.006)) for i in range(20)]
                    sell_shares = [int(vol_today * (0.12 - i * 0.005)) for i in range(20)]
                    stars_buy = [("★★★★★" if i < 5 else "★★★★" if i < 12 else "★★★") for i in range(20)]
                    stars_sell = [("⚠ 警戒" if i < 5 else "⚠ 注意" if i < 12 else "一般") for i in range(20)]

                    df_top_buy = pd.DataFrame({"排名": [f"第{i+1}名" for i in range(20)], "分點": top_buyers, "買進(張)": buy_shares, "星級": stars_buy})
                    df_top_sell = pd.DataFrame({"排名": [f"第{i+1}名" for i in range(20)], "分點": top_sellers, "賣出(張)": sell_shares, "星級": stars_sell})

                    col_b20, col_s20 = st.columns(2)
                    with col_b20:
                        st.markdown("<h5 style='color:#b85c50;'>🔴 買超主力大咖分點</h5>", unsafe_allow_html=True)
                        st.dataframe(df_top_buy, use_container_width=True, hide_index=True, height=400, column_config={"買進(張)": st.column_config.ProgressColumn("買進力道", format="%d", min_value=0, max_value=max(buy_shares)*1.2)})
                    with col_s20:
                        st.markdown("<h5 style='color:#5c8374;'>🟢 賣超調節分點</h5>", unsafe_allow_html=True)
                        st.dataframe(df_top_sell, use_container_width=True, hide_index=True, height=400, column_config={"賣出(張)": st.column_config.ProgressColumn("賣出力道", format="%d", min_value=0, max_value=max(sell_shares)*1.2)})

            with sub_tab2:
                df_30d = hist.tail(30).copy()
                dates_30 = df_30d.index.strftime('%m/%d').tolist()

                foreign_30, trust_30, dealer_30 = [], [], []
                for i in range(len(df_30d)):
                    vol = int(df_30d['Volume'].iloc[i] / 1000)
                    close_price = df_30d['Close'].iloc[i]
                    prev_close = df_30d['Close'].iloc[i-1] if i > 0 else df_30d['Close'].iloc[0]
                    change_pct = (close_price - prev_close) / prev_close * 100 if prev_close > 0 else 0
                    vol_factor = min(max(int(vol * 0.15), 50), 30000)
                    
                    foreign_30.append(int(vol_factor * (1.2 if change_pct >= 0 else -0.8) * (1 + abs(change_pct)*0.1)))
                    trust_30.append(int(vol_factor * 0.3 * (1 if change_pct > -0.5 else -0.5)))
                    dealer_30.append(int(vol_factor * 0.1 * (1 if change_pct > 0 else -1)))

                foreign_5, trust_5, dealer_5, dates_5 = foreign_30[-5:], trust_30[-5:], dealer_30[-5:], dates_30[-5:]
                today_total = foreign_30[-1] + trust_30[-1] + dealer_30[-1]

                g1, g2, g3, g4 = st.columns(4)
                g1.metric("今日外資", f"{foreign_30[-1]:+,} 張")
                g2.metric("今日投信", f"{trust_30[-1]:+,} 張")
                g3.metric("今日自營", f"{dealer_30[-1]:+,} 張")
                g4.metric("法人合計", f"{today_total:+,} 張", "🔥 同步買超" if today_total > 0 else "⚠️ 同步提款")
                st.markdown("<br>", unsafe_allow_html=True)
                
                inst_tab1, inst_tab2 = st.tabs(["📊 近 5 日法人動態 (短線轉折)", "📈 近 30 日波段籌碼 (長線成本)"])
                with inst_tab1:
                    fig_5 = go.Figure()
                    fig_5.add_trace(go.Bar(x=dates_5, y=foreign_5, name='外資', marker_color='#2563eb'))
                    fig_5.add_trace(go.Bar(x=dates_5, y=trust_5, name='投信', marker_color='#b85c50'))
                    fig_5.add_trace(go.Bar(x=dates_5, y=dealer_5, name='自營', marker_color='#d97706'))
                    fig_5.update_layout(plot_bgcolor='#ede7df', paper_bgcolor='#ede7df', font=dict(color="#57534e"), barmode='group', height=350, hovermode="x unified", margin=dict(l=5, r=5, t=10, b=5))
                    st.plotly_chart(fig_5, use_container_width=True, config={'displayModeBar': False})
                with inst_tab2:
                    fig_30 = go.Figure()
                    fig_30.add_trace(go.Bar(x=dates_30, y=foreign_30, name='外資', marker_color='#2563eb'))
                    fig_30.add_trace(go.Bar(x=dates_30, y=trust_30, name='投信', marker_color='#b85c50'))
                    fig_30.add_trace(go.Bar(x=dates_30, y=dealer_30, name='自營', marker_color='#d97706'))
                    fig_30.update_layout(plot_bgcolor='#ede7df', paper_bgcolor='#ede7df', font=dict(color="#57534e"), barmode='group', height=350, hovermode="x unified", margin=dict(l=5, r=5, t=10, b=5))
                    st.plotly_chart(fig_30, use_container_width=True, config={'displayModeBar': False})

            with sub_tab3:
                st.markdown("<h4>🌊 個股關聯產業資金流向與起漲雷達</h4>", unsafe_allow_html=True)
                df_ind = pd.DataFrame({"板塊": ["半導體", "電子組件", "電腦", "金融", "航運", "傳產", "生技", "通信"], "淨流入(億)": [145.2, 62.8, 48.5, 31.2, 24.6, -12.4, -18.5, -25.1]})
                fig_ind = go.Figure(go.Bar(x=df_ind["板塊"], y=df_ind["淨流入(億)"], marker_color=['#b85c50' if x>0 else '#5c8374' for x in df_ind["淨流入(億)"]]))
                fig_ind.update_layout(plot_bgcolor='#ede7df', paper_bgcolor='#ede7df', font=dict(color="#57534e"), height=300, margin=dict(t=10, b=10))
                st.plotly_chart(fig_ind, use_container_width=True, config={'displayModeBar': False})

                st.markdown("<h4 style='margin-top:20px;'>🥚 破底翻雷達：同步檢視同產業強勢標的</h4>", unsafe_allow_html=True)
                df_radar = pd.DataFrame({
                    "代號": [f"{clean_code} 概念股A", f"{clean_code} 概念股B", "3324 雙鴻", "3231 緯創"],
                    "技術型態": ["🔴 潛底成形", "🔴 突破壓力", "🟢 回測季線", "🔴 W底成形"],
                    "散戶(融資)": ["連 3 減 (-1200)", "連 2 減 (-850)", "大減 (-2100)", "連 4 減 (-5000)"],
                    "主力(外投)": ["連 3 買 (+3400)", "連 2 買 (+2100)", "由賣轉買 (+1500)", "大買 (+8500)"],
                    "評級": ["★★★★★", "★★★★", "★★★", "★★★★"]
                })
                st.dataframe(df_radar, use_container_width=True, hide_index=True)

        else:
            st.warning("⚠️ 請輸入有效的股票代號（例如 2330、2317），系統將立即為您同步解構所有維度！")

# ==========================================
# 模組 3：產業資金與起漲雷達
# ==========================================
elif menu == "🌊 產業資金與起漲雷達":
    st.markdown("<h2>🌊 總體產業資金流向與起漲雷達總覽</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("資金最強主流", "半導體產業", "+5.4% (佔 38%)")
    c2.metric("次族群黑馬", "航運與造紙", "+3.1% (佔 14%)")
    c3.metric("資金流出避險", "生技醫療", "-1.8% (佔 4%)")

    df_ind = pd.DataFrame({"板塊": ["半導體", "電子組件", "電腦", "金融", "航運", "傳產", "生技", "通信"], "淨流入(億)": [145.2, 62.8, 48.5, 31.2, 24.6, -12.4, -18.5, -25.1]})
    fig_ind = go.Figure(go.Bar(x=df_ind["板塊"], y=df_ind["淨流入(億)"], marker_color=['#b85c50' if x>0 else '#5c8374' for x in df_ind["淨流入(億)"]]))
    fig_ind.update_layout(plot_bgcolor='#ede7df', paper_bgcolor='#ede7df', font=dict(color="#57534e"), height=300, margin=dict(t=10, b=10))
    st.plotly_chart(fig_ind, use_container_width=True, config={'displayModeBar': False})

    st.markdown("<h4 style='margin-top:20px;'>🥚 全市場破底翻雷達：散戶恐慌退場 vs 主力吃貨</h4>", unsafe_allow_html=True)
    df_radar = pd.DataFrame({
        "代號": ["8996 高力", "2383 台光電", "3324 雙鴻", "3231 緯創"],
        "技術型態": ["🔴 潛底成形", "🔴 突破壓力", "🟢 回測季線", "🔴 W底成形"],
        "散戶(融資)": ["連 3 減 (-1200)", "連 2 減 (-850)", "大減 (-2100)", "連 4 減 (-5000)"],
        "主力(外投)": ["連 3 買 (+3400)", "連 2 買 (+2100)", "由賣轉買 (+1500)", "大買 (+8500)"],
        "評級": ["★★★★★", "★★★★", "★★★", "★★★★"]
    })
    st.dataframe(df_radar, use_container_width=True, hide_index=True)

# ==========================================
# 模組 4：系統性風險追蹤
# ==========================================
elif menu == "🛡️ 大盤系統風險濾網":
    st.markdown("<h2>🛡️️ 總體經濟與風險濾網</h2>", unsafe_allow_html=True)
    r1, r2, r3, r4 = st.columns(4)
    r1.metric("融資維持率", "165.4%", "安全區 (>160%)")
    r2.metric("VIX 恐慌指數", "14.2 點", "市場情緒穩定")
    r3.metric("台幣匯率", "31.85", "熱錢微幅匯出")
    r4.metric("大盤乖離率", "+3.2%", "無過熱超買現象")
    
    col_risk1, col_risk2 = st.columns(2)
    with col_risk1:
        st.markdown("<h4 style='margin-top:20px;'>🛡️️ 風控檢核</h4>", unsafe_allow_html=True)
        st.write("• **籌碼清洗**：散戶餘額穩定，無多殺多現象。")
        st.write("• **技術結構**：加權穩守季線(MA60)，多頭架構未破。")
        st.markdown(f"""
        <div class="ai-panel" style="border-left: 4px solid #5c8374;">
            <div>
                <span class="ai-tag green">風險係數：低</span>
                <span style="color:#57534e; margin-left:15px; font-size:14px; font-weight:600;">建議維持 7-8 成資金配置。</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_risk2:
        st.markdown("<h4 style='margin-top:20px;'>📉 VIX 趨勢</h4>", unsafe_allow_html=True)
        fig_risk = go.Figure(go.Scatter(x=['9月W1', '9月W2', '9月W3', '9月W4', '最新'], y=[15.1, 16.5, 14.8, 13.9, 14.2], mode='lines+markers', line=dict(color='#d97706', width=3)))
        fig_risk.update_layout(plot_bgcolor='#ede7df', paper_bgcolor='#ede7df', font=dict(color="#57534e"), height=250, margin=dict(t=10, b=10))
        st.plotly_chart(fig_risk, use_container_width=True, config={'displayModeBar': False})
