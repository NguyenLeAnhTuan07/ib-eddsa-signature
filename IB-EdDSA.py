import hashlib
import hmac
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey
)
from cryptography.hazmat.primitives import serialization
"""
EdDSA là một thuật toán chữ ký số hiện đại dựa trên các đường cong elliptic ở dạng Edwards xoắn,
cụ thể là Ed25519 và Ed448, được xác định trên các trường hữu hạn có cùng tham số với Curve25519 và Curve448.
"""


"""
IB-EdDSA không định nghĩa thuật toán Gen mới.
Các tham số hệ thống (p, G, n, curve) được lấy trực tiếp từ chuẩn Ed25519
(RFC 8032). IB chỉ thay đổi cơ chế cấp khóa bí mật theo danh tính.
"""
# Gen: thiết lập các tham số toàn cục của hệ Ed25519.
# Trong thực tế, bước này được chuẩn hóa và thực hiện sẵn bởi thư viện,
# không cần cài đặt thủ công trong mô hình IB-EdDSA.

MASTER_SECRET = b"day la master secret cua nguyen le anh tuan, cai nay can bao mat"


DOMAIN_EXTRACT = b"IB-EdDSA-EXTRACT"
DOMAIN_SIGN = b"IB-EdDSA-SIGN"
"""
Gắn một chuỗi định danh ngữ cảnh cố định vào đầu dữ liệu trước khi đưa vào hàm mật mã,
nhằm đảm bảo rằng cùng một dữ liệu nhưng ở các ngữ cảnh khác nhau sẽ cho kết quả hoàn toàn khác nhau.
"""

# LOAD ID
def load_id(id_path):
    """
    Đọc ID người dùng từ file
    ID = email | IP | role | ...
    """
    with open(id_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines()]
    return "|".join(lines).encode()

# EXTRACT – TẠO KHÓA RIÊNG TỪ ID
def extract_private_key(ID: bytes):
    """
    Thuật toán Extract(ID):
    sk_ID = H(MSK || ID || domain) mod n
    """

    # HMAC-SHA512(MSK, domain || ID)
    digest = hmac.new( #hmac.new(key, msg, hash)
        MASTER_SECRET,
        DOMAIN_EXTRACT + ID,
        hashlib.sha512
    ).digest() #.digets() dùng để trả về 64 byte = 512 bit theo đúng output SHA-512
    # HMAC-SHA512 được dùng trong IB-EdDSA để sinh khóa theo danh tính.
    # Master secret đóng vai trò là khóa HMAC; dữ liệu đầu vào gồm domain (tách ngữ nghĩa, chống cross-protocol)
    # và ID người dùng. Nhờ cấu trúc HMAC, hàm Extract hoạt động như một PRF,
    # an toàn hơn so với việc dùng hàm băm thông thường.
    """
    Trong IB-EdDSA, Master Secret Key không trực tiếp là khóa riêng, mà đóng vai trò khóa của một hàm giả ngẫu nhiên (PRF).
    Hàm Extract sử dụng MSK kết hợp với ID để sinh ra seed xác định, từ đó ánh xạ thành khóa riêng trên đường cong Edwards25519.
    """
    seed = digest[:32]  # 32 bytes đúng chuẩn Ed25519

    private_key = Ed25519PrivateKey.from_private_bytes(seed)
    """
    Ed25519Privatekey
    Clamp bit (theo RFC 8032): Clear bit thấp, Set bit cao
    Tạo scalar bí mật a
    Chuẩn hóa khóa vào nhóm elliptic curve
 
    """
    public_key = private_key.public_key()
    #PK = a · G

    return seed, private_key, public_key


def generate_user_key(id_path, name):
    ID = load_id(id_path)

    seed, private_key, public_key = extract_private_key(ID)
    #seed: Private key thô (32 bytes)

    with open(f"{name}_private.txt", "w") as f:
        f.write(seed.hex())

    pub_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    )
    #Xuất khóa công khai ra dạng 32 byte chuẩn Ed25519 (RFC 8032)

    with open(f"{name}_public.txt", "w") as f:
        f.write(pub_bytes.hex())

    print(f"[+] Đã phát hành khóa IB cho {name}")


# INPUT PRIVATE KEY
def get_private_key():
    print("PRIVATE KEY INPUT:")
    print("1. Paste HEX")
    print("2. Load from file")
    c = input("Choose: ")

    if c == "1":
        hexkey = input("Paste private key (hex): ").strip()
    else:
        path = input("Private key file: ")
        with open(path) as f:
            hexkey = f.read().strip()

    return Ed25519PrivateKey.from_private_bytes(bytes.fromhex(hexkey))

# SIGN
def sign_file(file_path):
    """
    Sig(m, sk_ID)
    """
    private_key = get_private_key()

    with open(file_path, "rb") as f: #Mở file ở chế độ nhị phân rb
        msg = f.read() #Đọc toàn bộ nội dung file thành một chuỗi bytes msg

    # domain separation khi ký
    signature = private_key.sign(DOMAIN_SIGN + msg)

    with open(file_path + ".sig", "wb") as f:
        f.write(signature)

    print("[+] Đã ký file")

# INPUT PUBLIC KEY
def get_public_key():
    print("PUBLIC KEY INPUT:")
    print("1. Paste HEX")
    print("2. Load from file")
    c = input("Choose: ")

    if c == "1":
        hexkey = input("Paste public key (hex): ").strip()
    else:
        path = input("Public key file: ")
        with open(path) as f:
            hexkey = f.read().strip()

    return Ed25519PublicKey.from_public_bytes(bytes.fromhex(hexkey))

# VERIFY
def verify(file_path, sig_path):
    """
    Ver(m, o, pk_ID)
    """
    public_key = get_public_key()

    with open(file_path, "rb") as f:
        msg = f.read()

    with open(sig_path, "rb") as f:
        sig = f.read()

    try:
        public_key.verify(sig, DOMAIN_SIGN + msg)
        print("[✓] Chữ ký HỢP LỆ")
    except:
        print("[✗] Chữ ký KHÔNG HỢP LỆ")

# MENU
def main():
    print("=== IB-EdDSA SYSTEM ===")
    print("1. Extract key from ID")
    print("2. Sign file")
    print("3. Verify signature")
    c = input("Choose: ")

    if c == "1":
        idp = input("ID file: ")
        name = input("User name: ")
        generate_user_key(idp, name)
    elif c == "2":
        sign_file(input("File to sign: "))
    elif c == "3":
        verify(
            input("File: "),
            input("Signature: ")
        )
    else:
        print("Invalid choice")


if __name__ == "__main__":
    main()
