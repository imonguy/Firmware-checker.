import os
from google import genai
import streamlit as st

class GeminiAgent:
    """Agent sử dụng mô hình Gemini 3.8 Flash mới nhất để phân tích và bóc tách firmware thực tế"""
    
    @staticmethod
    def get_client():
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
            # Nâng cấp lên model Gemini 3.8 Flash thông minh nhất cho agent và cào dữ liệu
            response = client.models.generate_content(
                model='gemini-3.8-flash',
                contents=prompt,
            )
            return response.text.strip()
        except Exception as e:
            return f"❌ Lỗi Gemini API: {str(e)}. Hãy kiểm tra lại GEMINI_API_KEY trong Streamlit Secrets."

    @classmethod
    def parse_samfw(cls, raw_text: str, model: str, csc: str) -> str:
        prompt = (
            f"Bạn là chuyên gia kỹ thuật phần cứng Samsung. Dưới đây là nội dung văn bản thô được cào từ trang Samfw cho thiết bị [{model}] với khu vực [{csc}]:\n\n"
            f"{raw_text}\n\n"
            "Nhiệm vụ: Phân tích kỹ nội dung trên, bóc tách và trả về CHÍNH XÁC 100% mã Build PDA firmware thực tế mới nhất.\n"
            "Yêu cầu nghiêm ngặt: Chỉ cung cấp chuỗi mã Build (ví dụ: S948BXXU...), không thêm giải thích rườm rà."
        )
        return cls.call_gemini(prompt)

    @classmethod
    def diagnose_odin(cls, log_text: str) -> str:
        prompt = f"Phân tích chuỗi log Odin báo lỗi sau dưới góc độ chuyên gia hệ thống, tìm nguyên nhân gốc rễ và cách khắc phục an toàn:\n{log_text}"
        return cls.call_gemini(prompt)
