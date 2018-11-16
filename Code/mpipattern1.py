"""
This routine sum the numbers from 1 to loops
using MPI to parallelise the calculation
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

# initilise MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
print( "[{}] Starting".format(rank) )

# number to sum to
loops = 1000

# divide number across processors
s,e = divide_loops(loops,size)

# perform partial sums for each section
x=0
for i in range(s,e):
    x += i+1

print( "[{}] Local sum {}".format(rank,x) )

# combine results using reduce
y = comm.reduce(x,op=MPI.SUM,root=0)

# print output
if rank==0:
    print( "[{}] Total sum {}".format(rank,y) )
