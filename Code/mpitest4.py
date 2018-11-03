from mpi4py import MPI

# Set up communication stuff
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

print( "[{}] Starting".format(rank) )

#initilise the data only on rank 0
if rank==0:
    data = "0 is the best rank"
else:
    data = None

#Send the data to all other ranks
data = comm.bcast(data, root=0)

print("[{}] I just heard that {}".format(rank,data) )
