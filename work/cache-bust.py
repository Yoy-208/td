from pathlib import Path

path = Path("dist/index.html")
html = path.read_text(encoding="utf-8")
html = html.replace('href="style.css"', 'href="style.css?v=20260914-radar2"')
html = html.replace('src="game.js"', 'src="game.js?v=20260914-radar2"')
path.write_text(html, encoding="utf-8")
