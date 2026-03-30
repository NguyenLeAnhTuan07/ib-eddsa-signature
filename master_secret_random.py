import secrets

# Tạo một master secret dài 32 bytes (256 bits)
master_secret = secrets.token_bytes(32)

# Nếu bạn muốn lưu dưới dạng chuỗi Hex để dễ đọc/chép
master_secret_hex = secrets.token_hex(32)

print(f"Master Secret (Hex): {master_secret_hex}")