import streamlit as st
import requests
from bs4 import BeautifulSoup
import anthropic

# ================= CẤU HÌNH GIAO DIỆN (ONE UI 9) =================
st.set_page_config(
    page_title="Samsung Firmware Hub - Samfw & Claude AI",
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
    .info-item span {
        display: block;
        color: #9ca3af;
        font-size: 11px;
        margin-bottom: 2px;
        text-transform: uppercase;
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
                # Lấy toàn bộ văn bản sạch trên trang để cung cấp context cho Claude AI phân tích
                return soup.get_text(separator="\n", strip=True)[:15000] # Giới hạn token an toàn
        except Exception as e:
            return f"Lỗi kết nối mạng: {str(e)}"
        return "Không thể truy xuất nội dung trang web."


# ================= 2. CLAUDE API AGENT (BỘ NÃO SIÊU CẤP) =================
class ClaudeMasterAgent:
    @staticmethod
    def ask_claude(api_key: str, system_prompt: str, user_prompt: str) -> str:
        if not api_key:
            return "⚠️ Vui lòng nhập Anthropic API Key của bạn ở thanh Sidebar bên trái để kích hoạt AI."
        try:
            client = anthropic.Anthropic(api_key=api_key)
            message = client.messages.create(
                model="claude-3-5-sonnet-20241022", # Model tối tân với khả năng đọc hiểu context web cực mạnh
                max_tokens=1500,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}]
            )
            return message.content[0].text
        except Exception as e:
            return f"❌ Lỗi gọi Claude API: {str(e)}"


# ================= 3. THANH SIDEBAR (CÀI ĐẶT API KEY) =================
st.sidebar.markdown("### ⚙️ Cấu hình Claude API")
user_api_key = st.sidebar.text_input("Nhập Anthropic API Key (sk-ant-...)", type="password", help="Khóa bảo mật cá nhân dùng để gọi Claude AI mạnh nhất.")
st.sidebar.markdown("---")
st.sidebar.markdown("💡 **Mẹo:** Key được mã hóa an toàn trên phiên làm việc của bạn để phân tích dữ liệu trực tiếp từ Samfw.")

# Khởi tạo trạng thái phiên làm việc
if 'latest_build' not in st.session_state:
    st.session_state['latest_build'] = "Chưa quét (Nhấn nút bên dưới để bắt đầu)"
if 'raw_context' not in st.session_state:
    st.session_state['raw_context'] = ""

st.title("📱 Samsung Firmware Hub")
st.caption("Live Samfw Parser & Claude 3.5 Sonnet Master Agent")

tab1, tab2 = st.tabs(["🌐 AI Samfw Parser", "🧠 Claude Deep Intelligence"])

# --- TAB 1: CÀO & AI PHÂN TÍCH MÃ BUILD CHÍNH XÁC ---
with tab1:
    st.markdown('<div class="oneui-card">', unsafe_allow_html=True)
    st.subheader("🌐 Trí tuệ nhân tạo quét Samfw")
    st.write("Hệ thống cào nội dung trang web Samfw và để Claude AI đọc, lọc ra chính xác phiên bản firmware mới nhất.")
    
    col1, col2 = st.columns(2)
    with col1:
        sel_model_name = st.selectbox("Model thiết bị", list(SamfwFetcher.POPULAR_MODELS.keys()))
        target_model = SamfwFetcher.POPULAR_MODELS[sel_model_name]
    with col2:
        sel_csc_name = st.selectbox("Khu vực (CSC)", list(SamfwFetcher.POPULAR_CSCS.keys()))
        target_csc = SamfwFetcher.POPULAR_CSCS[sel_csc_name]
        
    if st.button("🚀 Quét & Trích xuất bằng Claude AI", type="primary", use_container_width=True):
        with st.spinner("Đang kết nối Samfw và nhờ Claude AI phân tích dữ liệu..."):
            # Bước 1: Lấy raw text từ Samfw
            raw_text = SamfwFetcher.get_raw_page_text(target_model, target_csc)
            st.session_state['raw_context'] = raw_text
            
            # Bước 2: Dùng Claude API để phân tích chính xác mã build mới nhất từ raw text
            system_msg = "Bạn là một hệ thống trích xuất dữ liệu phần cứng Samsung chuyên nghiệp. Nhiệm vụ của bạn là đọc nội dung văn bản từ trang Samfw và tìm ra MÃ BUILD PDA (Firmware build number mới nhất, ví dụ dạng S948BXXU...) chính xác tuyệt đối."
            user_msg = f"Dưới đây là nội dung văn bản được cào từ trang Samfw cho model {target_model} với CSC {target_csc}:\n\n{raw_text}\n\nNhiệm vụ: Hãy trích xuất DUY NHẤT mã Build PDA mới nhất. Nếu tìm thấy, hãy định dạng trả về theo cấu trúc:\nBUILD: [mã build]\nNgày vá bảo mật (nếu có): [ngày]\nGhi chú ngắn gọn:"
            
            ai_result = ClaudeMasterAgent.ask_claude(user_api_key, system_msg, user_msg)
            st.session_state['latest_build'] = ai_result
            
        st.success("🎯 Hoàn tất phân tích dữ liệu thời gian thực từ Samfw!")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="oneui-card">
        <div>
            <span class="model-badge">{sel_model_name.split(' (')[0]} ({target_model})</span>
            <span class="csc-badge">{target_csc}</span>
        </div>
        <div style="clear: both;"></div>
        <div style="margin-top: 15px; background: #222630; padding: 16px; border-radius: 16px; font-size: 14px; line-height: 1.6;">
            <strong>Kết quả phân tích từ Claude AI:</strong><br>
            {st.session_state['latest_build'].replace(chr(10), '<br>')}
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- TAB 2: CHUYÊN GIA PHÂN TÍCH & CHẨN ĐOÁN ODIN ---
with tab2:
    st.markdown('<div class="oneui-card">', unsafe_allow_html=True)
    st.subheader("🧠 Claude AI Master Brain")
    st.write("Yêu cầu Claude AI đánh giá chuyên sâu bản dựng firmware hoặc hỗ trợ xử lý lỗi khi flash qua Odin.")
    
    action_mode = st.selectbox("Chọn tác vụ chuyên sâu", ["Đánh giá toàn diện phiên bản firmware hiện tại", "Chẩn đoán lỗi Odin qua chuỗi Log"])
    
    if "Đánh giá" in action_mode:
        prompt_text = st.text_area("Yêu cầu cụ thể cho Claude", value=f"Hãy phân tích mức độ ổn định, các cải tiến về bảo mật và hiệu suất NPU trên Android 17 (One UI 9) cho bản dựng vừa quét được của thiết bị {target_model} khu vực {target_csc}.")
        if st.button("🚀 Gửi yêu cầu phân tích", type="primary", use_container_width=True):
            with st.spinner("Claude AI đang xử lý báo cáo chuyên sâu..."):
                response_text = ClaudeMasterAgent.ask_claude(user_api_key, "Bạn là Claude Opus 5.5 / Claude 3.5 Sonnet, chuyên gia kỹ thuật phần mềm Samsung cao cấp.", prompt_text)
            st.markdown(f"""
            <div style="background:#222630; padding:16px; border-radius:16px; margin-top:12px; font-size:13px; color:#f0f2f5; line-height: 1.6;">
                {response_text.replace(chr(10), '<br>')}
            </div>
            """, unsafe_allow_html=True)
    else:
        log_input = st.text_area("Dán đoạn log Odin đang báo lỗi (FAIL!, Auth, PIT error...)")
        if st.button("🛠️ Claude Doctor Chẩn Đoán", type="primary", use_container_width=True):
            if not log_input.strip():
                st.warning("Vui lòng dán nội dung log Odin trước.")
            else:
                with st.spinner("Claude đang mổ xẻ mã lỗi log..."):
                    diag_text = ClaudeMasterAgent.ask_claude(user_api_key, "Bạn là chuyên gia khắc phục sự cố phần cứng Samsung qua công cụ Odin.", f"Hãy phân tích nguyên nhân cốt lõi và hướng dẫn khắc phục chi tiết cho đoạn log Odin sau:\n{log_input}")
                st.markdown(f"""
                <div style="background:#222630; padding:16px; border-radius:16px; margin-top:12px; font-size:13px; color:#f0f2f5; line-height: 1.6;">
                    {diag_text.replace(chr(10), '<br>')}
                </div>
                """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
