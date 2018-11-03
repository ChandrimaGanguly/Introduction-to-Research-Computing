from mpi4py import MPI
import numpy as np

# Set up communication stuff
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

print( "[{}] Starting".format(rank) )

# Create data
data_r = np.empty(5,dtype='int')

if rank==0:
    data_s = np.arange(5*size)
else:
    data_s = None

# Scattering
comm.Scatter(data_s,data_r,root=0)

print("[{}] My data is ".format(rank),data_r)

if rank==3:
    data_s = np.empty(5*size, dtype='int')
# Gather it back up
comm.Gather(data_r,data_s,root=3)

print("[{}] My data now is ".format(rank),data_s)

