#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
# درع البيانات (Data Shield) - أداة تشفير وفك تشفير مفتوحة المصدر متوافقة مع فيدورا لينكس (Fedora Linux)
# تستخدم نفس معيار تطبيق الويب: AES-256-GCM + PBKDF2-HMAC-SHA256 (100,000 iterations)
# تثبيت المتطلبات على فيدورا: sudo dnf install -y python3 python3-cryptography
import sys
import os
import base64
import getpass
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

ITERATIONS = 100000

def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=ITERATIONS,
    )
    return kdf.derive(password.encode('utf-8'))

def encrypt_bytes(data: bytes, password: str) -> bytes:
    salt = os.urandom(16)
    iv = os.urandom(12)
    key = derive_key(password, salt)
    aesgcm = AESGCM(key)
    ct = aesgcm.encrypt(iv, data, None)
    return salt + iv + ct

def decrypt_bytes(payload: bytes, password: str) -> bytes:
    if len(payload) < 29:
        raise ValueError('البيانات المشفرة غير صالحة أو قصيرة جداً')
    salt = payload[:16]
    iv = payload[16:28]
    ct = payload[28:]
    key = derive_key(password, salt)
    aesgcm = AESGCM(key)
    return aesgcm.decrypt(iv, ct, None)

def main():
    if len(sys.argv) < 3:
        print('الاستخدام على Fedora Linux:')
        print('  تشفير ملف : python3 fedora-vault.py enc-file <path>')
        print('  فك ملف    : python3 fedora-vault.py dec-file <path.vault>')
        print('  تشفير نص  : python3 fedora-vault.py enc-text "النص السري"')
        print('  فك نص     : python3 fedora-vault.py dec-text "<Base64>"')
        sys.exit(1)

    mode = sys.argv[1]
    target = sys.argv[2]
    pwd = getpass.getpass('أدخل مفتاح التشفير السري (كلمة المرور): ')

    try:
        if mode == 'enc-file':
            with open(target, 'rb') as f:
                raw = f.read()
            out_path = target + '.vault'
            with open(out_path, 'wb') as f:
                f.write(encrypt_bytes(raw, pwd))
            print('[+] تم تشفير الملف بنجاح:', out_path)
        elif mode == 'dec-file':
            with open(target, 'rb') as f:
                raw = f.read()
            out_path = target[:-6] if target.endswith('.vault') else 'decrypted_' + os.path.basename(target)
            with open(out_path, 'wb') as f:
                f.write(decrypt_bytes(raw, pwd))
            print('[+] تم فك تشفير الملف واستعادته:', out_path)
        elif mode == 'enc-text':
            b64 = base64.b64encode(encrypt_bytes(target.encode('utf-8'), pwd)).decode('ascii')
            print('[+] النص المشفر (Base64):')
            print(b64)
        elif mode == 'dec-text':
            plain = decrypt_bytes(base64.b64decode(target), pwd).decode('utf-8')
            print('[+] النص الأصلي:')
            print(plain)
        else:
            print('[-] أمر غير معروف:', mode)
    except Exception as e:
        print('[-] فشلت العملية: تأكد من صحة كلمة المرور أو سلامة الملف.', e)
        sys.exit(2)

if __name__ == '__main__':
    main()
