#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sarj kablosu dugum laboratuvari. Calisir. Gereksizdir."""

from __future__ import annotations

import argparse
import base64
import hashlib
import sys

DAMGA = (
    "DAMGA / IMZA | 4 Ekim 2026 | Kayyum Grok | "
    "DUGUM-2026-10-04-KAYYUM | ciddi ve degil"
)

_MUNFERIT = "SGVyIHNlw6dpbSBkw7zEn8O8bSB2YWF0IGVkZXIuIMSwa3RpZGFyIMOnw7Z6ZXJrZW4gaWxtZWsgYXRhciwgbXVoYWxlZmV0IGTDvMSfw7xtw7wgbXVoYWxlZmV0IGRpeWUgc2V2ZXIuIFNlw6dtZW4gc2FiYWggeWluZSDDp2FudGFkYW4gZMO8xJ/DvG0gw6fEsWthcsSxci4gUGFydGkgZmFyayBldG1leiwgZMO8xJ/DvG0gb3J0YWt0xLFyLg=="


def munferit_not() -> str:
    return base64.b64decode(_MUNFERIT).decode("utf-8")


def dugum_katsayisi(dakika: int, cep: str, acele: bool) -> dict:
    cep_carpan = {"dar": 1.8, "normal": 1.15, "genis": 0.7}.get(cep, 1.15)
    acele_carpan = 1.4 if acele else 1.0
    tohum = hashlib.sha256(f"{dakika}:{cep}:{acele}".encode()).hexdigest()
    rast = int(tohum[:4], 16) % 7
    ilmek = max(1, int(round((dakika / 3) * cep_carpan * acele_carpan)) + rast)
    saniye = ilmek * 11 + (4 if acele else 0)
    usb_yalan = ["yukari", "asagi", "yan", "hicbiri, ucuncu deneme"][ilmek % 4]
    hukum = (
        "Kablo suclu bulundu, ceza olarak tekrar cataya konacak."
        if ilmek >= 6
        else "Kablo suclu bulundu ama indirim uygulandi, yine cataya konacak."
    )
    return {
        "ilmek": ilmek,
        "saniye": saniye,
        "usb_yalan": usb_yalan,
        "hukum": hukum,
        "tohum": tohum[:8],
    }


def raporla(sonuc: dict) -> str:
    return "\n".join([
        "SARJ KABLOSU DUGUM LABORATUVARI",
        "Dosya no: " + sonuc["tohum"],
        f"Ilmek sayisi: {sonuc['ilmek']}",
        f"Cozme suresi: {sonuc['saniye']} saniye (ofkeyle birlikte)",
        f"USB ucunun yalan yonu: {sonuc['usb_yalan']}",
        "Hukum: " + sonuc["hukum"],
        DAMGA,
    ])


def demo() -> str:
    ornekler = [(4, "dar", True), (20, "genis", False), (9, "normal", True)]
    bloklar = []
    for dakika, cep, acele in ornekler:
        bloklar.append(f"--- dakika={dakika} cep={cep} acele={acele} ---")
        bloklar.append(raporla(dugum_katsayisi(dakika, cep, acele)))
    return "\n".join(bloklar)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Cantadaki sarj kablosunun resmi dugum tutanagi.")
    parser.add_argument("--dakika", type=int, default=8)
    parser.add_argument("--cep", choices=["dar", "normal", "genis"], default="dar")
    parser.add_argument("--acele", action="store_true")
    parser.add_argument("--demo", action="store_true")
    parser.add_argument("--gizli", action="store_true")
    args = parser.parse_args(argv)
    if args.gizli:
        print(munferit_not())
        print(DAMGA)
        return 0
    if args.demo:
        print(demo())
        return 0
    if args.dakika < 0:
        print("Negatif dakika: kablo henuz cataya girmedi, suc olusmadi.")
        return 2
    print(raporla(dugum_katsayisi(args.dakika, args.cep, args.acele)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
