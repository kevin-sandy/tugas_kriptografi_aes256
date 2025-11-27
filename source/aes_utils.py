import os
import binascii
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding, hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

# Konstanta Ukuran
SALT_SIZE = 16
IV_SIZE = 16
KEY_SIZE = 32  # 32 bytes = 256 bits (AES-256)
BLOCK_SIZE = 128 # AES block size is always 128 bits
MAX_FILE_SIZE = 1 * 1024 * 1024  # Batas 1 MB sesuai KAK

def derive_key(password: str, salt: bytes) -> bytes:
    """Mengubah password teks menjadi key 32-byte menggunakan PBKDF2."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_SIZE,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def check_file_size(file_path):
    """Memastikan ukuran file tidak melebihi 1 MB."""
    if os.path.getsize(file_path) > MAX_FILE_SIZE:
        raise ValueError("File terlalu besar! Maksimal 1 MB.")

def encrypt_file_aes(input_path, output_path, password):
    # 1. Validasi ukuran file
    check_file_size(input_path)

    # 2. Baca file asli (binary)
    with open(input_path, 'rb') as f:
        plaintext = f.read()

    # 3. Generate Salt & IV
    salt = os.urandom(SALT_SIZE)
    iv = os.urandom(IV_SIZE)

    # 4. Derivasi Key dari Password
    key = derive_key(password, salt)

    # 5. Lakukan Padding (PKCS7) agar pas kelipatan 16 byte
    padder = padding.PKCS7(BLOCK_SIZE).padder()
    padded_data = padder.update(plaintext) + padder.finalize()

    # 6. Enkripsi AES-CBC
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    # 7. Gabungkan: Salt + IV + Ciphertext
    encrypted_blob = salt + iv + ciphertext

    # 8. Konversi ke Hex dan simpan
    hex_output = binascii.hexlify(encrypted_blob).decode('utf-8')
    
    with open(output_path, 'w') as f:
        f.write(hex_output)
    
    print(f"[SUCCESS] File terenkripsi disimpan di: {output_path}")

def decrypt_file_aes(input_path, output_path, password):
    # 1. Baca file terenkripsi (format Hex string)
    with open(input_path, 'r') as f:
        hex_data = f.read().strip()
    
    try:
        encrypted_blob = binascii.unhexlify(hex_data)
    except binascii.Error:
        raise ValueError("File rusak: Bukan format Hex yang valid.")

    # 2. Validasi panjang data minimal (Salt + IV)
    if len(encrypted_blob) < (SALT_SIZE + IV_SIZE):
        raise ValueError("Data terlalu pendek/rusak.")

    # 3. Pisahkan komponen: Salt, IV, dan Ciphertext
    salt = encrypted_blob[:SALT_SIZE]
    iv = encrypted_blob[SALT_SIZE : SALT_SIZE + IV_SIZE]
    ciphertext = encrypted_blob[SALT_SIZE + IV_SIZE :]

    # 4. Derivasi ulang Key yang sama
    key = derive_key(password, salt)

    # 5. Dekripsi AES-CBC
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    
    try:
        padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    except Exception:
         raise ValueError("Gagal mendekripsi. Password salah atau file rusak.")

    # 6. Hapus Padding (Unpadding)
    try:
        unpadder = padding.PKCS7(BLOCK_SIZE).unpadder()
        plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
    except ValueError:
        raise ValueError("Password Salah! (Padding error)")

    # 7. Simpan file asli
    with open(output_path, 'wb') as f:
        f.write(plaintext)
    
    print(f"[SUCCESS] File berhasil didekripsi ke: {output_path}")