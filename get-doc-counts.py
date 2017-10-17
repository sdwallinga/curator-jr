#!/usr/bin/python
from datetime import datetime, timedelta
from elasticsearch import Elasticsearch
import subprocess

# Tenant's info goes here
name_prefix = '5thc'
haproxy_ip = '172.27.101.27'
sla_days = 30

es = Elasticsearch([haproxy_ip], port=9200)

cutoff = datetime.today() - timedelta(days=sla_days)
cutoff = cutoff.strftime('%Y.%m.%d')

indices = sorted(es.indices.get_alias("*"))
toArchive=[]
toSum=[]
for i in indices:
  i = i.split('-')
  if (len(i) == 2):
    index = datetime.strptime(i[1], '%Y.%m.%d').strftime('%Y.%m.%d')
    if (index >= cutoff):
      toArchive.append(index)

for i in toArchive:
    count = es.cat.count(index=name_prefix + "-" + i, filter_path=['count'])
    toSum.append(int(count[0]['count']))

print(sum(toSum))
