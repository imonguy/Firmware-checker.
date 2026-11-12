import anthropic

class ClaudeMasterAgent:
    """Agent chuyên trách xử lý các tác vụ phân tích, bóc tách firmware và chẩn đoán phần cứng Samsung"""
    
    @staticmethod
    def call_claude(api_key: str, system_prompt: str, user_prompt: str) -> str:
        if not api_key or not api_key.strip():
            return "⚠️ Vui lòng nhập Anthropic API Key hợp lệ ở thanh Sidebar bên trái để kích hoạt Agent Claude."
        try:
            client = anthropic.Anthropic(api_key=api_key)
            message = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1500,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}]
            )
            return message.content[0].text
        except Exception as e:
            return f"❌ Lỗi kết nối Anthropic API: {str(e)}"

    @classmethod
    def parse_samfw_firmware(cls, api_key: str, raw_html_text: str, model: str, csc: str) -> str:
        system_prompt = (
            "Bạn là một Trợ lý AI chuyên gia về dữ liệu phần cứng và firmware Samsung. "
            "Nhiệm vụ của bạn là tiếp nhận nội dung văn bản thô được cào từ trang Samfw.com "
            "của một model thiết bị và khu vực CSC cụ thể, sau đó lọc và tìm ra chính xác MÃ BUILD (PDA) MỚI NHẤT."
        )
        user_prompt = (
            f"Dưới đây là nội dung thô được lấy từ Samfw cho thiết bị [{model}] với mã vùng khu vực [{csc}]:\n\n"
            f"{raw_html_text}\n\n"
            "Yêu cầu nhiệm vụ:\n"
            "1. Phân tích văn bản để tìm ra mã Build PDA firmware thực tế mới nhất (ví dụ dạng S948BXXU..., A556EXXS..., v.v.).\n"
            "2. Tuyệt đối khônga bịa đặt số liệu. Nếu có nhiều phiên bản, hãy chọn phiên bản phát hành mới nhất nằm ở trên cùng.\n"
            "3. Trình bày kết quả rõ ràng theo định dạng cấu trúc sau:\n"
            "• **Mã Build mới nhất:** [Điền mã build chính xác]\n"
            "• **Trạng thái trích xuất:** Samfw Live AI Parsed\n"
            "• **Thông tin bổ sung:** [Ngày phát hành hoặc các chi tiết đi kèm nếu tìm thấy trong văn bản]"
        )
        return cls.call_claude(api_key, system_prompt, user_prompt)

    @classmethod
    def diagnose_odin(cls, api_key: str, log_text: str) -> str:
        system_prompt = "Bạn là chuyên gia Claude Doctor, chuyên gia khắc phục sự cố nạp firmware Samsung qua công cụ Odin."
        user_prompt = (
            f"Hãy phân tích chuỗi log Odin báo lỗi sau đây, chỉ rõ nguyên nhân gốc rễ "
            "và đưa ra các bước khắc phục thực tế an toàn nhất cho người dùng:\n{log_text}"
        )
        return cls.call_claude(api_key, system_prompt, user_prompt)
