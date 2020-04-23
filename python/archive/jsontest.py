import json
from datetime import datetime
now = datetime.now()
print(now)
date_time = now.strftime("%m/%d/%Y, %H:%M:%S.%f")
print("date and time:",date_time)

data = {}
data['people'] = []
data['people'].append({
    'name': 'Scott',
    'website': 'stackabuse.com',
    'from': 'Nebraska',
    'date_time': date_time

})
data['people'].append({
    'name': 'Larry',
    'website': 'google.com',
    'from': 'Michigan',
    'date_time': date_time

})
data['people'].append({
    'name': 'Tim',
    'website': 'apple.com',
    'from': 'Alabama',
    'date_time': date_time

})

with open('data.txt', 'w') as outfile:
    json.dump(data, outfile)