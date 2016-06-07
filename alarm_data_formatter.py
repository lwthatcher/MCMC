import json

file_name = 'noz_alarm_dif.txt'
out_file_name = 'alarm-gen-noz.json'

with open(file_name, 'r') as f:
    data = json.load(f)

out_data = []
for row in data:
    d = {'B': row[0], 'E': row[1], 'A': row[2], 'J': row[3], 'M': row[4]}
    out_data.append(d)

with open(out_file_name, 'w') as of:
    json.dump(out_data, of)
