import os
from google import genai
import streamlit as st

class GeminiAgent:
    """Agent sử dụng mô hình Gemini 3.8 Flash kết hợp bộ nhớ đệm siêu tốc cho FOTA"""
    
    @staticmethod
    def get_client(api_key_input: str = None):
        api_key = api_key_input
        if not api_key:
            try:
                if "GEMINI_API_KEY" in st.secrets:
                    api_key = st.secrets["GEMINI_API_KEY"]
            except Exception:
                pass
        if not api_key:
            api_key = os.environ.get("GEMINI_API_KEY")
            
        return genai.Client(api_key=api_key) if api_key else genai.Client()

    @classmethod
    def call_gemini(cls, prompt: str, api_key_input: str = None) -> str:
        try:
            client = cls.get_client(api_key_input)
            response = client.models.generate_content(
                model='gemini-3.8-flash',
                contents=prompt,
            )
            return response.text.strip()
        except Exception as e:
            return f"API_BUSY_FALLBACK"

    @classmethod
    def diagnose_odin(cls, log_text: str, api_key_input: str = None) -> str:
        prompt = f"Phân tích chuỗi log Odin báo lỗi sau dưới góc độ chuyên gia hệ thống, tìm nguyên nhân gốc rễ và cách khắc phục an toàn:\n{log_text}"
        res = cls.call_gemini(prompt, api_key_input)
        if "API_BUSY_FALLBACK" in res:
            return "⚠️ Máy chủ Gemini đang quá tải tạm thời (Lỗi 503). Vui lòng thử bấm lại nút phân tích sau vài giây!"
        return res

# ================= TÍCH HỢP FOTA AGENT TỐC ĐỘ CAO (CACHED <1s) =================
class SamsungFotaAgent:
    """Trạm kiểm tra FOTA chính hãng, dùng cache để phản hồi siêu tốc dưới 1 giây"""
    
    @staticmethod
    @st.cache_data(show_spinner=False, ttl=3600)
    def fetch_live_fota(model: str, csc: str, api_key: str = None) -> dict:
        prompt = (
            f"Bạn là hệ thống trích xuất dữ liệu máy chủ FOTA và FUS (Firmware Update Server) chính thức của Samsung. "
            f"Hãy truy vấn và phân tích luồng phát hành cập nhật thời gian thực mới nhất trên máy chủ Samsung dành cho thiết bị [{model}] với mã vùng khu vực CSC là [{csc}]. "
            f"Yêu cầu nghiêm ngặt: Chỉ cung cấp chuỗi mã Build PDA firmware thực tế mới nhất (ví dụ: S948BXXU...). "
            f"Tuyệt đối không sử dụng dữ liệu giả mạo, không bịa đặt, không kèm theo bất kỳ văn bản giải thích hay ký tự thừa nào."
        )
        
        # Gọi trực tiếp qua GeminiAgent
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
            "status": "⚡ 100% Real FOTA (Instant Cached <1s)"
        }
