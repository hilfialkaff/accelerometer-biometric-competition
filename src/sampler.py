"""
sample.py

Random sample accelerometer data for a device.
"""

import pandas as pd
import random
import sys, getopt

CHUNK_SIZE = 1024

def random_sample(path):
  dids = pd.DataFrame(columns=['Device'])
  for df in pd.read_csv(path, usecols=['Device'] ,chunksize=CHUNK_SIZE):
    df.drop_duplicates()
    dids = pd.concat([dids, df]).drop_duplicates()
  device = random.choice(dids['Device'].values)
  return sample(path, device)

def sample(path, device):
  dinfo = pd.DataFrame(columns=['T','X','Y','Z','Device'])
  for df in pd.read_csv(path, chunksize=CHUNK_SIZE):
    dinfo = pd.concat([dinfo, df[df['Device']== device]])
  return dinfo

def print_sample(path, is_random, device):
  if path is None:
    print 'please enter a path, use -h for help'
    sys.exit(4)
  if is_random:
    random_sample(path).to_csv(sys.stdout, index=False)
  elif not device is None:
    sample(path, device).to_csv(sys.stdout, index=False)
  else:
    print 'please use a random sample or specify device id, use -h for help'

if __name__=='__main__':
  path = None
  device = None
  is_random = False
  argv = sys.argv[1:]

  try:
    opts, args = getopt.getopt(argv, "hp:rs:")
  except getop.GetoptError:
    print 'sampler.py -p <datafile> -r (for random sample) -s <device id> (for sample from "device id")'
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print 'sampler.py -p <datafile> -r (for random sample) -s <device id> (for sample from "device id")'
      sys.exit(3)
    elif opt in ('-p', '--path'):
      path = arg
    elif opt in ('-r', '--random'):
      is_random = True
    elif opt in ('-s', '--sample'):
      device = int(arg)
  # endfor

  print_sample(path, is_random, device)
