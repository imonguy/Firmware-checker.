import anthropic

class ClaudeAPIClient:
    """Client chuyên biệt quản lý các tác vụ gọi Claude AI (Anthropic)"""
    
    @staticmethod
    def call_claude(api_key: str, system_prompt: str, user_prompt: str) -> str:
        if not api_key:
            return "⚠️ Vui lòng nhập Anthropic API Key của bạn ở thanh Sidebar bên trái để kích hoạt AI."
        try:
            client = anthropic.Anthropic(api_key=api_key)
            message = client.messages.create(
                model="claude-3-5-sonnet-20241022", # Model Claude mạnh mẽ nhất cho lập trình và phân tích văn bản
                max_tokens=1500,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}]
            )
            return message.content[0].text
        except Exception as e:
            return f"❌ Lỗi kết nối tới Anthropic API: {str(e)}"

    @classmethod
    def parse_samfw_firmware(cls, api_key: str, raw_text: str, model: str, csc: str) -> str:
        """Sử dụng Claude để bóc tách mã Build firmware chuẩn xác từ nội dung Samfw"""
        system_msg = "Bạn là hệ thống trích xuất dữ liệu phần cứng Samsung chuyên nghiệp. Nhiệm vụ của bạn là đọc nội dung HTML/văn bản từ Samfw và tìm ra MÃ BUILD PDA (Firmware build number mới nhất, ví dụ dạng S948BXXU...) chính xác tuyệt đối."
        user_msg = (
            f"Dưới đây là nội dung trang web Samfw cho model {model} với CSC {csc}:\n\n"
            f"{raw_text}\n\n"
            "Hãy trích xuất DUY NHẤT mã Build PDA mới nhất, ngày vá bảo mật và ghi chú ngắn gọn theo định dạng:\n"
            "BUILD: [mã build]\nNgày vá: [ngày]\nChi tiết:"
        )
        return cls.call_claude(api_key, system_msg, user_msg)

    @classmethod
    def diagnose_odin(cls, api_key: str, log_text: str) -> str:
        """Chuyên gia Claude Doctor phân tích lỗi flash Odin"""
        system_msg = "Bạn là chuyên gia kỹ thuật phần mềm Samsung cao cấp, chuyên khắc phục sự cố nạp firmware qua Odin."
        user_msg = f"Hãy phân tích nguyên nhân cốt lõi và cách khắc phục chi tiết cho đoạn log Odin báo lỗi sau:\n{log_text}"
        return cls.call_claude(api_key, system_msg, user_msg)
