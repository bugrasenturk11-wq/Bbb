#!/usr/bin/env python3
"""Jarvis için basit masaüstü uygulama (Tkinter)."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from jarvis import RuntimeState, _handle


class JarvisApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.state = RuntimeState()

        self.root.title("Jarvis Uygulaması")
        self.root.geometry("760x520")

        self._build_ui()
        self._append("Jarvis", "Merhaba efendim. Uygulamaya hoş geldiniz.")

    def _build_ui(self) -> None:
        container = ttk.Frame(self.root, padding=12)
        container.pack(fill="both", expand=True)

        self.chat = tk.Text(container, wrap="word", state="disabled", height=22)
        self.chat.pack(fill="both", expand=True)

        row = ttk.Frame(container)
        row.pack(fill="x", pady=(10, 0))

        self.entry = ttk.Entry(row)
        self.entry.pack(side="left", fill="x", expand=True)
        self.entry.bind("<Return>", self._send_event)

        send_btn = ttk.Button(row, text="Gönder", command=self._send)
        send_btn.pack(side="left", padx=(8, 0))

        quick = ttk.Frame(container)
        quick.pack(fill="x", pady=(10, 0))

        ttk.Button(quick, text="Yardım", command=lambda: self._send("yardim")).pack(side="left")
        ttk.Button(quick, text="MAX Aç", command=lambda: self._send("maxmod ac")).pack(side="left", padx=(6, 0))
        ttk.Button(quick, text="MAX Kapat", command=lambda: self._send("maxmod kapa")).pack(side="left", padx=(6, 0))
        ttk.Button(quick, text="Telefon Durum", command=lambda: self._send("telefon durum")).pack(side="left", padx=(6, 0))

    def _append(self, who: str, message: str) -> None:
        self.chat.configure(state="normal")
        self.chat.insert("end", f"{who}: {message}\n\n")
        self.chat.see("end")
        self.chat.configure(state="disabled")

    def _send_event(self, _event: tk.Event) -> None:
        self._send()

    def _send(self, preset: str | None = None) -> None:
        text = preset if preset is not None else self.entry.get().strip()
        if preset is None:
            self.entry.delete(0, "end")
        if not text:
            return

        self._append("Sen", text)
        response = _handle(text, self.state)
        label = "JARVIS-MAX" if self.state.max_mode else "Jarvis"
        self._append(label, response)


def main() -> None:
    root = tk.Tk()
    JarvisApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
