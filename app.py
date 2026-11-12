import streamlit as st
from gemini import GeminiAgent

# ================= CẤU HÌNH GIAO DIỆN (ONE UI 9) =================
st.set_page_config(
    page_title="Samsung Firmware Hub - Direct Samfw & Gemini",
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

# ================= DANH MỤC THIẾT BỊ =================
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

# ================= GIAO DIỆN STREAMLIT =================
st.title("📱 Samsung Firmware Hub")
st.caption("Samfw Direct Access & Gemini AI Agent")

tab1, tab2 = st.tabs(["🌐 Samfw Direct Hub", "🧠 Deep Intelligence & Odin"])

with tab1:
    st.markdown('<div class="oneui-card">', unsafe_allow_html=True)
    st.subheader("🌐 Truy cập nhanh Samfw chính chủ")
    st.write("Chọn thiết bị và khu vực để mở thẳng trang dữ liệu gốc trên Samfw với độ chính xác tuyệt đối 100%.")
    
    col1, col2 = st.columns(2)
    with col1:
        sel_model_name = st.selectbox("Model thiết bị", list(POPULAR_MODELS.keys()))
        target_model = POPULAR_MODELS[sel_model_name]
    with col2:
        sel_csc_name = st.selectbox("Khu vực (CSC)", list(POPULAR_CSCS.keys()))
        target_csc = POPULAR_CSCS[sel_csc_name]
        
    # Tạo đường link trực tiếp chính xác đến samfw
    samfw_direct_url = f"https://samfw.com/firmware/{target_model}/{target_csc}"
    
    st.markdown("<br>", unsafe_allow_html=True)
    # Nút bấm mở thẳng trang Samfw trong tab mới
    st.link_button("🔗 Mở trực tiếp trang Samfw của máy này", samfw_direct_url, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="oneui-card">
        <div>
            <span class="model-badge">{sel_model_name.split(' (')[0]} ({target_model})</span>
            <span class="csc-badge">{target_csc}</span>
        </div>
        <div style="clear: both;"></div>
        <div class="info-grid">
            <div class="info-item">
                <span>Nguồn dữ liệu</span>
                <strong>Samfw.com (Real-time)</strong>
            </div>
            <div class="info-item">
                <span>Hệ điều hành</span>
                <strong>Android 17 (One UI 9)</strong>
            </div>
            <div class="info-item">
                <span>Bảo mật</span>
                <strong>Mới nhất từ Samsung</strong>
            </div>
            <div class="info-item">
                <span>Trạng thái kết nối</span>
                <strong class="agent-status">⚡ Sẵn sàng kiểm tra</strong>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="oneui-card">', unsafe_allow_html=True)
    st.subheader("🧠 Gemini Master Brain")
    st.write("Hỗ trợ phân tích thông tin phiên bản hoặc chẩn đoán mã lỗi Odin.")
    
    action_mode = st.selectbox("Chọn tác vụ", ["Phân tích hệ thống One UI 9", "Chẩn đoán lỗi Odin qua Log"])
    
    if "Phân tích" in action_mode:
        build_input = st.text_input("Nhập mã Build bạn vừa xem trên Samfw (VD: S948BXXU3...)")
        if st.button("🚀 Gửi yêu cầu phân tích cho Gemini", use_container_width=True):
            if not build_input.strip():
                st.warning("Vui lòng nhập mã build từ Samfw trước.")
            else:
                with st.spinner("Gemini đang lập báo cáo phân tích..."):
                    analysis = GeminiAgent.call_gemini(f"Hãy phân tích chi tiết phiên bản firmware {build_input} của dòng máy {target_model} khu vực {target_csc}, đánh giá hiệu suất hệ thống trên One UI 9.", user_api_key)
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
