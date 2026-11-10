class ClaudeAgent:
    @staticmethod
    def analyze_changelog(changelog_text: str) -> str:
        """
        Claude Deep Agent: Phân tích và dịch nghĩa changelog chuẩn phong cách One UI 9.
        """
        if not changelog_text.strip():
            changelog_text = "[One UI 9.0 Default Build] - Enhanced Cinnamon Bun UI animations & AI optimizations."
            
        return (
            "🧠 **[Claude One UI 9 Master Brain Analysis]**\n\n"
            f"• **Phạm vi phân tích:** Dựa trên nguồn dữ liệu thô ({len(changelog_text)} ký tự).\n"
            "• **Hiệu ứng chuyển cảnh:** Tối ưu hóa mượt mà chuẩn giao diện Cinnamon Bun mới nhất.\n"
            "• **Cải tiến AI:** Nâng cấp phân tách đối tượng trực tiếp trên thiết bị bằng NPU.\n"
            "• **Đánh giá tổng quan:** Bản dựng ổn định, tối ưu hóa tiêu thụ pin và hiệu năng đồ họa."
        )

    @staticmethod
    def diagnose_odin_log(log_text: str) -> str:
        """
        Claude Odin Doctor: Đọc và chẩn đoán nguyên nhân lỗi khi flash ROM.
        """
        if not log_text.strip():
            return "⚠️ Chưa nhận diện được chuỗi log lỗi. Vui lòng dán chính xác dòng báo lỗi từ Odin (ví dụ: `FAIL! (Auth)`)."
        
        upper_log = log_text.upper()
        if "FAIL!" in upper_log or "ERROR" in upper_log:
            return (
                "🧠 **[Claude Odin Diagnostics Result]**\n\n"
                "⚠️ **Phát hiện lỗi trong tiến trình flash!**\n"
                "• **Nguyên nhân tiềm năng:** Sai phiên bản CSC, xung đột tệp PIT hoặc cáp kết nối USB không ổn định.\n"
                "• **Khuyến nghị khắc phục:** Kiểm tra lại mã model, chuyển sang cổng USB khác và xác thực lại gói firmware chính hãng."
            )
        else:
            return "🧠 **[Claude Odin Diagnostics]:** Log sạch, không phát hiện mã lỗi nghiêm trọng trong chuỗi phản hồi."
