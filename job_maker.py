import re
import os
from sys import argv
import math

def main():

  #choices of names
  names = ["openmp","mpi","serial"]

  num_ints = 1000000000
  num_iters = 1

  #List of processors
  procs = {"openmp":[1,2,4,8],"mpi":[1,2,4,8,16,32,64],"serial":[1]}
  dir = "/g/home/sbolding/prefix_sum/"
  execs = {"openmp":(dir+"psum_openmp"),"mpi":(dir+"psum_mpi"),"serial":(dir+"psum_serial")}
  
  if len(argv)<5:
    raise IOError("Usage -i <name> -n <num_iters>")

  #Get the root program_name and index
  for name in argv:

    if name == "-i":
      code = argv[argv.index(name)+1]

    elif name == "-n":
      num_runs = int(argv[argv.index(name)+1])
 
  if code not in names:
    raise ValueError("Invalid name, use syntax -i <name>, name choices are: openmp, mpi")

  #Create job files
  for i in procs[code]:

    f_name = code + "_submit_"+str(i)+".job"
    print "Creating job file "+f_name, "and submitting to eos..."
    print "...will execute %s %i times\n" % (execs[code],num_runs)
    f = open(f_name,"w")

    #nodes per core
    ppn = min(i,8)
    nodes = int(math.ceil(float(i)/8.))
    f.write("#PBS -l nodes=%i:nehalem:ppn=%i\n"%(nodes,ppn))
    f.write("#PBS -l walltime=00:20:00\n")
    f.write("#PBS -l mem=22gb\n")
    f.write("#PBS -N %s%i\n" % (code+"_out_",i))
    f.write("#PBS -S /bin/bash\n")
    f.write("#PBS -W NACCESSPOLICY:SINGLEJOB\n")
    f.write("#PBS -j oe\n")
    f.write("#\n\n")
    f.write("# $PBS_O_WORKDIR is the directory from which the job was submitted\n")
    f.write("cd $PBS_O_WORKDIR\n\n")
    
    #Print execution commands
    for j in range(num_runs):
    
      if code == "openmp":
        string = "OMP_NUM_THREADS=%i"% (i)
      elif code == "mpi":
        string = "mpirun -n %i" % (i)
      elif code == "serial":
        string = ""

      string += " %s %i %i" % (execs[code],num_ints,num_iters)

      f.write(string+"\n")
  
    f.close()


  
  
  


if __name__ == "__main__":
  main()
 
