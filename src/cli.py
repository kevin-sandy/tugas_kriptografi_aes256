import argparse
import sys
import os

# Import fungsi dari modul aes_utils
from aes_utils import encrypt_file_aes, decrypt_file_aes

def main():
    parser = argparse.ArgumentParser(description="Aplikasi Enkripsi Dataset AES-256 (CBC)")
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Command: encrypt
    enc_parser = subparsers.add_parser('encrypt', help='Enkripsi file')
    enc_parser.add_argument('input_file', help='Path file input (.csv/.txt)')
    enc_parser.add_argument('output_file', help='Path untuk menyimpan hasil (.txt/hex)')
    enc_parser.add_argument('-p', '--password', required=True, help='Password enkripsi')

    # Command: decrypt
    dec_parser = subparsers.add_parser('decrypt', help='Dekripsi file')
    dec_parser.add_argument('input_file', help='Path file terenkripsi (.txt/hex)')
    dec_parser.add_argument('output_file', help='Path untuk menyimpan hasil asli (.csv)')
    dec_parser.add_argument('-p', '--password', required=True, help='Password dekripsi')

    args = parser.parse_args()

    # Cek apakah file input ada
    if not os.path.exists(args.input_file):
        print(f"[ERROR] File input tidak ditemukan: {args.input_file}")
        sys.exit(1)

    try:
        if args.command == 'encrypt':
            print("Memproses Enkripsi...")
            encrypt_file_aes(args.input_file, args.output_file, args.password)
        elif args.command == 'decrypt':
            print("Memproses Dekripsi...")
            decrypt_file_aes(args.input_file, args.output_file, args.password)
            
    except Exception as e:
        print(f"[ERROR] Terjadi kesalahan: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()