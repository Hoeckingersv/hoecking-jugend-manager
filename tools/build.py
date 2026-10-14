import json, os, sys, glob, datetime
dump, out = sys.argv[1], sys.argv[2]
def load(col):
    res = []
    for f in sorted(glob.glob(os.path.join(dump, col, '*.json'))):
        d = json.load(open(f, encoding='utf-8'))
        if isinstance(d, dict) and isinstance(d.get('data'), dict): d = d['data']
        d = dict(d); d['id'] = os.path.basename(f)[:-5]; d.pop('telefon', None); res.append(d)
    return res
ein = {d['id']: d for d in load('einstellungen')}
keep = ['startgeld','befreit','medaillenProTeam','pokaleProJugend','semmelnProTeam','kuchenProJugend','anzahlSemmeln','anzahlBrezen']
z = ein.get('zahlen', {}); turnier = {k: v for k, v in ein.get('turnier', {}).items() if k != 'id'}
daten = {'stand': datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'), 'turnier': turnier, 'zahlen': {k: z[k] for k in keep if k in z}}
for col in ['teams','helfer','einkauf','checkliste','kontakte']: daten[col] = load(col)
daten['posten'] = []
assert turnier and daten['teams']
json.dump(daten, open(os.path.join(out, 'daten.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print('ok', len(daten['teams']))
