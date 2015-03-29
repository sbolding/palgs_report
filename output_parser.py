import re, os
from numpy import mean, array, std
import numpy
from math import sqrt
import matplotlib as plt
from pylab import *


def main():
  names = []
  serial_file = None
  for i in os.listdir("."):

    if re.search("_out_",i):
      if re.search("swp$",i):
        continue  
      if re.search("serial",i):
        serial_file = i
      else:
        names.append(i)

  print "Found these files"
  print names+[serial_file]

  #compute data
  data = {}
  for f in names+[serial_file]:

      avg, std, size = parseFile(f)

      #Find like names
      m = re.search("(\w+)_out_(\d+)",f)
      root_name = m.group(1)
      num = int(m.group(2)) #num procs

      if root_name not in data:

        data[root_name] = []

      data[root_name].append((num,avg,1.96*std))

       

  count = 0
  for key,val in data.iteritems():

    if re.search("serial",key):
      continue

    #sort val
    val = sorted(val, key=lambda d: d[0])
   
    #Calculate speed up
    seq_time = data["serial"][0][1]
    spdup = [seq_time/i[1] for i in val]
    p = [i[0] for i in val]
    
    #plot speedup
    count+=1
    print p
    print spdup
    plt.plot(p,spdup,label=key)
    plt.legend(loc="lower right")
  plt.show()

#parse each file
def parseFile(name):

  f = open(name, "r")
  times = []
  for line in f:

    if re.search("Prefix summation",line):

      m = re.search("(\d+)\s\(usec\)",line)
      times.append(float(m.group(1)))

  avg = sum(times)/(1.*len(times))
  N = len(times)
  times = array(times)
  std = numpy.std(times)/sqrt(N-1)

  return avg, std, len(times)

if __name__ == "__main__":
  main()



