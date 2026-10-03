#!/usr/bin/env python3
import html
import hashlib
import json
import re
from pathlib import Path


root = Path(__file__).resolve().parent
version = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()[:10]
runs = json.loads((root / "results.json").read_text())
docs = root / "docs"
docs.mkdir(exist_ok=True)
(docs / ".nojekyll").touch()
cards = []
horses = [run for run in runs if (root / "results" / run["name"] / "index.html").exists()]


def navigation(run):
    index = horses.index(run)
    previous = horses[(index - 1) % len(horses)]["name"]
    following = horses[(index + 1) % len(horses)]["name"]
    icons = {
        "Previous horse": '<path d="m15 18-6-6 6-6"/>',
        "Gallery": '<rect x="3" y="3" width="6" height="6" rx="1"/><rect x="15" y="3" width="6" height="6" rx="1"/><rect x="3" y="15" width="6" height="6" rx="1"/><rect x="15" y="15" width="6" height="6" rx="1"/>',
        "Next horse": '<path d="m9 18 6-6-6-6"/>',
    }
    buttons = "".join(
        f'<a href="{href}" aria-label="{label}" title="{label}"><svg aria-hidden="true" viewBox="0 0 24 24">{icons[label]}</svg></a>'
        for label, href in [("Previous horse", f"../{previous}/?v={version}"), ("Gallery", f"../?v={version}"), ("Next horse", f"../{following}/?v={version}")]
    )
    label = html.escape(f'{run["harness"]} · {run["model"]} · {run["effort"]}')
    content = f"""<style>
:host{{position:fixed;bottom:max(20px,env(safe-area-inset-bottom));left:50%;transform:translateX(-50%);z-index:2147483647;max-width:calc(100vw - 24px);font:12px system-ui,sans-serif;color:#e9eddf}}
nav{{display:flex;align-items:center;gap:8px;background:rgba(16,21,16,.9);border:1px solid #53624b;border-radius:18px;padding:8px;box-shadow:0 6px 30px #0004;backdrop-filter:blur(12px)}}
a{{display:grid;place-items:center;width:44px;height:44px;flex-shrink:0;color:#d9ef8c;border-radius:12px;text-decoration:none}}a:hover{{background:#344034}}a:focus-visible{{outline:2px solid #d9ef8c;outline-offset:1px}}svg{{width:22px;height:22px;fill:none;stroke:currentColor;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}}
.info{{min-width:0;max-width:330px;padding:0 8px}}.model{{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}.count{{color:#aab4a4;margin-top:4px}}@media(max-width:520px){{.info{{max-width:140px}}}}
</style><nav aria-label="Horse navigation">{buttons}<div class="info"><div class="model" title="{label}">{label}</div><div class="count">{index + 1} / {len(horses)}</div></div></nav>"""
    return '<script>(()=>{const host=document.createElement("div");host.id="horse-bench-overlay";host.attachShadow({mode:"open"}).innerHTML=' + json.dumps(content).replace("<", "\\u003c") + ';document.body.append(host)})();</script>'


for run in runs:
    name = run["name"]
    source = root / "results" / name / "index.html"
    metadata = "".join(
        f"<dt>{label}</dt><dd>{html.escape(str(run.get(key) or 'default'))}</dd>"
        for key, label in [("harness", "Harness"), ("model", "Model"), ("effort", "Effort"), ("provider", "Provider")]
    )
    if source.exists():
        destination = docs / name
        destination.mkdir(exist_ok=True)
        original = source.read_text()
        viewport = '<meta name="viewport" content="width=device-width, initial-scale=1">'
        index = horses.index(run)
        prefetch = ''.join(
            f'<link rel="prefetch" href="../{horses[neighbor % len(horses)]["name"]}/?v={version}" as="document">'
            for neighbor in [index - 1, index + 1]
        )
        original = re.sub(r'<meta\b[^>]*\bname\s*=\s*[\"\']viewport[\"\'][^>]*>', '', original, flags=re.IGNORECASE)
        original = re.sub(r'<head\b[^>]*>', lambda match: match.group() + '\n' + viewport + '\n' + prefetch, original, count=1, flags=re.IGNORECASE)
        published = re.sub(r"</body\s*>", lambda match: navigation(run) + match.group(), original, count=1, flags=re.IGNORECASE)
        (destination / "index.html").write_text(published)
        action = f'<a href="{html.escape(name)}/?v={version}">Open horse <span aria-hidden="true">↗</span></a>'
    else:
        action = f'<p class="failure">{html.escape(run.get("failure") or "No HTML returned")}</p>'
    cards.append(f'<article data-harness="{html.escape(run["harness"])}"><h2>{html.escape(name)}</h2><dl>{metadata}</dl>{action}</article>')
count = sum((root / "results" / run["name"] / "index.html").exists() for run in runs)
page = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Horse Bench</title>
<style>
:root{color-scheme:dark;font:16px system-ui,sans-serif;background:#101510;color:#e9eddf}*{box-sizing:border-box}body{max-width:1250px;margin:auto;padding:48px 24px}header{margin-bottom:36px}h1{font-size:clamp(38px,7vw,72px);letter-spacing:-.055em;margin:0 0 12px}header p{max-width:750px;color:#aab4a4;line-height:1.6}a{color:#d9ef8c;text-decoration:none}a:hover{text-decoration:underline}.count{font-size:13px;text-transform:uppercase;letter-spacing:.12em;color:#d9ef8c}nav{display:flex;gap:8px;flex-wrap:wrap;margin:28px 0}button{background:#1b231b;color:#bfc9b6;border:1px solid #344034;border-radius:24px;padding:9px 16px;font:inherit;cursor:pointer}button[aria-pressed=true]{color:#101510;background:#d9ef8c;border-color:#d9ef8c}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(290px,1fr));gap:16px}article{background:#192019;border:1px solid #303b2e;border-radius:14px;padding:24px;display:flex;flex-direction:column;min-width:0}article[hidden]{display:none}h2{font-size:17px;margin:0 0 20px;overflow-wrap:anywhere}dl{display:grid;grid-template-columns:70px 1fr;gap:10px;margin:0 0 24px;font-size:14px}dt{color:#879781}dd{margin:0;overflow-wrap:anywhere}article a{margin-top:auto;display:block;border-top:1px solid #303b2e;padding-top:16px}.failure{color:#d9aa88;font-size:14px;line-height:1.5;margin-top:auto}footer{font-size:13px;color:#879781;line-height:1.6;margin-top:36px}details{margin-top:18px;color:#aab4a4;line-height:1.6}summary{cursor:pointer}blockquote{margin:12px 0;max-width:850px}
</style>
</head>
<body>
<header><p class="count">__COUNT__ / __TOTAL__ generated</p><h1>Horse Bench</h1><p>One running horse prompt, multiple coding harnesses and models. Open a run to see its HTML. Each card records the exact configuration requested.</p><details><summary>The prompt</summary><blockquote>Create a low-poly 3D horse running in a seamless loop using Three.js. Build it procedurally from primitive geometry, animate the legs, body, head, and tail, and return a single self-contained HTML file.</blockquote></details></header>
<nav aria-label="Filter by harness">__FILTERS__</nav>
<main>__CARDS__</main>
<footer>Effort “default” means no effort override was supplied. Generated HTML loads Three.js from a CDN and needs internet access. <a href="https://github.com/0x7067/horse-bench">Code and results</a>.</footer>
<script>
document.querySelectorAll('nav button').forEach(button=>button.addEventListener('click',()=>{document.querySelectorAll('nav button').forEach(item=>item.setAttribute('aria-pressed',String(item===button)));document.querySelectorAll('article').forEach(card=>card.hidden=button.dataset.harness!=='all'&&card.dataset.harness!==button.dataset.harness)}));
</script>
</body>
</html>
"""
filters = ''.join(f'<button data-harness="{name}" aria-pressed="{str(name == "all").lower()}">{name.title()}</button>' for name in ["all", *dict.fromkeys(run["harness"] for run in runs)])
page = page.replace("__COUNT__", str(count)).replace("__TOTAL__", str(len(runs))).replace("__FILTERS__", filters).replace("__CARDS__", "\n".join(cards))
(docs / "index.html").write_text(page)
print(f"Built index and {count} horse pages in {docs}")
