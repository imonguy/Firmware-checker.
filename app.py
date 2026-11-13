import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
from gemini import GeminiAgent

# ================= CẤU HÌNH GIAO DIỆN (ONE UI 9) =================
st.set_page_config(
    page_title="Samsung Firmware Hub - Pure Real Scraper",
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

# ================= SIDEBAR CẤU HÌNH API KEY =================
st.sidebar.markdown("### ⚙️ Cấu hình Gemini API")
user_api_key = st.sidebar.text_input(
    "Nhập Gemini API Key", 
    type="password", 
    help="Lấy key miễn phí tại aistudio.google.com"
)
st.sidebar.markdown("---")

# ================= HỆ THỐNG CÀO DỮ LIỆU THẬT 100% =================
class PureSamfwScraper:
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
    def scrape_real_build(model: str, csc: str) -> dict:
        target_url = f"https://samfw.com/firmware/{model}/{csc}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Referer": "https://samfw.com/"
        }
        
        extracted_build = None
        status_msg = "Thành công (Real Scraped)"
        
        try:
            session = requests.Session()
            res = session.get(target_url, headers=headers, timeout=5)
            
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'html.parser')
                model_short = model.replace("SM-", "")
                
                # Quét tìm kiếm cấu trúc mã build chuẩn thực tế trên trang
                for tag in soup.find_all(['a', 'td', 'span', 'div', 'h3', 'p', 'b']):
                    text = tag.get_text().strip()
                    matches = re.findall(rf"\b({model_short}[A-Z0-9]{{8,12}})", text)
                    if matches:
                        extracted_build = matches[0]
                        break
            elif res.status_code == 403:
                status_msg = "⚠️ Bị Cloudflare chặn (403 Forbidden)"
            else:
                status_msg = f"⚠️ Lỗi HTTP {res.status_code}"
                
        except requests.exceptions.Timeout:
            status_msg = "⚠️ Quá thời gian kết nối (Timeout)"
        except Exception as e:
            status_msg = f"❌ Lỗi: {str(e)}"

        # TUYỆT ĐỐI KHÔNG DÙNG GIÁ TRỊ GIẢ. Nếu không cào được, trả về thông báo rõ ràng để nắm tình hình.
        if not extracted_build:
            extracted_build = "Không thể cào (IP Server bị Samfw Cloudflare chặn)"

        return {
            "model": model,
            "csc": csc,
            "build": extracted_build,
            "status": status_msg
        }

# ================= GIAO DIỆN STREAMLIT =================
st.title("📱 Samsung Firmware Hub")
st.caption("Pure Real-time Samfw Scraper (No Fake Data)")

tab1, tab2 = st.tabs(["🌐 Pure Real Scraper", "🧠 Deep Intelligence & Odin"])

with tab1:
    st.markdown('<div class="oneui-card">', unsafe_allow_html=True)
    st.subheader("🌐 Cào dữ liệu thực tế từ Samfw")
    st.write("Truy xuất trực tiếp mã build gốc. Không sử dụng dữ liệu dự phòng hay dữ liệu giả.")
    
    col1, col2 = st.columns(2)
    with col1:
        sel_model_name = st.selectbox("Model thiết bị", list(PureSamfwScraper.POPULAR_MODELS.keys()))
        target_model = PureSamfwScraper.POPULAR_MODELS[sel_model_name]
    with col2:
        sel_csc_name = st.selectbox("Khu vực (CSC)", list(PureSamfwScraper.POPULAR_CSCS.keys()))
        target_csc = PureSamfwScraper.POPULAR_CSCS[sel_csc_name]
        
    if st.button("🚀 Thực hiện cào dữ liệu thật", type="primary", use_container_width=True):
        with st.spinner("Đang gửi yêu cầu cào dữ liệu thực tế từ Samfw..."):
            st.session_state['fw_result'] = PureSamfwScraper.scrape_real_build(target_model, target_csc)
        st.success("🌐 Đã hoàn tất quá trình quét!")
    st.markdown('</div>', unsafe_allow_html=True)

    if 'fw_result' not in st.session_state:
        st.session_state['fw_result'] = PureSamfwScraper.scrape_real_build("SM-S948B", "XXV")

    res = st.session_state['fw_result']
    st.markdown(f"""
    <div class="oneui-card">
        <div>
            <span class="model-badge">{sel_model_name.split(' (')[0]} ({res['model']})</span>
            <span class="csc-badge">{res['csc']}</span>
        </div>
        <div style="clear: both;"></div>
        <div class="info-grid">
            <div class="info-item">
                <span>Mã Build Thực Tế (PDA)</span>
                <strong>{res['build']}</strong>
            </div>
            <div class="info-item">
                <span>Trạng thái kết nối</span>
                <strong class="agent-status">{res['status']}</strong>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="oneui-card">', unsafe_allow_html=True)
    st.subheader("🧠 Gemini Master Brain")
    st.write("Phân tích thông tin hoặc chẩn đoán mã lỗi Odin.")
    
    action_mode = st.selectbox("Chọn tác vụ", ["Phân tích hệ thống", "Chẩn đoán lỗi Odin qua Log"])
    
    if "Phân tích" in action_mode:
        if st.button("🚀 Gửi yêu cầu phân tích cho Gemini", use_container_width=True):
            with st.spinner("Gemini đang phân tích..."):
                analysis = GeminiAgent.call_gemini(f"Hãy phân tích chi tiết phiên bản firmware {res['build']} của dòng máy {target_model} khu vực {target_csc}.", user_api_key)
            st.markdown(f"""
            <div style="background:#222630; padding:16px; border-radius:16px; margin-top:12px; font-size:13px; line-height: 1.6;">
                {analysis.replace(chr(10), '<br>')}
            </div>
            """, unsafe_allow_html=True)
    else:
        log_input = st.text_area("Dán nội dung log Odin báo lỗi (FAIL!, Auth, PIT error...)")
        if st.button("🛠️ Gemini Doctor Chẩn Đoán", use_container_width=True):
            if not log_input.strip():
                st.warning("Vui lòng dán chuỗi log Odin trước.")
            else:
                with st.spinner("Gemini đang mổ xẻ mã lỗi..."):
                    diag = GeminiAgent.diagnose_odin(log_input, user_api_key)
                st.markdown(f"""
                <div style="background:#222630; padding:16px; border-radius:16px; margin-top:12px; font-size:13px; line-height: 1.6;">
                    {diag.replace(chr(10), '<br>')}
                </div>
                """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
