from pathlib import Path

game_path = Path("dist/game.js")
game = game_path.read_text(encoding="utf-8")
game = game.replace("범위 4칸", "범위 3칸")
game = game.replace("price:40,repeatable:true,radarType:'speedRadar'", "price:25,repeatable:true,radarType:'speedRadar'")
game = game.replace("price:40,repeatable:true,radarType:'attackRadar'", "price:25,repeatable:true,radarType:'attackRadar'")
game = game.replace("Math.hypot(radar.x-t.x,radar.y-t.y)>4", "Math.hypot(radar.x-t.x,radar.y-t.y)>3")
game = game.replace("ctx.arc(radar.x*s,radar.y*s,4*s,0,Math.PI*2)", "ctx.arc(radar.x*s,radar.y*s,3*s,0,Math.PI*2)")
game_path.write_text(game, encoding="utf-8")

html_path = Path("dist/index.html")
html = html_path.read_text(encoding="utf-8")
html = html.replace("범위 4칸", "범위 3칸")
html = html.replace("각 40원", "각 25원")
html = html.replace("20260914-radar2", "20260914-radar3")
html_path.write_text(html, encoding="utf-8")
