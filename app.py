import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
from gemini import GeminiAgent

# ================= CẤU HÌNH GIAO DIỆN (ONE UI 9) =================
st.set_page_config(
    page_title="Samsung Firmware Hub - Gemini 3.8 AI",
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

# ================= CÀO DỮ LIỆU THỰC TẾ TỪ SAMFW KẾT HỢP GEMINI 3.8 =================
class SamfwLiveCrawler:
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
    @st.cache_data(ttl=180)
    def fetch_real_firmware(model: str, csc: str) -> dict:
        target_url = f"https://samfw.com/firmware/{model}/{csc}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Referer": "https://samfw.com/"
        }
        
        raw_text = ""
        extracted_build = None
        
        try:
            session = requests.Session()
            res = session.get(target_url, headers=headers, timeout=8)
            
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'html.parser')
                raw_text = soup.get_text(separator="\n", strip=True)[:15000]
                
                # Quét Regex tìm mã Build chuẩn
                model_short = model.replace("SM-", "")
                pattern = re.compile(rf"{model_short}[A-Z0-9]{{6,12}}", re.IGNORECASE)
                
                for tag in soup.find_all(['a', 'td', 'span', 'div', 'h3', 'p', 'b']):
                    match = pattern.search(tag.get_text())
                    if match and len(match.group(0)) >= 12:
                        extracted_build = match.group(0)
                        break
        except Exception as e:
            raw_text = f"Lỗi kết nối: {str(e)}"

        # Nếu cào thô bị chặn, giao toàn bộ cho Gemini 3.8 Flash phân tích truy xuất trực tiếp
        if not extracted_build or len(extracted_build
