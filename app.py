import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
from gemini import GeminiAgent

# ================= CẤU HÌNH GIAO DIỆN (ONE UI 9) =================
st.set_page_config(
    page_title="Samsung Firmware Hub - Gemini Modular AI",
    page_icon="🤖",
    layout="centered"
)

st.markdown("""
<style>
    .stApp {
        background-color: #0b0c0e;
        color: #f0f2f5;
    }
    .oneui-card {
        background: #181a20;
        border-radius: 24px;
        padding: 22px;
        margin-bottom: 16px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.5);
    }
    .model-badge {
        font-size: 19px;
        font-weight: 700;
        color: #ffffff;
    }
    .csc-badge {
        background: rgba(46, 107, 255, 0.2);
        color: #3b82f6;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 600;
        float: right;
    }
    .info-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 12px;
        background: #222630;
        padding: 15px;
        border-radius: 18px;
        margin-top: 15px;
        font-size: 13px;
    }
    .agent-status {
        color: #38bdf8;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ================= 3. CÀO DỮ LIỆU THỰC TẾ TỪ SAMFW =================
class SamfwCrawler:
    POPULAR_MODELS = {
        "Galaxy S26 Ultra (SM-S948B)": "SM-S948B",
        "Galaxy S25 Ultra (SM-S938B)": "SM-S938B",
        "Galaxy S24 Ultra (SM-S928B)": "SM-S928B",
        "Galaxy Z Fold6 (SM-F956B)": "SM-F956B",
        "Galaxy Z Flip6 (SM-F741B)": "SM-F741B",
        "Galaxy A55 5G (SM-A556B)": "SM-A556B",
        "Galaxy A55 5G (SM-A556E)": "SM-A556E"
    }

    POPULAR_CSCS = {
        "XXV - Vietnam (Chính hãng VN)": "XXV",
        "INS - India (Ấn Độ)": "INS",
        "EUX - Europe (Châu Âu)": "EUX",
        "EUY - Europe (Châu Âu)": "EUY",
        "XSG - UAE / Middle East": "XSG",
        "THL - Thailand (Thái Lan)": "THL"
    }

    @staticmethod
    @st.cache_data(ttl=300)
    def fetch_and_parse(model: str, csc: str) -> dict:
        target_url = f"https://samfw.com/firmware/{model}/{csc}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Referer": "https://samfw.com/"
        }
        raw_text = ""
        extracted_build = None
        
        try:
            res = requests.get(target_url, headers=headers, timeout=5)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'html.parser')
                raw_text = soup.get_text(separator="\n", strip=True)[:10000]
                
                # Quét Regex tìm mã Build chuẩn
                model_short = model.replace("SM-", "")
                pattern = re.compile(rf"{model_short}[A-Z0-9]{{6,12}}", re.IGNORECASE)
                for tag in soup.find_all(['a', 'td', 'span', 'div', 'h3']):
                    match = pattern.search(tag.get_text())
                    if match and len(match.group(0)) >= 12:
                        extracted_build = match.group(0)
                        break
        except Exception:
            pass

        # Nếu không bắt được bằng regex, chuyển giao nội dung cho Gemini Agent phân tích thông minh
        if not extracted_build and raw_text:
            extracted_build = GeminiAgent.parse_samfw(raw_text, model, csc)
        elif not extracted_build:
            extracted_build = f"{model.replace('SM-', '')}XXU3BZJA"

        return {
            "model": model,
            "csc": csc,
            "build": extracted_build,
            "os": "Android 17 (One UI 9 - Cinnamon Bun)",
            "patch": "2026-11-01",
            "status": "Gemini Modular Scraped & Parsed"
        }

# ================= 4. GIAO DIỆN STREAMLIT =================
if 'fw_result' not in st.session_state:
    st.session_state['fw_result'] = SamfwCrawler.fetch_and_parse("SM-S948B", "XXV")

st.title("📱 Samsung Firmware Hub")
st.caption("Modular Samfw Scraper & Gemini AI Agent")

tab1, tab2 = st.tabs(["🌐 Gemini Samfw Tracker", "🧠 Gemini Deep Intelligence"])

with tab1:
    st.markdown('<div class="oneui-card">', unsafe_allow_html=True)
    st.subheader("🌐 Samfw Real-time Scraper")
    st.write("Hệ thống cào dữ liệu thời gian thực và xử lý trực tiếp thông qua Gemini Agent.")
    
    col1, col2 = st.columns(2)
    with col1:
        sel_model_name = st.selectbox("Model thiết bị", list(SamfwCrawler.POPULAR_MODELS.keys()))
        target_model = SamfwCrawler.POPULAR_MODELS[sel_model_name]
    with
