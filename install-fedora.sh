#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
set -e
echo "[*] جاري تثبيت متطلبات التشفير على نظام Fedora Linux..."
sudo dnf install -y python3 python3-cryptography
chmod +x fedora-vault.py
sudo cp fedora-vault.py /usr/local/bin/fedora-vault
echo "[+] تم التثبيت بنجاح! يمكنك الآن استخدام الأمر: fedora-vault"
