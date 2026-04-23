#!/usr/bin/env python3
"""Basit bir terminal asistanı: Jarvis."""

from __future__ import annotations

import datetime as _dt
import subprocess
from dataclasses import dataclass, field
from typing import Callable


COMMANDS = {
    "yardim": "Komutları listeler.",
    "saat": "UTC saatini söyler.",
    "tarih": "Bugünün tarihini söyler.",
    "not": "Kısa bir not alır. Kullanım: not <metin>",
    "notlar": "Alınan notları listeler.",
    "maxmod ac": "Iron Man MAX modunu açar.",
    "maxmod kapa": "Iron Man MAX modunu kapatır.",
    "maxmod durum": "MAX modunun açık/kapalı bilgisini verir.",
    "telefon durum": "ADB bağlı cihazı listeler.",
    "telefon batarya": "Android batarya bilgisini gösterir.",
    "telefon wifi ac|kapa": "Wi-Fi durumunu aç/kapat.",
    "telefon bluetooth ac|kapa": "Bluetooth durumunu aç/kapat.",
    "cikis": "Jarvis'i kapatır.",
}

MAX_STATUS = [
    "⚙️ Arc reaktör: %100",
    "🛡️ Kalkan sistemi: Aktif",
    "🚀 İtki sistemi: Hazır",
    "🎯 Hedefleme: Stabil",
]


@dataclass
class RuntimeState:
    notes: list[str] = field(default_factory=list)
    max_mode: bool = False


def _utc_now() -> _dt.datetime:
    return _dt.datetime.now(tz=_dt.timezone.utc)


def _help_text() -> str:
    lines = ["Yapabileceklerim:"]
    for key, desc in COMMANDS.items():
        lines.append(f"- {key}: {desc}")
    lines.append("Not: Telefon komutları için bilgisayarda adb kurulu ve USB hata ayıklama açık olmalı.")
    return "\n".join(lines)


def _max_mode_prompt(enabled: bool) -> str:
    return "JARVIS-MAX> " if enabled else "Jarvis> "


def _run_shell(command: list[str]) -> tuple[int, str, str]:
    try:
        proc = subprocess.run(command, capture_output=True, text=True, check=False)
    except FileNotFoundError:
        return 127, "", f"komut bulunamadı: {command[0]}"
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def _adb(*args: str, executor: Callable[[list[str]], tuple[int, str, str]] = _run_shell) -> tuple[int, str, str]:
    return executor(["adb", *args])


def _phone_help() -> str:
    return (
        "Telefon komutları:\n"
        "- telefon durum\n"
        "- telefon batarya\n"
        "- telefon wifi ac|kapa\n"
        "- telefon bluetooth ac|kapa"
    )


def _handle_phone(raw: str, executor: Callable[[list[str]], tuple[int, str, str]]) -> str:
    lower = raw.lower().strip()

    if lower == "telefon":
        return _phone_help()

    if lower == "telefon durum":
        code, out, err = _adb("devices", executor=executor)
        if code != 0:
            return f"ADB erişimi başarısız: {err or 'adb komutu çalıştırılamadı.'}"
        return f"Bağlı cihazlar:\n{out or 'Cihaz bulunamadı.'}"

    if lower == "telefon batarya":
        code, out, err = _adb("shell", "dumpsys", "battery", executor=executor)
        if code != 0:
            return f"Batarya bilgisi alınamadı: {err or 'cihaz bağlı olmayabilir.'}"
        if not out:
            return "Batarya çıktısı boş geldi."
        lines = out.splitlines()
        keep = [line.strip() for line in lines if any(k in line.lower() for k in ["level", "status", "temperature", "health"])]
        if not keep:
            keep = lines[:12]
        return "Batarya özeti:\n" + "\n".join(keep)

    if lower in {"telefon wifi ac", "telefon wifi kapa"}:
        mode = "enable" if lower.endswith("ac") else "disable"
        code, _, err = _adb("shell", "svc", "wifi", mode, executor=executor)
        if code != 0:
            return f"Wi-Fi komutu başarısız: {err or 'izin/cihaz sorunu.'}"
        return "Wi-Fi komutu gönderildi."

    if lower in {"telefon bluetooth ac", "telefon bluetooth kapa"}:
        mode = "enable" if lower.endswith("ac") else "disable"
        code, _, err = _adb("shell", "cmd", "bluetooth_manager", mode, executor=executor)
        if code != 0:
            return f"Bluetooth komutu başarısız: {err or 'Android sürümü desteklemiyor olabilir.'}"
        return "Bluetooth komutu gönderildi."

    return "Telefon komutu anlaşılamadı. Yardım için 'telefon' yaz."


def _handle(message: str, state: RuntimeState, executor: Callable[[list[str]], tuple[int, str, str]] = _run_shell) -> str:
    raw = message.strip()
    if not raw:
        return "Bir şey yaz, efendim."

    lower = raw.lower()

    if lower in {"yardim", "help"}:
        return _help_text()

    if lower.startswith("telefon"):
        return _handle_phone(raw, executor=executor)

    if lower == "saat":
        text = f"UTC saat: {_utc_now().strftime('%H:%M:%S')}"
        if state.max_mode:
            text += " | MAX telemetri senkron."
        return text

    if lower == "tarih":
        return f"Bugün (UTC): {_utc_now().strftime('%Y-%m-%d')}"

    if lower.startswith("not "):
        content = raw[4:].strip()
        if not content:
            return "Not boş olamaz."
        state.notes.append(content)
        return f"Not alındı ({len(state.notes)}): {content}"

    if lower == "notlar":
        if not state.notes:
            return "Henüz not yok."
        joined = "\n".join(f"{i + 1}. {n}" for i, n in enumerate(state.notes))
        return f"Notların:\n{joined}"

    if lower in {"maxmod", "maxmod durum", "iron man max", "max mod", "max modu"}:
        state_text = "AÇIK" if state.max_mode else "KAPALI"
        return f"Iron Man MAX modu: {state_text}"

    if lower in {"maxmod ac", "max mod ac", "iron man max modu"}:
        state.max_mode = True
        status = "\n".join(MAX_STATUS)
        return f"Iron Man MAX modu etkinleştirildi.\n{status}"

    if lower in {"maxmod kapa", "max mod kapa"}:
        state.max_mode = False
        return "Iron Man MAX modu kapatıldı. Standart profile dönüldü."

    if lower in {"jarvis", "selam", "merhaba"}:
        if state.max_mode:
            return "MAX protokoldeyim efendim. Komut bekliyorum."
        return "Hazırım efendim. Komut için 'yardim' yazabilirsiniz."

    if state.max_mode:
        return "Komut doğrulanamadı. MAX mod açık: 'yardim' veya 'maxmod durum' yaz."

    return "Anlaşılamadı. 'yardim' yazarak komutları görebilirsiniz."


def run() -> None:
    print("Jarvis v3.0 başlatıldı. Çıkmak için 'cikis' yaz.")
    state = RuntimeState()

    while True:
        try:
            user_input = input("Sen> ")
        except EOFError:
            print(f"\n{_max_mode_prompt(state.max_mode)}Görüşmek üzere, efendim.")
            break

        if user_input.strip().lower() in {"cikis", "exit", "quit"}:
            print(f"{_max_mode_prompt(state.max_mode)}Görüşmek üzere, efendim.")
            break

        response = _handle(user_input, state)
        print(f"{_max_mode_prompt(state.max_mode)}{response}")


if __name__ == "__main__":
    run()
