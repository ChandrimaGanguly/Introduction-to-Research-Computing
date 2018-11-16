"""
A very simple domain decomposition code to multiple matricies in parallel
ie: M(mm,5) . N(5,5) in parallel using MPI
"""
from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# The long matrix dimension
mm = 100
# divide this by number of processors
# we have made no allowances for remainder
# in a prefect world we would keep track of this
# and pad our matrixies accordingly
split = mm//size
 
# Object to recv matrix from scatter
matrix_M_r = np.empty((split,5),dtype='int')

# matric to multiply the large one by
matrix_N = np.arange(1,26).reshape((5,5))

# Initilise the large matrix on rank 0
if rank==0:
    matrix_M_s = np.array([range(i,i+5) for i in range(mm)])
else:
    matrix_M_s = None
    
if rank==0:
    print("[{}] My send data is ".format(rank),matrix_M_s)

# Scatter the large matric to all ranks
comm.Scatter(matrix_M_s,matrix_M_r,root=0)

print("[{}] My recv data is: ".format(rank),matrix_M_r)

# compute multiplication
matrix_M_r = np.dot(matrix_M_r,matrix_N)

# gather reults back together
comm.Gather(matrix_M_r,matrix_M_s,root=0)
    
if rank==0:
    print("[{}] My gath data is \n".format(rank),matrix_M_s)


