#!/usr/bin/python
from datetime import datetime, timedelta
import sys

cutoff = datetime.today() - timedelta(days=int(sys.argv[1]))
cutoff = cutoff.strftime('%Y.%m.%d')
print(cutoff)
