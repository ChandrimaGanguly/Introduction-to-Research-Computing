from mpi4py import MPI
import numpy as np

# Set up communication stuff
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

print( "[{}] Starting".format(rank) )

# Create data
data_s = np.random.randint(1,9,(5))
data_r = np.empty(5,dtype='int')

print( "[{}] Starting with data: ".format(rank),data_s )

comm.Reduce(data_s,data_r,op=MPI.SUM,root=0)

if rank==0:
    print("summed data: ",data_r)
