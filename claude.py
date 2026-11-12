import anthropic

class ClaudeAPIClient:
    """Agent chuyên trách xử lý các tác vụ gọi Claude AI, bóc tách firmware và chẩn đoán phần cứng Samsung"""
    
    @staticmethod
    def call_claude(api_key: str, system_prompt: str, user_prompt: str) -> str:
        if not api_key or not api_key.strip():
            return "⚠️ Vui lòng nhập Anthropic API Key hợp lệ ở thanh Sidebar bên trái để kích hoạt Agent Claude."
        try:
            client = anthropic.Anthropic(api_key=api_key)
            message = client.messages.create(
                model="claude-3-5-sonnet-20241022",  # Model Claude tối ưu cho phân tích mã nguồn và cú pháp
                max_tokens=1500,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}]
            )
            return message.content[0].text
        except Exception as e:
            return f"❌ Lỗi kết nối Anthropic API: {str(e)}"

    @classmethod
    def parse_samfw_firmware(cls, api_key: str, raw_html_text: str, model: str, csc: str) -> str:
        """Smart Parser Agent: Đọc nội dung HTML thô từ Samfw để trích xuất mã Build mới nhất"""
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
            "2. Tuyệt đối không bịa đặt số liệu. Nếu có nhiều phiên bản, hãy chọn phiên bản phát hành mới nhất nằm ở trên cùng.\n"
            "3. Trình bày kết quả rõ ràng theo định dạng cấu trúc sau:\n"
            "• **Mã Build mới nhất:** [Điền mã build chính xác]\n"
            "• **Trạng thái trích xuất:** Samfw Live AI Parsed\n"
            "• **Thông tin bổ sung:** [Ngày phát hành hoặc các chi tiết đi kèm nếu tìm thấy trong văn bản]"
        )
        return cls.call_claude(api_key, system_prompt, user_prompt)

    @classmethod
    def analyze_firmware_intelligence(cls, api_key: str, build_code: str, model: str, csc: str) -> str:
        """Agent phân tích chuyên sâu phần mềm và phần cứng"""
        system_prompt = "Bạn là Claude Opus 5.5, một chuyên gia kỹ thuật hệ điều hành và phần cứng Samsung cấp cao."
        user_prompt = (
            f"Hãy phân tích chuyên sâu về bản dựng firmware mã `{build_code}` của thiết bị `{model}` (Khu vực: `{csc}`). "
            "Đánh giá các cải tiến về hiệu suất tập lệnh 64-bit, tối ưu hóa NPU, độ mượt của giao diện One UI mới nhất "
            "và tính an toàn khi tiến hành nạp nâng cấp."
        )
        return cls.call_claude(api_key, system_prompt, system_prompt and user_prompt)

    @classmethod
    def diagnose_odin(cls, api_key: str, log_text: str) -> str:
        """Odin Doctor Agent chuyên chẩn đoán lỗi flash phần cứng"""
        system_prompt = "Bạn là chuyên gia Claude Doctor, chuyên khắc phục sự cố nạp firmware Samsung qua công cụ Odin."
        user_prompt = (
            f"Hãy phân tích chuỗi log Odin báo lỗi sau đây, chỉ rõ nguyên nhân gốc rễ "
            f"và đưa ra các bước khắc phục thực tế an toàn nhất cho người dùng:\n{log_text}"
        )
        return cls.call_claude(api_key, system_prompt, user_prompt)

# Tạo alias tương thích ngược để app.py gọi theo tên nào cũng không bị lỗi
ClaudeMasterAgent = ClaudeAPIClient
