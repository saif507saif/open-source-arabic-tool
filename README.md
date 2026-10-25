# 🛡️ درع البيانات (Data Shield Vault) — Open Source Encryption Suite

أداة تشفير وحماية بيانات محلية مفتوحة المصدر بالكامل (**Free and Open Source Software - MIT License**) تعمل داخل المتصفح وعلى نظام **Fedora Linux** دون أي اتصال بالخادم.

## ✨ المميزات الرئيسية
- **تشفير قياسي معتمد (AES-256-GCM)**: تشفير موثق يحمي السرية ويكتشف أي محاولة تلاعب بالبيانات.
- **اشتقاق مفاتيح قوي (PBKDF2-HMAC-SHA256)**: باستخدام 100,000 دورة وملح عشوائي (`16-byte Salt`) ومتجه ابتدائي (`12-byte IV`) لكل عملية.
- **توافق كامل مع Fedora Linux**: أداة طرفية (`fedora-vault.py`) متوافقة 100% مع صيغة `.vault` والواجهة الرسومية.
- **شفافية كاملة (Zero Telemetry)**: لا توجد أي خوادم خلفية أو تتبع، والكود قابل للمراجعة الأمنية والتعديل.

## 🐧 التشغيل على Fedora Linux
```bash
sudo dnf install -y python3 python3-cryptography
chmod +x fedora-vault.py
python3 fedora-vault.py enc-file secret.pdf
python3 fedora-vault.py dec-file secret.pdf.vault
```

## 🌐 تشغيل واجهة الويب محلياً
افتح ملف `data_encryption_vault.html` مباشرة في متصفح **Firefox** أو **Chromium** على نظام Fedora Linux أو أي نظام تشغيل آخر.

## ⚖️ الرخصة (License)
مرخص تحت رخصة **MIT License** مفتوحة المصدر (انظر ملف `LICENSE`).
