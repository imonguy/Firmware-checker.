import os
from google import genai
import streamlit as st

class GeminiAgent:
    """Agent sử dụng Gemini API miễn phí của Google để phân tích và bóc tách dữ liệu"""
    
    @staticmethod
    def get_client():
        # Tự động lấy API key từ Streamlit Secrets hoặc biến môi trường
        api_key = None
        try:
            if "GEMINI_API_KEY" in st.secrets:
                api_key = st.secrets["GEMINI_API_KEY"]
        except Exception:
            pass
        
        if not api_key:
            api_key = os.environ.get("GEMINI_API_KEY")
            
        return genai.Client(api_key=api_key) if api_key else genai.Client()

    @classmethod
    def call_gemini(cls, prompt: str) -> str:
        try:
            client = cls.get_client()
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
            )
            return response.text.strip()
        except Exception as e:
            return f"❌ Lỗi Gemini API: {str(e)}. Hãy cấu hình GEMINI_API_KEY trong Streamlit Secrets."

    @classmethod
    def parse_samfw(cls, raw_text: str, model: str, csc: str) -> str:
        prompt = (
            f"Bạn là chuyên gia phần cứng Samsung. Dưới đây là nội dung văn bản thô được cào trực tiếp từ trang Samfw cho model {model} (CSC: {csc}):\n\n"
            f"{raw_text}\n\n"
            "Nhiệm vụ: Phân tích kỹ nội dung trên và trích xuất CHÍNH XÁC 100% mã Build PDA firmware mới nhất.\n"
            "Yêu cầu nghiêm ngặt: Chỉ trả về chuỗi mã Build thực tế (ví dụ dạng S948BXXU3...), tuyệt đối không bịa đặt hay dùng mã giả."
        )
        return cls.call_gemini(prompt)

    @classmethod
    def diagnose_odin(cls, log_text: str) -> str:
        prompt = f"Phân tích chuỗi log Odin báo lỗi sau, tìm nguyên nhân gốc rễ và cách khắc phục an toàn:\n{log_text}"
        return cls.call_gemini(prompt)
