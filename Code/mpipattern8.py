"""
Code to compute a cumulitive sum using MPI after reacting the problem
"""
from mpi4py import MPI
import numpy as np
import math

# initilise
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# calculate how many send loops we will need
# we have assumed that the number or processors is a power of 2
# otherwise we need to have lots of logic for edge cases
# in our merge tree
levels = int(math.log2(size))

# set list length
length = 200
# divide this by number of processors
# we have made no allowances for remainder
# in a prefect world we would keeep track of this
# and pad our arrays accordingly
split = length//size

# create list to recv data from scatter
list1 = np.empty((split),dtype='int')

# create long list on rank 0
if rank==0:
    listall = np.random.randint(0,100,(length))
else:
    listall = None
    
if rank==0:
    print("[{}] My send data is ".format(rank),listall)

#scatter orginal list   
comm.Scatter(listall,list1,root=0)

# compute cumulitive sum for our section
x=0
for index, item in enumerate(list1):
     x += item
     list1[index] = x

# now send cum sum to other ranks.  This is a bit fiddly
# we first send from 1mod2 to 0mod2 then from
# 2mod4 to 0mod4  and so on adding the new section on at each setp    
for i in range(1,levels+1):
    if rank%2**i == 0:
        dest = rank + 2**(i-1)
        comm.send(list1[-1], dest=dest, tag=11)
    elif rank%2**i == 2**(i-1):
        src = rank - 2**(i-1)
        x = comm.recv(source=src, tag=11)
        list1 = list1+x

# gather the cumultive sums back together
comm.Gather(list1,listall,root=0)

# output result
if rank==0:
    print(listall)