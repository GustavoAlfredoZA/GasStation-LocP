import json

f = open('mexicostates.json',)
data = json.load(f)

for d in data['features']:
    for p in d['properties']:
        print(d['properties'][p])
    print("\n")
f.close()
