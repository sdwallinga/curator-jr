#!/usr/bin/python
# Depends on elasticdump (npm install -g elasticdump)
from datetime import datetime, timedelta
from elasticsearch import Elasticsearch
from pathlib import Path
import subprocess

# Tenant's info goes here
name_prefix = ''
haproxy_ip = ''
sla_days = 90
archive_directory = '/home/ubuntu/archive'

es = Elasticsearch([haproxy_ip], port=9200)

cutoff = datetime.today() - timedelta(days=sla_days)
cutoff = cutoff.strftime('%Y.%m.%d')

indices = sorted(es.indices.get_alias("*"))
toArchive=[]
for i in indices:
  i = i.split('-')
  if (len(i) == 2):
    index = datetime.strptime(i[1], '%Y.%m.%d').strftime('%Y.%m.%d')
    if (index <= cutoff):
      toArchive.append(index)

print(toArchive)

for index in toArchive:
  index = name_prefix + "-" + index
  path = archive_directory + "/" + index + ".json"
  if (Path(path).is_file()) or (Path(path + ".gz").is_file()):
      continue;
  else:
    ed_input = "--input=http://" + haproxy_ip + ":9200/" + index
    ed_output = "--output=" + path
    subprocess.call(["elasticdump", ed_input, ed_output])
    subprocess.call(["gzip", path])
    es.indices.delete(index=index, ignore=[400, 404])
