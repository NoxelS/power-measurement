import json

with open('data.json') as json_file:
    data = json.load(json_file)
    for p in data['messdaten']:
        print('Date: ' + p['date'])
        print('Time: ' + p['time'])
        print('Voltage: ' + p['voltage'])
        print('Power: ' + p['power'])
        print('Channel: ' +p['channel'])
        print('')