import streamlit as st
from stellar_engine import StellarEngine
from claude_agent import ClaudeAgent

# Cấu hình trang
st.set_page_config(
    page_title="Samsung Firmware Hub",
    page_icon="📱",
    layout="centered"
)

# Giao diện CSS chuẩn One UI 9 (Cinnamon Bun Dark Theme)
st.markdown("""
<style>
    .stApp {
        background-color: #0b0c0e;
        color: #f0f2f5;
    }
    .oneui-card {
        background: #181a20;
        border-radius: 24px;
        padding: 20px;
        margin-bottom: 16px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
    }
    .model-badge {
        font-size: 18px;
        font-weight: 700;
        color: #ffffff;
    }
    .csc-tag {
        background: rgba(46, 107, 255, 0.15);
        color: #2e6bff;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 600;
        float: right;
    }
    .info-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 10px;
        background: #222630;
        padding: 14px;
        border-radius: 18px;
        margin-top: 14px;
        font-size: 13px;
    }
    .info-item span {
        display: block;
        color: #9ca3af;
        font-size: 11px;
        margin-bottom: 2px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .ai-badge-stellar {
        color: #10b981;
        font-weight: 600;
    }
    .pricing-card {
        background: linear-gradient(135deg, #181a20, #222630);
        border: 1px solid rgba(168, 85, 247, 0.3);
        border-radius: 20px;
        padding: 18px;
        margin-bottom: 12px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Khởi tạo session state lưu dữ liệu firmware thông qua StellarEngine
if 'firmware_data' not in st.session_state:
    st.session_state['firmware_data'] = StellarEngine.parse_payload("SM-S928B", "XXV", "")

# Tiêu đề ứng dụng
st.title("📱 Samsung Firmware Hub")
st.caption("Multi-Agent Architecture | Stellar AI + Claude Master Brain")

# Điều hướng Tabs chuẩn One UI
tab1, tab2, tab3 = st.tabs(["🔍 Tra cứu & Stellar", "🧠 Claude Deep Agent", "💎 Gói Premium"])

# ================= TAB 1: TRA CỨU & STELLAR AI =================
with tab1:
    st.markdown('<div class="oneui-card">', unsafe_allow_html=True)
    st.subheader("⚡ Stellar AI Fast Parser")
    st.write("Xử lý dữ liệu thô an toàn, chống lỗi 403 từ Samsung FOTA.")
    
    col1, col2 = st.columns(2)
    with col1:
        model_input = st.text_input("Model thiết bị", value="SM-S928B")
    with col2:
        csc_input = st.text_input("Mã vùng CSC", value="XXV")
        
    raw_payload = st.text_area("Dán FOTA Payload thô (tùy chọn)", placeholder="Dữ liệu JSON/XML từ nguồn cộng đồng...")
    
    if st.button("⚡ Chạy Stellar AI Parse", type="primary", use_container_width=True):
        # Gọi module stellar_engine.py để xử lý
        st.session_state['firmware_data'] = StellarEngine.parse_payload(model_input, csc_input, raw_payload)
        st.success("⚡ Stellar AI đã bóc tách và lập chỉ mục thành công!")
    st.markdown('</div>', unsafe_allow_html=True)

    # Hiển thị kết quả dạng One UI Card
    fw = st.session_state['firmware_data']
    st.markdown(f"""
    <div class="oneui-card">
        <div>
            <span class="model-badge">Galaxy S24 Ultra ({fw['model']})</span>
            <span class="csc-tag">{fw['csc']} / Vietnam</span>
        </div>
        <div style="clear: both;"></div>
        <div class="info-grid">
            <div class="info-item">
                <span>Mã Build (PDA)</span>
                <strong>{fw['build']}</strong>
            </div>
            <div class="info-item">
                <span>Hệ điều hành</span>
                <strong>{fw['os']}</strong>
            </div>
            <div class="info-item">
                <span>Bản vá bảo mật</span>
                <strong>{fw['patch']}</strong>
            </div>
            <div class="info-item">
                <span>Trạng thái xử lý</span>
                <strong class="ai-badge-stellar">⚡ {fw['status']}</strong>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ================= TAB 2: CLAUDE DEEP AGENT =================
with tab2:
    st.markdown('<div class="oneui-card">', unsafe_allow_html=True)
    st.subheader("🧠 Claude Master Brain (PRO)")
    st.write("Sử dụng module Claude Agent để phân tích chuyên sâu.")
    
    agent_mode = st.selectbox(
        "Chọn tác vụ phân tích chuyên sâu",
        ["Dịch & Tóm tắt Changelog One UI 9", "Chẩn đoán lỗi Odin qua Log file"]
    )
    
    if "Changelog" in agent_mode:
        changelog_input = st.text_area("Nhãn Changelog gốc từ Samsung", value="[One UI 9.0 Update]\n- Enhanced Cinnamon Bun transition animations.\n- Advanced on-device AI object segmentation.")
        if st.button("🚀 Kích hoạt Claude Dịch Changelog", use_container_width=True):
            result = ClaudeAgent.analyze_changelog(changelog_input)
            st.markdown(f"""
            <div style="background:#222630; padding:16px; border-radius:16px; margin-top:12px; font-size:13px; color:#f0f2f5;">
                {result.replace(chr(10), '<br>')}
            </div>
            """, unsafe_allow_html=True)
    else:
        odin_log_input = st.text_area("Dán nội dung log Odin lỗi", placeholder="Ví dụ: FAIL! Auth, PIT mismatch...")
        if st.button("🛠️ Kích hoạt Claude Doctor", use_container_width=True):
            result = ClaudeAgent.diagnose_odin_log(odin_log_input)
            st.markdown(f"""
            <div style="background:#222630; padding:16px; border-radius:16px; margin-top:12px; font-size:13px; color:#f0f2f5;">
                {result.replace(chr(10), '<br>')}
            </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ================= TAB 3: GÓI PREMIUM (THÁNG / NĂM) =================
with tab3:
    st.markdown('<div class="oneui-card">', unsafe_allow_html=True)
    st.subheader("💎 Nâng cấp Tài khoản Pro")
    st.write("Mở khóa toàn bộ sức mạnh của Claude Deep Agent.")
    
    col_p1, col_p2 = st.columns(2)
    
    with col_p1:
        st.markdown("""
        <div class="pricing-card">
            <h3>Gói Tháng</h3>
            <p style="font-size:22px; font-weight:700; color:#a855f7; margin:10px 0;">30.000đ</p>
            <p style="font-size:12px; color:#9ca3af;">Thanh toán linh hoạt.<br>Hủy bất cứ lúc nào.</p>
            <br>
            <button style="width:100%; background:#2e6bff; border:none; color:white; padding:10px; border-radius:12px; font-weight:600; cursor:pointer;">Đăng ký Tháng</button>
        </div>
        """, unsafe_allow_html=True)
        
    with col_p2:
        st.markdown("""
        <div class="pricing-card" style="border-color: #2e6bff;">
            <h3>Gói Năm <span style="font-size:11px; background:#2e6bff; padding:2px 6px; border-radius:6px;">Tiết kiệm 30%</span></h3>
            <p style="font-size:22px; font-weight:700; color:#2e6bff; margin:10px 0;">250.000đ</p>
            <p style="font-size:12px; color:#9ca3af;">Dùng trọn vẹn cả năm.<br>Ưu tiên tốc độ cao.</p>
            <br>
            <button style="width:100%; background:linear-gradient(135deg, #7c3aed, #db2777); border:none; color:white; padding:10px; border-radius:12px; font-weight:600; cursor:pointer;">Đăng ký Năm</button>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("<p style='text-align:center; font-size:11px; color:#6b7280; margin-top:20px;'>Samsung Firmware Hub Pre-Alpha 2 — Modular Python Architecture</p>", unsafe_allow_html=True)
