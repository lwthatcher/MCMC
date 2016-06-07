import json
import random

model = '01'
p = 0.25

file_name = 'alarm-gen-' + model + '.json'
with open(file_name, 'r') as f:
    data = json.load(f)

for row in data:
    for key in row:
        u = random.random()
        if u > 1-p:
            row[key] = 'x'

P = p*100
out_file_name = 'alarm-gen-' + model + '_' + str(int(P)) + '.json'
with open(out_file_name, 'w') as of:
    json.dump(data, of)
