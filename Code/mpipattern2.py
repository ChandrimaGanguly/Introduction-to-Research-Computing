"""
This routine sum the triangular double sum of numbers from 1 to imax
using MPI to parallelise the calculation

To ensure load balancing we flatten the loops
"""
from mpi4py import MPI

def divide_loops(loops,size):
    """
    Divides 'loops' into 'size' groups
    
    Divide the number of loops into as close to equal
    size chunks as possible for use with parallelisation
    
    
    Parameters
    ----------
    loops: int
        the number of loops to divide up
    size: int
        the number of groups to break loops into
        
    Returns
    ----------
    start_loop: int
        The loop number to start from
    end_loop: int
        The loop number to stop at 
    """
    # floor division
    loop_rank=loops//size
    # remainder
    auxloop = loops%size
    #calculate start and end
    start_loop = rank*loop_rank
    end_loop = (rank+1)*loop_rank
    
    # allocate remainder across loops
    if(auxloop!=0):
        if (rank < auxloop):
            start_loop = start_loop + rank
            end_loop = end_loop + rank + 1
        else:
            start_loop = start_loop + auxloop
            end_loop = end_loop + auxloop
    # return start and end
    return start_loop, end_loop

def gen(s,e,imax):
    """
    Create generator for part of triangular sum
    
    Parameters
    ----------
    s: int
        the loop number to begin at
    e: int
        the loop number to end at
        
    Returns
    ----------
    None: 
    
    """
    # initilise count
    count = 1
    #triangular loop
    for ii in range(imax):
        for jj in range(ii,imax):
            # gone to far then end
            if count>e:
                break
            # Don't return pair until we have gone s loops
            if count>s:
                yield (ii,jj)
            count += 1

# initilise MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
print( "[{}] Starting".format(rank) )

# double triangular sum numbers from 1 to imax
imax = 100
loops = imax*(imax+1)//2

# divide up the loops
s,e = divide_loops(loops,size)
# create generator for these loops
G1 = gen(s,e,imax)

# compute double sum
x=0
for item in G1:
    x += item[0]+item[1]

print( "[{}] Local sum {}".format(rank,x) )

# combine results using reduce
y = comm.reduce(x,op=MPI.SUM,root=0)

# print output
if rank==0:
    print( "[{}] Total sum {}".format(rank,y) )
