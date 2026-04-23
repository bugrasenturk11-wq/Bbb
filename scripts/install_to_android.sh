#!/usr/bin/env bash
set -euo pipefail

APP_DIR_ON_PHONE="/sdcard/JarvisCLI"

if ! command -v adb >/dev/null 2>&1; then
  echo "❌ adb bulunamadı. Önce Android Platform Tools kur." >&2
  exit 1
fi

if [[ "$(adb get-state 2>/dev/null || true)" != "device" ]]; then
  echo "❌ adb ile bağlı/izinli cihaz yok. USB hata ayıklamayı aç ve izin ver." >&2
  exit 1
fi

echo "📱 Cihaz bulundu. Dosyalar telefona aktarılıyor..."
adb shell "mkdir -p ${APP_DIR_ON_PHONE}"
adb push jarvis.py "${APP_DIR_ON_PHONE}/jarvis.py" >/dev/null
adb push README.md "${APP_DIR_ON_PHONE}/README.md" >/dev/null

echo "✅ Dosyalar yüklendi: ${APP_DIR_ON_PHONE}"
cat <<'EOF'

Termux ile çalıştırmak için telefonda:
1) Termux kur
2) Şu komutları çalıştır:
   pkg update -y
   pkg install -y python
   cd /sdcard/JarvisCLI
   python jarvis.py

Not:
- Telefon komutlarının çalışması için bilgisayarda adb açık olmalı ve cihaz bağlı olmalı.
- Bu script APK üretmez; Jarvis CLI dosyalarını telefona kopyalar.
EOF
