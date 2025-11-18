# quiz_app/utils/constants.py

"""
Chứa các hằng số về thiết kế (màu sắc, khoảng cách, font chữ, bo góc).
Điều này giúp đảm bảo giao diện đồng nhất và dễ dàng thay đổi toàn bộ theme.
"""

# Colors - Light Theme Only
class Colors:
    # Primary blue palette màu chủ đạo
    PRIMARY = "#2563eb"
    PRIMARY_LIGHT = "#3b82f6" 
    PRIMARY_LIGHTER = "#60a5fa"
    PRIMARY_LIGHTEST = "#eff6ff"
    
    # Gray scale colors: màu xám dùng làm nền và viền
    WHITE = "#ffffff"
    GRAY_50 = "#f8fafc"
    GRAY_100 = "#f1f5f9"
    GRAY_200 = "#e2e8f0"
    GRAY_300 = "#cbd5e1"
    GRAY_400 = "#94a3b8"
    GRAY_500 = "#64748b"
    GRAY_600 = "#475569"
    GRAY_700 = "#334155"
    GRAY_800 = "#1e293b"
    GRAY_900 = "#0f172a"
    
    # Accent colors màu nhấn nếu báo lỗi hoặc thành công
    SUCCESS = "#10b981"
    WARNING = "#f59e0b"
    ERROR = "#ef4444"
    
    # Màu chữ
    TEXT_PRIMARY = "#1e293b"
    TEXT_SECONDARY = "#64748b"
    TEXT_MUTED = "#94a3b8"

# Spacing scale (4px base): khoảng cách giữa các thành phần
class Spacing:
    XS = 4
    SM = 8
    MD = 12
    LG = 16
    XL = 20
    XXL = 24
    XXXL = 32
    XXXXL = 48
    XXXXXL = 64

# Typography: kích thước chữ
class Typography:
    SIZE_XS = 12
    SIZE_SM = 14
    SIZE_BASE = 16
    SIZE_LG = 18
    SIZE_XL = 20
    SIZE_2XL = 24
    SIZE_3XL = 32

class BorderRadius:
    """Các giá trị bo góc (border radius).
    Sử dụng các hằng số này đảm bảo tất cả các thành phần như nút bấm, thẻ card, ô nhập liệu
    đều có độ bo góc nhất quán, tạo cảm giác đồng bộ cho thiết kế."""
    SM = 4
    MD = 8
    LG = 12
    XL = 16
    XXL = 24 # Bo góc lớn hơn cho các thành phần nổi bật.