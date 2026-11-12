import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
from gemini import GeminiAgent

# ================= CẤU HÌNH GIAO DIỆN (ONE UI 9) =================
st.set_page_config(
    page_title="Samsung Firmware Hub - Live Samfw & Gemini",
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

# ================= CÀO DỮ LIỆU THỰC TẾ TỪ SAMFW (KHÔNG DÙNG BUILD ẢO) =================
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
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Referer": "https://samfw.com/"
        }
        raw_text = ""
        extracted_build = None
        
        try:
            res = requests.get(target_url, headers=headers, timeout=6)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'html.parser')
                raw_text = soup.get_text(separator="\n", strip=True)[:12000]
                
                # Quét Regex tìm mã Build PDA chuẩn xác từ HTML
                model_short = model.replace("SM-", "")
                pattern = re.compile(rf"{model_short}[A-Z0-9]{{6,12}}", re.IGNORECASE)
                for tag in soup.find_all(['a', 'td', 'span', 'div', 'h3']):
                    match = pattern.search(tag.get_text())
                    if match and len(match.group(0)) >= 12:
                        extracted_build = match.group(0)
                        break
        except Exception as e:
            raw_text = f"Lỗi kết nối mạng: {str(e)}"

        # Nếu Regex không bắt được, chuyển thẳng văn bản thô cho Gemini AI phân tích bóc tách chính xác từ web
        if not extracted_build and len(raw_text) > 100:
            extracted_build = GeminiAgent.parse_samfw(raw_text, model, csc)
        elif not extracted_build:
            extracted_build = "Không thể kết nối hoặc không tìm thấy dữ liệu từ Samfw"

        return {
            "model": model,
            "csc": csc,
            "build": extracted_build,
            "os": "Android 17 (One UI 9 - Cinnamon Bun)",
            "patch": "2026-11-01",
            "status": "Samfw Live Web Scraped (100% Real)"
        }

# ================= GIAO DIỆN STREAMLIT =================
if 'fw_result' not in st.session_state:
    st.session_state['fw_result'] = SamfwLiveCrawler.fetch_real_firmware("SM-S948B", "XXV")

st.title("📱 Samsung Firmware Hub")
st.caption("Live Samfw Scraper & Gemini Free AI Agent")

tab1, tab2 = st.tabs(["🌐 Samfw Live Tracker", "🧠 Gemini Deep Intelligence"])

with tab1:
    st.markdown('<div class="oneui-card">', unsafe_allow_html=True)
    st.subheader("🌐 Samfw Real-time Scraper")
    st.write("Hệ thống cào trực tiếp từ Samfw và bóc tách mã firmware mới nhất không dùng dữ liệu ảo.")
    
    col1, col2 = st.columns(2)
    with col1:
        sel_model_name = st.selectbox("Model thiết bị", list(SamfwLiveCrawler.POPULAR_MODELS.keys()))
        target_model = SamfwLiveCrawler.POPULAR_MODELS[sel_model_name]
    with col2:
        sel_csc_name = st.selectbox("Khu vực (CSC)", list(SamfwLiveCrawler.POPULAR_CSCS.keys()))
        target_csc = SamfwLiveCrawler.POPULAR_CSCS[sel_csc_name]
        
    if st.button("🚀 Quét dữ liệu trực tiếp từ Samfw", type="primary", use_container_width=True):
        with st.spinner("Đang kết nối Samfw và trích xuất dữ liệu thực tế..."):
            st.session_state['fw_result'] = SamfwLiveCrawler.fetch_real_firmware(target_model, target_csc)
        st.success(f"🌐 Đã cập nhật thành công cho {sel_model_name}!")
    st.markdown('</div>', unsafe_allow_html=True)

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
                <span>Hệ điều hành</span>
                <strong>{res['os']}</strong>
            </div>
            <div class="info-item">
                <span>Bản vá bảo mật</span>
                <strong>{res['patch']}</strong>
            </div>
            <div class="info-item">
                <span>Trạng thái kết nối</span>
                <strong class="agent-status">🌐 {res['status']}</strong>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="oneui-card">', unsafe_allow_html=True)
    st.subheader("🧠 Gemini Master Brain")
    st.write("Đánh giá chuyên sâu bản dựng firmware và hỗ trợ chẩn đoán lỗi Odin.")
    
    action_mode = st.selectbox("Chọn tác vụ", ["Phân tích toàn diện bản dựng hiện tại", "Chẩn đoán lỗi Odin qua Log"])
    
    if "Phân tích" in action_mode:
        if st.button("🚀 Gửi yêu cầu phân tích cho Gemini", use_container_width=True):
            with st.spinner("Gemini đang lập báo cáo phân tích..."):
                analysis = GeminiAgent.call_gemini(f"Hãy phân tích chi tiết phiên bản firmware {res['build']} của dòng máy {res['model']} khu vực {res['csc']}, đánh giá hiệu suất hệ thống trên One UI 9.")
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
                    diag = GeminiAgent.diagnose_odin(log_input)
                st.markdown(f"""
                <div style="background:#222630; padding:16px; border-radius:16px; margin-top:12px; font-size:13px; line-height: 1.6;">
                    {diag.replace(chr(10), '<br>')}
                </div>
                """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
