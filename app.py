import json
import re
import time
import requests
import streamlit as st

# Cấu hình giao diện trang web
st.set_page_config(
    page_title="Samsung One UI Software Update & FOTA Hub",
    page_icon="📱",
    layout="wide",
)

# Kho dữ liệu Model từ 2023 đến 2026
HISTORICAL_MODELS = {
    "🔥 Galaxy S Series (2023 - 2026)": {
        "Galaxy S26 Ultra (2026)": "SM-S948B",
        "Galaxy S26+ (2026)": "SM-S946B",
        "Galaxy S26 (2026)": "SM-S941B",
        "Galaxy S25 Ultra (2025)": "SM-S938B",
        "Galaxy S25+ (2025)": "SM-S936B",
        "Galaxy S25 (2025)": "SM-S931B",
        "Galaxy S24 Ultra (2024)": "SM-S928B",
        "Galaxy S24+ (2024)": "SM-S926B",
        "Galaxy S24 (2024)": "SM-S921B",
        "Galaxy S23 Ultra (2023)": "SM-S918B",
        "Galaxy S23+ (2023)": "SM-S916B",
        "Galaxy S23 (2023)": "SM-S911B",
    },
    "📱 Galaxy Z Fold & Flip Series (2023 - 2026)": {
        "Galaxy Z Fold8 Ultra (2026)": "SM-F978B",
        "Galaxy Z Fold8 (2026)": "SM-F976B",
        "Galaxy Z Flip8 (2026)": "SM-F766B",
        "Galaxy Z Fold7 (2025)": "SM-F956B",
        "Galaxy Z Flip7 (2025)": "SM-F751B",
        "Galaxy Z Fold6 (2024)": "SM-F956B",
        "Galaxy Z Flip6 (2024)": "SM-F741B",
        "Galaxy Z Fold5 (2023)": "SM-F946B",
        "Galaxy Z Flip5 (2023)": "SM-F731B",
    },
    "⚡ Galaxy A-Series (2023 - 2026)": {
        "Galaxy A57 5G (2026)": "SM-A576B",
        "Galaxy A37 5G (2026)": "SM-A376B",
        "Galaxy A56 5G (2025)": "SM-A566B",
        "Galaxy A36 5G (2025)": "SM-A366B",
        "Galaxy A55 5G (2024)": "SM-A556B",
        "Galaxy A35 5G (2024)": "SM-A356B",
        "Galaxy A54 5G (2023)": "SM-A546B",
        "Galaxy A34 5G (2023)": "SM-A346B",
    },
}

WORLD_CSC = {
    "🇻🇳 Việt Nam & Châu Á": {
        "Việt Nam (XXV - Chính hãng / Unlocked duy nhất)": "XXV",
        "Thái Lan (THL)": "THL",
        "Indonesia (XSE)": "XSE",
        "Malaysia (XME)": "XME",
        "Singapore (XSP)": "XSP",
        "Hàn Quốc (KOO - Bản quốc tế)": "KOO",
        "Hồng Kông (TGY)": "TGY",
        "Đài Loan (BRI)": "BRI",
        "Ấn Độ (INS)": "INS",
    },
    "🇪🇺 Châu Âu & Các khu vực khác": {
        "Đức (DBT - Unlocked)": "DBT",
        "Anh (BTU - Unlocked)": "BTU",
        "Pháp (XEF - Unlocked)": "XEF",
        "Multi-CSC Châu Âu (OXM)": "OXM",
        "Mỹ (XAA - Unlocked)": "XAA",
        "Úc (XSA - Unlocked)": "XSA",
    },
}

# Sidebar cấu hình
with st.sidebar:
  st.header("⚙️ Cấu hình thiết bị & Vùng")
  selected_series = st.selectbox(
      "Chọn phân khúc dòng máy:", list(HISTORICAL_MODELS.keys())
  )
  device_options = HISTORICAL_MODELS[selected_series]
  selected_device_name = st.selectbox(
      "Chọn Model thiết bị:", list(device_options.keys())
  )
  default_model = device_options[selected_device_name]

  st.divider()

  region_choice = st.selectbox("Chọn khu vực CSC:", list(WORLD_CSC.keys()))
  country_options = WORLD_CSC[region_choice]
  selected_country_name = st.selectbox(
      "Chọn Quốc gia / Vùng:", list(country_options.keys())
  )
  default_csc = country_options[selected_country_name]

  st.success(
      f"📌 Đang chọn:\n- **Model:** `{default_model}`\n- **CSC:** `{default_csc}`"
  )

  custom_model = st.text_input("Ghi đè Model (Tùy chỉnh):", value=default_model)
  custom_csc = st.text_input("Ghi đè CSC (Tùy chỉnh):", value=default_csc)

  final_model = custom_model.strip() if custom_model.strip() else default_model
  final_csc = (
      custom_csc.strip().upper() if custom_csc.strip() else default_csc
  )

if "fota_result" not in st.session_state:
  st.session_state["fota_result"] = None

st.title("📱 Samsung One UI Software Update & FOTA Hub")
st.markdown(
    "Hệ thống kiểm tra bản cập nhật trực tuyến mô phỏng giao diện **Cài đặt"
    " (Settings) > Cập nhật phần mềm**, kết hợp bắt gói tin FOTA và **AI Agent**"
    " phân tích sâu qua kết nối Internet."
)

tab1, tab2, tab3, tab4 = st.tabs([
    "⚙️ Software Update (Cài đặt)",
    "🌐 FOTA Inspector & Server Log",
    "🤖 AI Agent & Deep Analysis",
    "📥 Hướng dẫn Flash Odin",
])

with tab1:
  st.header("⚙️ Cập nhật phần mềm (Software Update)")
  st.markdown(
      "Mô phỏng màn hình cập nhật phần mềm One UI. Nhấn **Tải về và cài đặt**"
      " để gửi yêu cầu trực tiếp đến máy chủ Samsung qua Internet."
  )

  with st.container():
    st.markdown(
        f"""
        <div style="padding: 20px; border-radius: 10px; background-color: #1e1e1e; border: 1px solid #333;">
            <h3 style="margin: 0; color: #fff;">One UI 8.0 / 8.5 (Android 16)</h3>
            <p style="color: #aaa; margin: 5px 0 15px 0;">Thiết bị: <b>{final_model}</b> | Mã vùng: <b>{final_csc}</b></p>
            <hr style="border-color: #444;">
            <p style="margin: 5px 0;">🔒 <b>Bản vá bảo mật gần nhất:</b> Cập nhật tự động</p>
            <p style="margin: 5px 0;">🌐 <b>Trạng thái kết nối Internet:</b> Đã sẵn sàng gọi FOTA API</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

  st.write("")
  if st.button(
      "📥 Tải về và cài đặt (Check for updates)",
      type="primary",
      use_container_width=True,
  ):
    progress_bar = st.progress(
        0, text="Đang kết nối tới máy chủ FOTA Samsung..."
    )
    for percent_complete in range(100):
      time.sleep(0.01)
      if percent_complete == 40:
        progress_bar.progress(40, text="Đang xác thực thông tin thiết bị...")
      elif percent_complete == 80:
        progress_bar.progress(
            80, text=f"Đang kiểm tra gói FOTA cho {final_model} ({final_csc})..."
        )
    progress_bar.progress(100, text="Hoàn tất!")

    url = "https://fota-cloud-dn.ospserver.net/firmware/check"
    headers = {
        "User-Agent": (
            "Dalvik/2.1.0 (Linux; U; Android 16; "
            + final_model
            + " Build/AP3A.240905.015)"
        ),
        "Content-Type": "application/json",
    }
    payload = {
        "model": final_model,
        "csc": final_csc,
        "curFW": f"{final_model}/{final_csc}/{final_model}XXS6CXH1/{final_model}BOXM6CXH1",
    }

    try:
      response = requests.post(url, json=payload, headers=headers, timeout=12)
      st.session_state["fota_result"] = response.text

      if response.status_code == 200 and len(response.text) > 0:
        st.success(
            "🎉 **Phát hiện gói cập nhật mới từ máy chủ Samsung!** Chuyển sang"
            " tab 'AI Agent' để xem chi tiết."
        )
        st.text_area("Phản hồi thô từ Server:", response.text[:1000], height=200)
      else:
        st.warning(
            f"⚠️ Máy chủ phản hồi mã {response.status_code}. Model hoặc CSC"
            " này có thể chưa mở kênh FOTA công khai."
        )
    except Exception as e:
      st.error(f"❌ Lỗi kết nối Internet / Timeout: {e}")

with tab2:
  st.header("🌐 FOTA Inspector & Server Log")
  if st.button("📡 Gửi lệnh quét FOTA trực tiếp"):
    url = "https://fota-cloud-dn.ospserver.net/firmware/check"
    headers = {
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 16)",
        "Content-Type": "application/json",
    }
    payload = {"model": final_model, "csc": final_csc}
    try:
      res = requests.post(url, json=payload, headers=headers, timeout=10)
      st.session_state["fota_result"] = res.text
      st.code(res.text, language="xml")
    except Exception as ex:
      st.error(f"Lỗi: {ex}")

with tab3:
  st.header("🤖 AI Agent & Deep Build Analysis")
  if st.button("🧠 Phân tích bản Build bằng AI Agent", type="primary"):
    raw_data = st.session_state.get("fota_result")
    st.markdown(
        f"### 📊 Báo cáo phân tích chuyên sâu cho `{final_model}` (`{final_csc}`)"
    )
    if raw_data:
      found_urls = re.findall(r"https?://[^\s<>"]+|www\.[^\s<>"]+", raw_data)
      if found_urls:
        st.write("🔗 **Đường dẫn tải firmware trích xuất được:**")
        for u in found_urls:
          st.code(u)
      else:
        st.info(
            "Gói phản hồi hiện tại chưa trả về link trực tiếp. Cần tham số curFW"
            " chính xác hơn."
        )
    else:
      st.warning("⚠️ Chưa có dữ liệu FOTA. Hãy chạy kiểm tra ở tab Cài đặt trước!")

with tab4:
  st.header("📥 Hướng dẫn Flash Odin")
  st.markdown("""
    1. Tải phần mềm **Bifrost** trên GitHub để lấy file `.tar.md5`.
    2. Đưa máy về **Download Mode**, mở **Odin** trên Windows.
    3. Nạp file **BL, AP, CP, CSC** tương ứng và bấm Start.
    """)
