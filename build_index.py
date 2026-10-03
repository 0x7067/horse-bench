#!/usr/bin/env python3
import html
import json
import shutil
from pathlib import Path


root = Path(__file__).resolve().parent
runs = json.loads((root / "results.json").read_text())
docs = root / "docs"
docs.mkdir(exist_ok=True)
(docs / ".nojekyll").touch()
cards = []
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
        shutil.copyfile(source, destination / "index.html")
        action = f'<a href="{html.escape(name)}/">Open horse <span aria-hidden="true">↗</span></a>'
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
