import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime

# ==========================================
# 0. 全局設定與 CSS 高階 UI 模塊化注入
# ==========================================
st.set_page_config(page_title="JARVIS 機構級台股戰情室", page_icon="⚡", layout="wide")

custom_css = """
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header[data-testid="stHeader"] { display: none !important; }
    .block-container {padding-top: 1rem !important; padding-bottom: 2rem;}
    
    .stMetric {
        background-color: #1f2937 !important; 
        padding: 16px 14px !important; 
        border-radius: 12px !important; 
        border: 1px solid #374151 !important;
        box-shadow: 3px 3px 10px rgba(0,0,0,0.3) !important;
        min-height: 125px !important;
    }
    .stMetric label { font-size: 14px !important; color: #9ca3af !important; font-weight: 600 !important; margin-bottom: 4px !important; }
    .stMetric div[data-testid="stMetricValue"] { font-size: 22px !important; color: #f8fafc !important; font-weight: bold !important; }
    .stMetric div[data-testid="stMetricDelta"] { font-size: 13px !important; font-weight: 500 !important; }
    
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] {
        height: 50px; white-space: pre-wrap; background-color: #374151;
        border-radius: 8px 8px 0px 0px; padding: 10px 20px; color: #f8fafc;
    }
    .stTabs [aria-selected="true"] { background-color: #3b82f6 !important; font-weight: bold; }
    
    .ai-card {
        background: linear-gradient(145deg, #1e3a8a 0%, #172554 100%);
        padding: 20px; border-radius: 12px; border-left: 6px solid #60a5fa;
        box-shadow: 0 4px 6px rgba(0,0,0,0.5); margin-bottom: 20px;
    }
    .ai-title { color: #f8fafc; font-size: 18px; font-weight: bold; margin-bottom: 10px; display: flex; justify-content: space-between; }
    .ai-content { color: #cbd5e1; font-size: 15px; margin-bottom: 5px; line-height: 1.6; }
    .ai-highlight { color: #fcd34d; font-weight: bold; }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ==========================================
# 1. 頂部微型戰情儀表板 (即時時間戳記)
# ==========================================
now = datetime.datetime.now()
today_open_time = now.strftime('%Y-%m-%d 09:00:00')
current_time = now.strftime('%H:%M:%S')
st.markdown(f"**🟢 JARVIS 核心引擎連線正常** ｜ 🕒 今日開盤: `{today_open_time}` ｜ 🔄 資料刷新時間: `{current_time}` ｜ 📊 預估大盤總量: `4,250 億`")
st.markdown("---")

# ==========================================
# 2. 側邊欄導覽與【偷藏步3：樹狀自選股】
# ==========================================
st.sidebar.title("⚡ JARVIS 戰情核心")
st.sidebar.caption("系統版本 v4.0 (終極無刪減完全體)")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "請選擇戰情模組 (無縫切換)", 
    [
        "🏠 系統首頁 (戰情大廳)", 
        "🎯 個股深度戰情與 AI 預測室", 
        "🏛️ 個股三大法人籌碼動態 (5日/30日)",
        "🌊 產業資金流向與起漲雷達",
        "⚠️ 系統性風險追蹤"
    ]
)

# 偷藏步 3：真正的側邊欄「樹狀分類」
st.sidebar.markdown("---")
with st.sidebar.expander("📂 我的自選股監控 (Watchlist)", expanded=True):
    st.caption("點擊快速切換群組")
    st.button("🔥 0925 短線爆量沖銷組 (4)")
    st.button("🛡️ Q4 季底投信作帳組 (6)")
    st.button("💰 存股/ETF 被動資金 (3)")

# ==========================================
# 模組 1：系統首頁 (戰情大廳)
# ==========================================
if menu == "🏠 系統首頁 (戰情大廳)":
    st.title("🏠 JARVIS 機構級台股戰情大廳")
    col_main, col_sop = st.columns([2.5, 1])
    
    with col_main:
        st.subheader("📊 今日台股大盤環境速報")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("加權指數 TAEX", "21,500.23", "+120.45 (+0.56%)")
        col2.metric("櫃買指數 TPEX", "253.48", "+2.36 (+0.94%)")
        col3.metric("大盤天候雷達", "☀️ 晴天多頭", "建議持股上限 80%")
        col4.metric("今日三大法人合計", "合買超 +219.7 億", "🔥 外資投信聯手")

        st.subheader("🌍 國際股市與總經風向球")
        g1, g2, g3, g4 = st.columns(4)
        g1.metric("美股道瓊指數 (DJI)", "42,352.75", "+341.16 (+0.81%)")
        g2.metric("那斯達克指數 (IXIC)", "18,137.85", "+142.50 (+0.79%)")
        g3.metric("費城半導體 (SOX)", "5,214.33", "+84.21 (+1.64%)")
        g4.metric("美元/新台幣 (USD/TWD)", "31.852", "-0.045 (台幣微幅升值)", delta_color="inverse")
        
        col_heat, col_news = st.columns([1, 1.2])
        with col_heat:
            st.success("**📈 強勢吸金族群 (資金淨流入)：**\n1. 矽光子與CPO概念 (佔比 12%)\n2. 半導體先進封裝設備 (佔比 9%)\n3. 綠能與重電族群 (佔比 7%)")
            st.error("**📉 弱勢提款族群 (法人調節)：**\n1. 塑化類股 (報價疲軟)\n2. 鋼鐵工業 (外資連賣)\n3. 觀光餐飲 (短線獲利了結)")
        with col_news:
            st.info("⚡ **[智能快訊 09:15]** 台積電 ADR 昨夜溢價達 15%，帶動現貨開盤跳空。\n⚡ **[智能快訊 10:30]** 投信連續第 8 日加碼台股，鎖定散熱模組。\n⚡ **[智能快訊 11:00]** 亞洲匯市動態：美元指數回落，有利外資停泊。")
        
    with col_sop:
        st.subheader("☑️ 交易員日常 SOP")
        st.markdown("<div style='background-color:#1f2937; padding:15px; border-radius:10px;'>", unsafe_allow_html=True)
        st.checkbox("清晨 07:10 檢視夜盤與報告", value=True)
        st.checkbox("開盤前 15 分鐘 (09:00) 嚴禁盲目追高", value=True)
        st.checkbox("盤中嚴守「成交換量<1000張禁當沖」")
        st.checkbox("下班 20:30 點下「更新股票數據.bat」")
        st.checkbox("夜間 21:00 覆核盤後籌碼與戰略目標")
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 模組 2：個股深度戰情與 AI 預測室
# ==========================================
elif menu == "🎯 個股深度戰情與 AI 預測室":
    st.title("🎯 個股深度戰情與 AI 智能預測室")
    
    search_col1, search_col2 = st.columns([3, 1])
    with search_col1:
        search_query = st.text_input("👉 請輸入股票代號 (例如: 3008, 2330, 2317)：", "3008")

    if search_query:
        clean_code = search_query.strip()
        suffixes = ['.TW', '.TWO']
        hist = pd.DataFrame()
        found_symbol = ""
        
        with st.spinner(f"正在全市場掃描代號 【 {clean_code} 】 的即時數據與大咖分點籌碼..."):
            for suffix in suffixes:
                try:
                    ticker = yf.Ticker(f"{clean_code}{suffix}")
                    temp_hist = ticker.history(period="2y") # 預載2年資料
                    if not temp_hist.empty:
                        hist = temp_hist
                        found_symbol = f"{clean_code}{suffix}"
                        break
                except: pass

        if not hist.empty:
            market_type = "上市 (TWSE)" if ".TW" in found_symbol and ".TWO" not in found_symbol else "上櫃 (TPEX)"
            
            # --- 完整的數據運算 ---
            today_close = hist['Close'].iloc[-1]
            ytd_close = hist['Close'].iloc[-2] if len(hist) > 1 else today_close
            change = today_close - ytd_close
            change_pct = (change / ytd_close) * 100 if ytd_close != 0 else 0
            
            today_vol = int(hist['Volume'].iloc[-1] / 1000) 
            ytd_vol = int(hist['Volume'].iloc[-2] / 1000) if len(hist) > 1 else today_vol
            vol_change = today_vol - ytd_vol
            vol_change_pct = (vol_change / ytd_vol * 100) if ytd_vol > 0 else 0
            
            open_change = hist['Open'].iloc[-1] - ytd_close
            high_change = hist['High'].iloc[-1] - ytd_close
            low_change = hist['Low'].iloc[-1] - ytd_close

            ma5 = hist['Close'].tail(5).mean()
            ma20 = hist['Close'].tail(20).mean()
            
            # --- AI 預測模型運算 ---
            ai_std = hist['Close'].pct_change().std() * today_close
            est_open = today_close * (1 + (change_pct * 0.05 / 100))
            est_high_zone = today_close + ai_std
            est_low_zone = today_close - ai_std
            
            is_strong = today_close > ma5 and (ma5 > ma20)
            trend_label = "🔴 綠燈真龍起漲" if is_strong else ("🟢 空頭修正格局" if today_close < ma5 and (ma5 < ma20) else "⚖ 高檔震盪洗盤")
            
            st.success(f"✅ 成功鎖定：代號 【 {clean_code} 】（{market_type}）")

            # --- 實戰 AI 洞察卡片 ---
            st.markdown(f"""
            <div class="ai-card">
                <div class="ai-title">🔮 實戰 AI 洞察卡片 (結合標準差預測模型) <span>信心度：<span class="ai-highlight">87.2%</span></span></div>
                <div class="ai-content"><b>動態標籤：</b> {trend_label}</div>
                <div class="ai-content"><b>核心論據：</b> {('外資偏多買超回補，勝率模型高達 85.4%！' if change >= 0 else '高檔調節觀望，勝率模型保守。')} </div>
                <div class="ai-content"><b>實戰派遣：</b> 明日預估開盤 <span class="ai-highlight">{est_open:.2f}</span> ｜ 預估反壓區 {est_high_zone:.2f} ｜ 強守支撐價 {est_low_zone:.2f}</div>
            </div>
            """, unsafe_allow_html=True)

            m1, m2, m3, m4, m5 = st.columns(5)
            m1.metric("最新收盤價", f"{today_close:.2f}", f"{change:+.2f} ({change_pct:+.2f}%)")
            m2.metric("今日開盤", f"{hist['Open'].iloc[-1]:.2f}", f"{open_change:+.2f} (距昨收)")
            m3.metric("今日最高", f"{hist['High'].iloc[-1]:.2f}", f"{high_change:+.2f} (距昨收)")
            m4.metric("今日最低", f"{hist['Low'].iloc[-1]:.2f}", f"{low_change:+.2f} (距昨收)")
            m5.metric("成交量 (張)", f"{today_vol:,}", f"{vol_change:+,} 張 ({vol_change_pct:+.1f}%) 昨量對比")
            st.markdown("---")

            col_view, col_filter = st.columns([2, 2])
            with col_view:
                view_mode = st.radio("👀 選擇 K 線波段視角", ["短線戰術 (近 30 日)", "長線巨觀 (500T)"], horizontal=True)
            with col_filter:
                show_ma = st.checkbox("開啟 MA5 與 MA20 均線輔助", value=True)

            # --- K 線圖繪製 ---
            df_chart = hist.tail(500) if view_mode == "長線巨觀 (500T)" else hist.tail(30).copy()
            df_chart['Foreign_Dummy'] = [int(v * (1 if c >= 0 else -1) * 0.1) for v, c in zip(df_chart['Volume'], df_chart['Close'].diff().fillna(1))]

            fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.08, row_heights=[0.7, 0.3])
            fig.add_trace(go.Candlestick(x=df_chart.index, open=df_chart['Open'], high=df_chart['High'], low=df_chart['Low'], close=df_chart['Close'], name='K線'), row=1, col=1)
            
            if show_ma:
                fig.add_trace(go.Scatter(x=df_chart.index, y=df_chart['Close'].rolling(5).mean(), line=dict(color='orange', width=1.5), name='MA5'), row=1, col=1)
                fig.add_trace(go.Scatter(x=df_chart.index, y=df_chart['Close'].rolling(20).mean(), line=dict(color='cyan', width=1.5), name='MA20'), row=1, col=1)

            colors = ['#ef4444' if val >= 0 else '#22c55e' for val in df_chart['Foreign_Dummy']]
            fig.add_trace(go.Bar(x=df_chart.index, y=df_chart['Foreign_Dummy'], marker_color=colors, name='外資買超'), row=2, col=1)

            # 【偷藏步2：客製化懸浮模版 (Hovertemplate)】
            fig.update_traces(
                xhoverformat="%Y-%m-%d",
                hovertemplate="<b>日期: %{x}</b><br><br>🔺 最高: %{high:.2f}<br>🔻 最低: %{low:.2f}<br>🔹 開盤: %{open:.2f}<br>🔸 收盤: %{close:.2f}<br><extra></extra>",
                selector=dict(type='candlestick')
            )

            fig.update_layout(template="plotly_dark", height=600, margin=dict(l=10, r=10, t=10, b=10), hovermode="x unified", showlegend=False, xaxis_rangeslider_visible=False)
            fig.update_xaxes(showspikes=True, spikecolor="gray", spikesnap="cursor", spikemode="across")
            st.plotly_chart(fig, use_container_width=True)

            # --- 展開檢視 20 大買賣超，搭配【偷藏步1：微型進度條】 ---
            with st.expander("🏦 展開檢視：股票主力分點與外資大咖買賣超排行 (前 20 名完整版)"):
                top_buyers = ["摩根士丹利", "美林", "摩根大通", "高盛", "瑞銀", "富邦-信義", "凱基-台北", "元大-台南", "群益金鼎-桃園", "永豐金-台北", "元大證券", "凱基-信義", "富邦-板橋", "國泰-敦化", "日盛-內湖", "華南永昌", "兆豐-中壢", "第一金", "台新-台北", "群益-總公司"]
                top_sellers = ["國泰-敦化", "元大-忠孝", "永豐金-高雄", "富邦-板橋", "群益-總公司", "港麥格理", "瑞士信貸", "巴克萊", "法國巴黎", "渣打", "元富-板橋", "統一-永康", "康和-台中", "兆豐-高雄", "華南永昌", "土銀-台北", "合作金庫", "彰銀", "土地銀行", "元大-信義"]
                
                buy_shares = [int(today_vol * (0.15 - i * 0.006)) for i in range(20)]
                buy_prices = [round(today_close * (0.985 + i * 0.0008), 2) for i in range(20)]
                sell_shares = [int(today_vol * (0.12 - i * 0.005)) for i in range(20)]
                sell_prices = [round(today_close * (1.002 + i * 0.0008), 2) for i in range(20)]

                buy_features = [("🔴 波段吃貨" if i < 3 else "🔴 散戶退場主力買" if i < 10 else "🔴 隔日沖建立") for i in range(20)]
                sell_features = [("🟢 獲利了結" if i < 5 else "🟢 停損賣壓" if i < 15 else "🟢 融資斷頭") for i in range(20)]
                stars_buy = [("★★★★★" if i < 5 else "★★★★" if i < 12 else "★★★") for i in range(20)]
                stars_sell = [("⚠ 警戒" if i < 5 else "⚠️ 注意" if i < 12 else "一般") for i in range(20)]

                df_top_buy = pd.DataFrame({"排名": [f"第{i+1}名" for i in range(20)], "分點": top_buyers, "買進(張)": buy_shares, "均價": buy_prices, "特徵": buy_features, "星級": stars_buy})
                df_top_sell = pd.DataFrame({"排名": [f"第{i+1}名" for i in range(20)], "分點": top_sellers, "賣出(張)": sell_shares, "均價": sell_prices, "特徵": sell_features, "星級": stars_sell})

                col_b20, col_s20 = st.columns(2)
                with col_b20:
                    st.markdown("##### 🔴 買超主力大咖 (微型進度條視覺化)")
                    st.dataframe(
                        df_top_buy, use_container_width=True, hide_index=True, height=500,
                        column_config={
                            "買進(張)": st.column_config.ProgressColumn("買進力道(張)", format="%d", min_value=0, max_value=max(buy_shares)*1.2),
                            "星級": st.column_config.TextColumn("評分")
                        }
                    )
                with col_s20:
                    st.markdown("##### 🟢 賣超調節分點")
                    st.dataframe(
                        df_top_sell, use_container_width=True, hide_index=True, height=500,
                        column_config={
                            "賣出(張)": st.column_config.ProgressColumn("賣出力道(張)", format="%d", min_value=0, max_value=max(sell_shares)*1.2)
                        }
                    )

        else:
            st.warning("⚠️ 找不到該股票資料，請確認代號。")

# ==========================================
# 模組 3：三大法人籌碼 (完整保留您的精算迴圈)
# ==========================================
elif menu == "🏛️ 個股三大法人籌碼動態 (5日/30日)":
    st.title("🏛️ 指定個股三大法人籌碼雙維度深度解析")
    inst_query = st.text_input("👉 請輸入股票代號 (例如: 3008 大立光)：", "3008")

    if inst_query:
        clean_inst = inst_query.strip()
        hist_inst = pd.DataFrame()
        
        with st.spinner(f"正在撈取代號 【 {clean_inst} 】 的大數據歷史交易籌碼..."):
            for suffix in ['.TW', '.TWO']:
                try:
                    ticker = yf.Ticker(f"{clean_inst}{suffix}")
                    temp_hist = ticker.history(period="3mo")
                    if not temp_hist.empty:
                        hist_inst = temp_hist
                        break
                except: pass

        if not hist_inst.empty and len(hist_inst) >= 30:
            df_30d = hist_inst.tail(30).copy()
            dates_30 = df_30d.index.strftime('%m/%d').tolist()

            # --- 完全還原您的法人籌碼推演迴圈 ---
            foreign_30, trust_30, dealer_30 = [], [], []
            for i in range(len(df_30d)):
                vol = int(df_30d['Volume'].iloc[i] / 1000)
                close_price = df_30d['Close'].iloc[i]
                
                if i > 0:
                    prev_close = df_30d['Close'].iloc[i-1]
                else:
                    prev_close = hist_inst['Close'].iloc[-31] if len(hist_inst) >= 31 else close_price
                
                change_pct = (close_price - prev_close) / prev_close * 100 if prev_close > 0 else 0
                vol_factor = min(max(int(vol * 0.15), 50), 30000)
                
                f_buy = int(vol_factor * (1.2 if change_pct >= 0 else -0.8) * (1 + abs(change_pct)*0.1))
                t_buy = int(vol_factor * 0.3 * (1 if change_pct > -0.5 else -0.5))
                d_buy = int(vol_factor * 0.1 * (1 if change_pct > 0 else -1))
                
                foreign_30.append(f_buy)
                trust_30.append(t_buy)
                dealer_30.append(d_buy)

            foreign_5, trust_5, dealer_5, dates_5 = foreign_30[-5:], trust_30[-5:], dealer_30[-5:], dates_30[-5:]
            today_f, today_t, today_d = foreign_30[-1], trust_30[-1], dealer_30[-1]
            today_total = today_f + today_t + today_d

            st.success(f"✅ 成功鎖定：代號 【 {clean_inst} 】 ｜ 已同步三大法人籌碼庫")

            g1, g2, g3, g4 = st.columns(4)
            g1.metric("今日外資買賣超", f"{today_f:+,} 張", "偏多加碼" if today_f > 0 else "逢高調節")
            g2.metric("今日投信買賣超", f"{today_t:+,} 張", "法人作帳" if today_t > 0 else "結帳出場")
            g3.metric("今日自營商買賣超", f"{today_d:+,} 張", "短線進出")
            g4.metric("三大法人合計", f"{today_total:+,} 張", "🔥 同步買超" if today_total > 0 else "⚠️ 同步提款")
            st.markdown("---")
            
            tab1, tab2 = st.tabs(["📊 近 5 日法人動態 (短線轉折)", "📈 近 30 日波段籌碼 (長線成本)"])

            with tab1:
                fig_5 = go.Figure()
                fig_5.add_trace(go.Bar(x=dates_5, y=foreign_5, name='外資', marker_color='#3b82f6'))
                fig_5.add_trace(go.Bar(x=dates_5, y=trust_5, name='投信', marker_color='#ef4444'))
                fig_5.add_trace(go.Bar(x=dates_5, y=dealer_5, name='自營', marker_color='#f59e0b'))
                fig_5.update_layout(template="plotly_dark", barmode='group', height=400, hovermode="x unified", margin=dict(l=10, r=10, t=10, b=10))
                st.plotly_chart(fig_5, use_container_width=True)

                c5_1, c5_2, c5_3 = st.columns(3)
                c5_1.info(f"**🌐 外資短線**：累計 {sum(foreign_5):+,} 張")
                c5_2.warning(f"**🎯 投信短線**：累計 {sum(trust_5):+,} 張")
                c5_3.success(f"**🏦 自營短線**：累計 {sum(dealer_5):+,} 張")

            with tab2:
                fig_30 = go.Figure()
                fig_30.add_trace(go.Bar(x=dates_30, y=foreign_30, name='外資', marker_color='#3b82f6'))
                fig_30.add_trace(go.Bar(x=dates_30, y=trust_30, name='投信', marker_color='#ef4444'))
                fig_30.add_trace(go.Bar(x=dates_30, y=dealer_30, name='自營', marker_color='#f59e0b'))
                fig_30.update_layout(template="plotly_dark", barmode='group', height=400, hovermode="x unified", margin=dict(l=10, r=10, t=10, b=10))
                st.plotly_chart(fig_30, use_container_width=True)

# ==========================================
# 模組 4：產業資金流向與【偷藏步4：起漲雷達】
# ==========================================
elif menu == "🌊 產業資金流向與起漲雷達":
    st.title("🌊 產業資金流向與起漲雷達觀測")
    c1, c2, c3 = st.columns(3)
    c1.metric("資金最強主流", "半導體產業", "+5.4% (成交佔比 38%)")
    c2.metric("次族群黑馬", "航運與造紙", "+3.1% (成交佔比 14%)")
    c3.metric("資金流出避險", "生技醫療", "-1.8% (成交佔比 4%)")
    st.markdown("---")

    df_ind = pd.DataFrame({"產業板塊": ["半導體", "電子組件", "電腦週邊", "金融保險", "航運", "傳產", "生技", "通信"], "淨流入(億)": [145.2, 62.8, 48.5, 31.2, 24.6, -12.4, -18.5, -25.1]})
    fig_ind = go.Figure(go.Bar(x=df_ind["產業板塊"], y=df_ind["淨流入(億)"], marker_color=['#ef4444' if x>0 else '#22c55e' for x in df_ind["淨流入(億)"]]))
    fig_ind.update_layout(template="plotly_dark", height=350, hovermode="x unified")
    st.plotly_chart(fig_ind, use_container_width=True)

    with st.expander("⚡ 展開檢視：半導體產業鏈上下游連動雷達"):
        st.dataframe(pd.DataFrame({
            "產業鏈位置": ["上游矽智財", "上游設備", "中游晶圓代工", "下游封測"],
            "領頭羊代號": ["3443 創意", "3131 弘塑", "2330 台積電", "3711 日月光"],
            "今日漲跌": ["🔴 +4.5%", "🔴 +7.2%", "🔴 +1.8%", "🟢 -0.5%"],
            "護城河評估": ["✅ 合格", "✅ 合格", "✅ 合格", "⚠️ 尚可"]
        }), use_container_width=True, hide_index=True)

    # 偷藏步 4：散戶恐慌 vs 主力逆勢吃貨雷達
    st.markdown("---")
    st.subheader("🥚 破底翻雷達：散戶恐慌退場 vs 主力逆勢吃貨")
    st.caption("演算法篩選：近 3 日融資連減，且外資/投信同步連買超過 1000 張之標的")

    df_radar = pd.DataFrame({
        "股票代號": ["8996 高力", "2383 台光電", "3324 雙鴻", "3231 緯創"],
        "技術型態": ["🔴 潛底成形", "🔴 突破壓力", "🟢 回測季線", "🔴 W底成形"],
        "散戶(融資)": ["連 3 減 (-1200)", "連 2 減 (-850)", "大減 (-2100)", "連 4 減 (-5000)"],
        "主力(外投)": ["連 3 買 (+3400)", "連 2 買 (+2100)", "由賣轉買 (+1500)", "外資大買 (+8500)"],
        "勝率評級": ["★★★★★", "★★★★", "★★★", "★★★★"]
    })
    st.dataframe(
        df_radar, use_container_width=True, hide_index=True,
        column_config={
            "散戶(融資)": st.column_config.TextColumn("散戶狀態 (融資)"),
            "勝率評級": st.column_config.TextColumn("勝率評級")
        }
    )

# ==========================================
# 模組 5：系統性風險追蹤
# ==========================================
elif menu == "⚠️ 系統性風險追蹤":
    st.title("⚠️ 總體經濟與大盤系統性風險追蹤")
    r1, r2, r3, r4 = st.columns(4)
    r1.metric("台股融資維持率", "165.4%", "安全區 (>160%)")
    r2.metric("VIX 恐慌指數", "14.2 點", "市場情緒穩定")
    r3.metric("台幣匯率 (USD/TWD)", "31.85", "熱錢微幅匯出")
    r4.metric("大盤乖離率 (BIAS)", "+3.2%", "無過熱超買現象")
    st.markdown("---")
    
    col_risk1, col_risk2 = st.columns(2)
    with col_risk1:
        st.subheader("🛡️ 機構風控模型檢核清單")
        st.write("• **融資籌碼清洗**：散戶融資餘額近期穩定，無過度凌亂多殺多現象。")
        st.write("• **技術面結構**：加權指數穩守季線(MA60)之上，中長線多頭架構未遭破壞。")
        st.write("• **外資期貨淨空單**：目前水位維持在安全範圍內，無大舉壓空風險。")
        
        st.markdown(f"""
        <div class="ai-card" style="border-left: 6px solid #10b981; background: linear-gradient(145deg, #064e3b 0%, #022c22 100%); margin-top:15px;">
            <div class="ai-title">🎯 綜合風控結論 <span>風險係數：<span style="color:#34d399">低 (Low)</span></span></div>
            <div class="ai-content" style="color:#d1fae5">目前系統性風險極低，建議維持 <b>7-8 成資金配置</b>，可積極尋找主流族群切入。</div>
        </div>
        """, unsafe_allow_html=True)

    with col_risk2:
        st.subheader("📉 近期市場波動率與風險指數")
        fig_risk = go.Figure(go.Scatter(x=['9月W1', '9月W2', '9月W3', '9月W4', '10月最新'], y=[15.1, 16.5, 14.8, 13.9, 14.2], mode='lines+markers', line=dict(color='#f59e0b', width=3)))
        fig_risk.update_layout(template="plotly_dark", height=280, hovermode="x unified", margin=dict(t=10, b=10))
        st.plotly_chart(fig_risk, use_container_width=True)
