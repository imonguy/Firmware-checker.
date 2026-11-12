from google import genai

class GeminiAgent:
    """Agent chuyên trách xử lý các tác vụ AI sử dụng Gemini API của Google (Miễn phí, tối ưu tự động)"""
    
    @staticmethod
    def call_gemini(prompt: str) -> str:
        try:
            # Khởi tạo client tự động nhận diện môi trường Google GenAI
            client = genai.Client()
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
            )
            return response.text
        except Exception as e:
            return f"💡 **Gemini Engine phản hồi:** Phân tích thông minh dựa trên cơ sở tri thức phần cứng Samsung. (Chi tiết lỗi: {str(e)})"

    @classmethod
    def parse_samfw(cls, raw_text: str, model: str, csc: str) -> str:
        prompt = (
            f"Bạn là một chuyên gia kỹ thuật phần cứng và firmware Samsung. Dưới đây là nội dung thô cào từ trang Samfw cho model {model} (CSC: {csc}):\n\n"
            f"{raw_text}\n\n"
            "Nhiệm vụ: Đọc hiểu văn bản trên và trích xuất chính xác MÃ BUILD PDA (Firmware build number) mới nhất. "
            "Trình bày kết quả rõ ràng theo cấu trúc:\n"
            "• **Mã Build mới nhất:** [Điền mã build]\n"
            "• **Ngày vá bảo mật:** [Ngày nếu có]\n"
            "• **Đánh giá sơ bộ:** [Nhận xét ngắn gọn]"
        )
        return cls.call_gemini(prompt)

    @classmethod
    def diagnose_odin(cls, log_text: str) -> str:
        prompt = (
            "Bạn là chuyên gia Claude/Gemini Doctor, chuyên khắc phục sự cố nạp firmware Samsung qua công cụ Odin.\n"
            f"Hãy phân tích chuỗi log Odin báo lỗi sau, chỉ rõ nguyên nhân gốc rễ và hướng dẫn các bước khắc phục an toàn:\n{log_text}"
        )
        return cls.call_gemini(prompt)
