import os
from google import genai
import streamlit as st

class GeminiAgent:
    """Agent sử dụng mô hình Gemini 3.8 Flash kết hợp cơ chế dự phòng thông minh"""
    
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
            # Nếu gặp lỗi quá tải 503 từ server, trả về thông báo gọn gàng để hệ thống tự chuyển cơ chế quét web
            return f"API_BUSY_FALLBACK"

    @classmethod
    def parse_samfw(cls, raw_text: str, model: str, csc: str, api_key_input: str = None) -> str:
        prompt = (
            f"Bạn là chuyên gia kỹ thuật phần cứng Samsung. Dưới đây là nội dung văn bản thô được cào từ trang Samfw cho thiết bị [{model}] với khu vực [{csc}]:\n\n"
            f"{raw_text}\n\n"
            "Nhiệm vụ: Phân tích kỹ nội dung trên, bóc tách và trả về CHÍNH XÁC 100% mã Build PDA firmware thực tế mới nhất.\n"
            "Yêu cầu nghiêm ngặt: Chỉ cung cấp chuỗi mã Build (ví dụ: S948BXXU...), không thêm giải thích rườm rà."
        )
        result = cls.call_gemini(prompt, api_key_input)
        return result

    @classmethod
    def diagnose_odin(cls, log_text: str, api_key_input: str = None) -> str:
        prompt = f"Phân tích chuỗi log Odin báo lỗi sau dưới góc độ chuyên gia hệ thống, tìm nguyên nhân gốc rễ và cách khắc phục an toàn:\n{log_text}"
        res = cls.call_gemini(prompt, api_key_input)
        if "API_BUSY_FALLBACK" in res:
            return "⚠️ Máy chủ Gemini đang quá tải tạm thời (Lỗi 503). Vui lòng thử bấm lại nút phân tích sau vài giây!"
        return res
