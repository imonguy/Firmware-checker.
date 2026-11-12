import streamlit as st
import requests
from bs4 import BeautifulSoup
from claude import ClaudeAPIClient

# ================= CẤU HÌNH GIAO DIỆN (ONE UI 9) =================
st.set_page_config(
    page_title="Samsung Firmware Hub - Modular Claude AI",
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

# ================= 1. CÀO DỮ LIỆU THÔ TỪ SAMFW =================
class SamfwFetcher:
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
    def get_raw_page_text(model: str, csc: str) -> str:
        target_url = f"https://samfw.com/firmware/{model}/{csc}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Referer": "https://samfw.com/"
        }
        try:
            res = requests.get(target_url, headers=headers, timeout=6)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'html.parser')
                return soup.get_text(separator="\n", strip=True)[:15000]
        except Exception as e:
            return f"Lỗi kết nối mạng: {str(e)}"
        return "Không thể truy xuất nội dung trang web."

# ================= 2. SIDEBAR CẤU HÌNH API KEY =================
st.sidebar.markdown("### ⚙️ Cấu hình Claude API")
user_api_key = st.sidebar.text_input("Nhập Anthropic API Key (sk-ant-...)", type="password", help="Khóa API cá nhân dùng để gọi Claude AI.")
st.sidebar.markdown("---")

if 'latest_build' not in st.session_state:
    st.session_state['latest_build'] = "Chưa quét dữ liệu (Nhấn nút bên dưới để bắt đầu)"

st.title("📱 Samsung Firmware Hub")
st.caption("Modular Samfw Crawler & Claude AI API")

tab1, tab2 = st.tabs(["🌐 Samfw AI Parser", "🧠 Claude Deep Intelligence"])

# --- TAB 1: CÀO & AI PHÂN TÍCH MÃ BUILD ---
with tab1:
    st.markdown('<div class="oneui-card">', unsafe_allow_html=True)
    st.subheader("🌐 Trí tuệ nhân tạo quét Samfw")
    st.write("Hệ thống cào nội dung Samfw và chuyển giao cho Claude API xử lý trích xuất thông minh.")
    
    col1, col2 = st.columns(2)
    with col1:
        sel_model_name = st.selectbox("Model thiết bị", list(SamfwFetcher.POPULAR_MODELS.keys()))
        target_model = SamfwFetcher.POPULAR_MODELS[sel_model_name]
    with col2:
        sel_csc_name = st.selectbox("Khu vực (CSC)", list(SamfwFetcher.POPULAR_CSCS.keys()))
        target_csc = SamfwFetcher.POPULAR_CSCS[sel_csc_name]
        
    if st.button("🚀 Quét & Phân tích bằng Claude AI", type="primary", use_container_width=True):
        with st.spinner("Đang kết nối Samfw và gọi Claude API phân tích..."):
            raw_text = SamfwFetcher.get_raw_page_text(target_model, target_csc)
            ai_result = ClaudeAPIClient.parse_samfw_firmware(user_api_key, raw_text, target_model, target_csc)
            st.session_state['latest_build'] = ai_result
        st.success("🎯 Hoàn tất xử lý dữ liệu thời gian thực!")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="oneui-card">
        <div>
            <span class="model-badge">{sel_model_name.split(' (')[0]} ({target_model})</span>
            <span class="csc-badge">{target_csc}</span>
        </div>
        <div style="clear: both;"></div>
        <div style="margin-top: 15px; background: #222630; padding: 16px; border-radius: 16px; font-size: 14px; line-height: 1.6;">
            <strong>Kết quả từ Claude API:</strong><br>
            {st.session_state['latest_build'].replace(chr(10), '<br>')}
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- TAB 2: CHUYÊN GIA PHÂN TÍCH & ODIN DOCTOR ---
with tab2:
    st.markdown('<div class="oneui-card">', unsafe_allow_html=True)
    st.subheader("🧠 Claude AI Master Brain")
    st.write("Đánh giá chuyên sâu bản dựng firmware hoặc chẩn đoán lỗi khi nạp qua Odin.")
    
    action_mode = st.selectbox("Chọn tác vụ", ["Đánh giá toàn diện phiên bản firmware", "Chẩn đoán lỗi Odin qua Log"])
    
    if "Đánh giá" in action_mode:
        custom_prompt = st.text_area("Yêu cầu cho Claude", value=f"Hãy phân tích mức độ ổn định và cải tiến bảo mật của bản dựng firmware cho thiết bị {target_model} khu vực {target_csc}.")
        if st.button("🚀 Gửi yêu cầu", type="primary", use_container_width=True):
            with st.spinner("Claude đang phân tích..."):
                resp = ClaudeAPIClient.call_claude(user_api_key, "Bạn là chuyên gia kỹ thuật phần mềm Samsung cao cấp.", custom_prompt)
            st.markdown(f"""
            <div style="background:#222630; padding:16px; border-radius:16px; margin-top:12px; font-size:13px; line-height: 1.6;">
                {resp.replace(chr(10), '<br>')}
            </div>
            """, unsafe_allow_html=True)
    else:
        log_input = st.text_area("Dán log Odin báo lỗi (FAIL!, Auth error...)")
        if st.button("🛠️ Claude Doctor Chẩn Đoán", type="primary", use_container_width=True):
            if not log_input.strip():
                st.warning("Vui lòng dán nội dung log Odin.")
            else:
                with st.spinner("Claude đang phân tích mã lỗi log..."):
                    diag = ClaudeAPIClient.diagnose_odin(user_api_key, log_input)
                st.markdown(f"""
                <div style="background:#222630; padding:16px; border-radius:16px; margin-top:12px; font-size:13px; line-height: 1.6;">
                    {diag.replace(chr(10), '<br>')}
                </div>
                """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
