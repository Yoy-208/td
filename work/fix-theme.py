from pathlib import Path
p=Path('work/portable.py')
s=p.read_text(encoding='utf-8')
old='css=re.sub(r"@import\\s+url\\([^;]+;\\s*",\'\',css)'
new='css=re.sub(r"@import\\s+url\\([^)]*\\)\\s*;\\s*",\'\',css)'
assert old in s
s=s.replace(old,new)
s=s.replace("assert not re.search(r'https?://|@import|url\\(',css)", "assert not re.search(r'https?://|@import|url\\(',css)\nassert css.lstrip().startswith(':root{color-scheme:dark;--bg:#0b1119;')\nassert 'display=swap' not in css\nassert 'body{margin:0;background:var(--bg);color:#eef3f9;' in css")
p.write_text(s,encoding='utf-8')
