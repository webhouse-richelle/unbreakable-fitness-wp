import sys, re
raw = open(sys.argv[1], encoding='utf-8', errors='ignore').read()
parts = raw.split('<script')
blocks = []
for p in parts[1:]:
    head = p.split('>', 1)
    if len(head) < 2:
        continue
    body = head[1].split('</script>', 1)[0]
    blocks.append((head[0], body))

xdc = [b for a, b in blocks if '<x-dc>' in b]
comp = [b for a, b in blocks if 'class Component' in b]

def unesc(s):
    s = re.sub(r'\\u([0-9a-fA-F]{4})', lambda m: chr(int(m.group(1), 16)), s)
    s = s.replace('\\n', '\n').replace('\\t', '\t')
    s = s.replace('\\"', '"').replace("\\'", "'")
    s = s.replace('\\/', '/')
    s = s.replace('\\\\', '\\')
    return s

m = unesc(xdc[0])
c = unesc(comp[0]) if comp else ''
open('design_markup.html', 'w', encoding='utf-8').write(m)
open('design_component.js', 'w', encoding='utf-8').write(c)
print("markup bytes:", len(m))
print("component bytes:", len(c))
