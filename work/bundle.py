from pathlib import Path
html=Path('dist/index.html').read_text(encoding='utf-8').replace('<link rel="stylesheet" href="style.css">','<style>'+Path('dist/style.css').read_text(encoding='utf-8')+'</style>').replace('<script src="game.js"></script>','<script>'+Path('dist/game.js').read_text(encoding='utf-8')+'</script>')
Path('outputs/nexus-defense.html').write_text(html,encoding='utf-8')
