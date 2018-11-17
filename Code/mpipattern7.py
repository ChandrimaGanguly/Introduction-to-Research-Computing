"""
Code to compute a 'merge-sort' using MPI
"""
from mpi4py import MPI
import numpy as np
import math

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# calculate how many merge loops we will need
# we have assumed that the number or processors is a power of 2
# otherwise we need to have lots of logic for edge cases
# in our merge tree
levels = int(math.log2(size))

def mergelist(list1,list2):
    """
    Merges two sorted list into one sorted list
    
    
    Parameters
    ----------
    list1: numpy array
        our first sorted list
    list2: numpy array
        our second sorted list
        
    Returns
    ----------
    list3: numpy array
        our merged sorted list
    """
    # get sizes (len works on 1d arrays)
    size1 = len(list1)
    size2 = len(list2)
    size3 = size1+size2
    # create blank list
    list3 = np.empty((size3),dtype='int')
    # i counts list 1, j list 2 and k list3
    i=0
    j=0
    k=0
    #loop over both lists until we reach the end of one
    while i<size1 and j<size2:
        # test which is smaller and add it to list3
        # and increment the counter for that list and list3
        if list1[i]<list2[j]:
            list3[k] = list1[i]
            i+=1
        else:
            list3[k] = list2[j]
            j+=1
        k+=1
    
    # add remaining elements for the list
    # we didn't get to the end of
    while i<size1:
        list3[k] = list1[i]
        i+=1
        k+=1
        
    while j<size2:
        list3[k] = list2[j]
        j+=1
        k+=1
    
    return list3
 
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
    listall = np.random.randint(0,100,(200))
else:
    listall = None
    
if rank==0:
    print("[{}] My send data is ".format(rank),listall)

#scatter orginal list
comm.Scatter(listall,list1,root=0)

# sort our section
list1 = np.sort(list1)

level = 2
# now merge back.  This is a bit fiddly
# we first send from 1mod2 to 0mod2 then from
# 2mod4 to 0mod4  and so on merging at each step
for i in range(1,levels+1):
    if rank%2**i == 2**(i-1):
        dest = rank - 2**(i-1)
        comm.Send(list1, dest=dest, tag=11)
    elif rank%2**i == 0:
        list2 = np.empty((split*2**(i-1)),dtype='int')
        src = rank + 2**(i-1)
        comm.Recv(list2, source=src, tag=11)
        list1 = mergelist(list1,list2)

#print answer
if rank==0:
    print(list1)  