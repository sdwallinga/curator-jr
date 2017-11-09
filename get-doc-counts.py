#!/usr/bin/python
from datetime import datetime, timedelta
from elasticsearch import Elasticsearch

# Tenant's info goes here
name_prefix = 'ies'
haproxy_ip = '63.141.41.169'
sla_days = 30

es = Elasticsearch([haproxy_ip], port=9200)

cutoff = datetime.today() - timedelta(days=sla_days)
cutoff = cutoff.strftime('%Y.%m.%d')

indices = sorted(es.indices.get_alias("*"))
toArchive=[]
toSum=[]
sizeSum=0
for i in indices:
  i = i.split('-')
  if (len(i) == 2):
    index = datetime.strptime(i[1], '%Y.%m.%d').strftime('%Y.%m.%d')
    if (index >= cutoff):
      toArchive.append(index)

for i in toArchive:
    target = name_prefix + "-" + i
    count = es.cat.count(index=target, filter_path=['count'])
    size = es.indices.stats(index=target, metric=['store'])
    toSum.append(int(count[0]['count']))
    sizeSum += int(size['indices'][target]['total']['store']['size_in_bytes'])

records = str(sum(toSum))
size = str(sizeSum)

print(f'For the last {sla_days} days:')
print('---------------------')
print(f'Total records: {records}')
print(f'Total size in bytes: {size}b')