#!/usr/bin/env python3
"""Usage: python3 build.py <base-url> [--qr]
Reads game.js, builds <base-url>#<encoded game>, prints it, optionally saves qr.png"""
import sys, pathlib, urllib.parse

args = [a for a in sys.argv[1:] if not a.startswith("--")]
base = args[0] if args else "http://localhost:8000/"
js = pathlib.Path(__file__).with_name("game.js").read_text(encoding="utf8").strip()
# keep only URL-safe punctuation literal; encode < > | " ` etc. so scanners/browsers don't choke
frag = urllib.parse.quote(js, safe="()=,;:._*'!-/?+@$&")
url = f"{base}#{frag}"
print(url)
print(f"\n{len(url)} characters in QR", file=sys.stderr)

if "--qr" in sys.argv:
    import qrcode
    q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L, border=4, box_size=10)
    q.add_data(url)
    q.make(fit=True)
    q.make_image(fill_color="black", back_color="white").save("qr.png")
    print(f"saved qr.png (QR version {q.version}, {q.modules_count}x{q.modules_count} modules)", file=sys.stderr)
