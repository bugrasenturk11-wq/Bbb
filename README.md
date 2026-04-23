# Jarvis (CLI Asistan)

Bu depo, terminalde çalışan bir **Jarvis** asistanı içerir.

## Çalıştırma

```bash
python3 jarvis.py
```

## Komutlar

- `yardim` → komut listesini gösterir
- `saat` → UTC saatini söyler
- `tarih` → UTC tarihini söyler
- `not <metin>` → not alır
- `notlar` → alınan notları listeler
- `maxmod ac` / `maxmod kapa` / `maxmod durum` → Iron Man MAX modu
- `telefon durum` → bağlı Android cihazları listeler
- `telefon batarya` → batarya özetini getirir
- `telefon wifi ac|kapa` → Wi‑Fi komutu yollar
- `telefon bluetooth ac|kapa` → Bluetooth komutu yollar
- `cikis` → programı kapatır

## Telefon kontrolü (Android / ADB)

Telefon komutları için:

1. Bilgisayarda `adb` kurulu olmalı.
2. Telefonda **Geliştirici seçenekleri** ve **USB hata ayıklama** açık olmalı.
3. Telefon USB ile bağlanıp yetki izni verilmiş olmalı.

> Not: Bu asistan komutları ADB üzerinden yerel makineden gönderir; cihaz tarafındaki izin/sürüm kısıtları bazı komutları engelleyebilir.


## Telefona yükleme (Android)

Jarvis'i telefonuna hızlıca kopyalamak için (ADB gerekli):

```bash
./scripts/install_to_android.sh
```

Bu komut `jarvis.py` ve `README.md` dosyalarını telefonda `/sdcard/JarvisCLI` klasörüne yükler.

Sonra telefonda (Termux):

```bash
pkg update -y
pkg install -y python
cd /sdcard/JarvisCLI
python jarvis.py
```

> Not: Bu işlem APK kurmaz; CLI uygulamasını dosya olarak yükler.


## Uygulama (GUI) olarak çalıştırma

CLI yerine pencere uygulaması olarak kullanmak için:

```bash
python3 jarvis_app.py
```

Bu sürümde mesajlarını kutuya yazıp **Gönder** ile çalıştırabilirsin.
Hızlı butonlar: Yardım, MAX Aç/Kapat ve Telefon Durum.
