#!/usr/bin/env python3
"""Build the standalone web release from src/game.html.

src/game.html is the single-file game as published in the Claude artifact (no <html>/<head>).
This wraps it into a full document with PWA metadata, writes public/index.html,
and packs dist/starmarch-web.zip for itch.io (index.html at the zip root).
"""
import pathlib, re, zipfile, hashlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
src = (ROOT / "src/game.html").read_text(encoding="utf-8")
src = re.sub(r'<meta name="claude:[^>]*>\n?', "", src)

cut = src.index("</style>") + len("</style>")
head_part, body_part = src[:cut], src[cut:]

HEAD = """<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover,user-scalable=no">
<meta name="description" content="リアルタイムで銀河を奪い合う、全自動寄りの宇宙戦略ゲーム。">
<meta name="theme-color" content="#070b22">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Starmarch">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" type="image/png" sizes="192x192" href="icons/icon-192.png">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
"""
SW = """
<script>
// Offline support when served from our own site (GitHub Pages / PWA). Harmless elsewhere.
if('serviceWorker' in navigator&&location.protocol==='https:'&&!/itch\\.(io|zone)$/.test(location.hostname)){
  addEventListener('load',()=>navigator.serviceWorker.register('sw.js').catch(()=>{}));
}
</script>
"""
out = HEAD + head_part + "\n</head>\n<body>\n" + body_part + SW + "</body>\n</html>\n"
pub = ROOT / "public"
(pub / "index.html").write_text(out, encoding="utf-8")

# bump the service worker cache name whenever the game changes
ver = hashlib.sha1(out.encode()).hexdigest()[:10]
sw = (ROOT / "tools/sw.template.js").read_text(encoding="utf-8").replace("__VERSION__", ver)
(pub / "sw.js").write_text(sw, encoding="utf-8")

dist = ROOT / "dist"; dist.mkdir(exist_ok=True)
with zipfile.ZipFile(dist / "starmarch-web.zip", "w", zipfile.ZIP_DEFLATED) as z:
    for f in sorted(pub.rglob("*")):
        if f.is_file() and not f.name.startswith("."):
            z.write(f, f.relative_to(pub).as_posix())
print("built", pub / "index.html", f"({len(out)//1024} KB)", "sw", ver, "->", dist / "starmarch-web.zip")
