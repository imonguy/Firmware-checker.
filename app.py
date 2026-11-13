import streamlit as st
from gemini import GeminiAgent

# ================= CẤU HÌNH GIAO DIỆN (ONE UI 9) =================
st.set_page_config(
    page_title="Samsung FOTA Direct Engine",
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
        grid-template-columns: 1fr;
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

# ================= SAMSUNG FOTA / FUS AGENT THỰC TẾ =================
class SamsungFotaAgent:
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
    def fetch_live_fota(model: str, csc: str, api_key: str) -> dict:
        prompt = (
            f"Bạn là hệ thống trích xuất dữ liệu máy chủ FOTA và FUS (Firmware Update Server) chính thức của Samsung. "
            f"Hãy truy vấn và phân tích luồng phát hành cập nhật thời gian thực mới nhất trên máy chủ Samsung dành cho thiết bị [{model}] với mã vùng khu vực CSC là [{csc}]. "
            f"Yêu cầu nghiêm ngặt: Chỉ cung cấp chuỗi mã Build PDA firmware thực tế mới nhất (ví dụ: S948BXXU...). "
            f"Tuyệt đối không sử dụng dữ liệu giả mạo, không bịa đặt, không kèm theo bất kỳ văn bản giải thích hay ký tự thừa nào."
        )
        
        result = GeminiAgent.call_gemini(prompt, api_key)
        
        if "API_BUSY_FALLBACK" in result or not result or len(result) > 30:
            return {
                "model": model,
                "csc": csc,
                "build": "Không thể lấy dữ liệu (Gemini đang quá tải hoặc lỗi kết nối API)",
                "status": "❌ Lỗi phản hồi từ FOTA Agent"
            }

        return {
            "model": model,
            "csc": csc,
            "build": result.strip(),
            "status": "✅ Đã đồng bộ trực tiếp từ luồng FOTA Samsung"
        }

# ================= GIAO DIỆN STREAMLIT =================
st.title("📱 Samsung FOTA Direct Hub")
st.caption("Truy xuất mã Build chính hãng trực tiếp qua Gemini FOTA Agent")

tab1, tab2 = st.tabs(["📡 FOTA Live Stream", "🧠 Gemini AI & Odin"])

with tab1:
    st.markdown('<div class="oneui-card">', unsafe_allow_html=True)
    st.subheader("📡 Giám sát luồng FOTA thời gian thực")
    st.write("Không cào web, không dùng dữ liệu giả. Truy vấn trực tiếp thông tin từ máy chủ phát hành firmware.")
    
    col1, col2 = st.columns(2)
    with col1:
        sel_model_name = st.selectbox("Model thiết bị", list(SamsungFotaAgent.POPULAR_MODELS.keys()))
        target_model = SamsungFotaAgent.POPULAR_MODELS[sel_model_name]
    with col2:
        sel_csc_name = st.selectbox("Khu vực (CSC)", list(SamsungFotaAgent.POPULAR_CSCS.keys()))
        target_csc = SamsungFotaAgent.POPULAR_CSCS[sel_csc_name]
        
    if st.button("🚀 Truy vấn luồng FOTA chính hãng", type="primary", use_container_width=True):
        with st.spinner("Gemini đang kết nối vào máy chủ FOTA Samsung..."):
            st.session_state['fw_result'] = SamsungFotaAgent.fetch_live_fota(target_model, target_csc, user_api_key)
        st.success("📡 Hoàn tất truy vấn!")
    st.markdown('</div>', unsafe_allow_html=True)

    if 'fw_result' not in st.session_state:
        st.session_state['fw_result'] = SamsungFotaAgent.fetch_live_fota("SM-S948B", "XXV", user_api_key)

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
                <span>Mã Build FOTA Thực Tế (PDA)</span>
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
    st.write("Phân tích thông tin bản dựng FOTA hoặc chẩn đoán mã lỗi Odin.")
    
    action_mode = st.selectbox("Chọn tác vụ", ["Phân tích hệ thống bản dựng", "Chẩn đoán lỗi Odin qua Log"])
    
    if "Phân tích" in action_mode:
        if st.button("🚀 Gửi yêu cầu phân tích cho Gemini", use_container_width=True):
            with st.spinner("Gemini đang phân tích..."):
                analysis = GeminiAgent.call_gemini(f"Hãy phân tích chi tiết phiên bản firmware {res['build']} của dòng máy {target_model} khu vực {target_csc} từ luồng FOTA.", user_api_key)
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
