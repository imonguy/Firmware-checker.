import sqlite3
import os

DB_FILE = "firmware_cache.db"

class DatabaseManager:
    @staticmethod
    def init_db():
        """Khởi tạo bảng lưu trữ dữ liệu firmware cục bộ"""
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS firmware_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                model TEXT,
                csc TEXT,
                build_number TEXT,
                os_version TEXT,
                security_patch TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

    @staticmethod
    def save_firmware(model, csc, build, os_ver, patch):
        """Lưu kết quả quét vào database nội bộ"""
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO firmware_logs (model, csc, build_number, os_version, security_patch)
            VALUES (?, ?, ?, ?, ?)
        ''', (model, csc, build, os_ver, patch))
        conn.commit()
        conn.close()

    @staticmethod
    def get_latest_firmware(model, csc):
        """Lấy dữ liệu đã cache để hiển thị ngay lập tức không cần gọi mạng"""
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT build_number, os_version, security_patch FROM firmware_logs
            WHERE model = ? AND csc = ? ORDER BY id DESC LIMIT 1
        ''', (model, csc))
        row = cursor.fetchone()
        conn.close()
        return row
