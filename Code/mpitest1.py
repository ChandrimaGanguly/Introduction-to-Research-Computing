from mpi4py import MPI

# Set up communication stuff
comm = MPI.COMM_WORLD

# Find out which rank I am
rank = comm.Get_rank()

# Find out how many ranks there are
size = comm.Get_size()

print( "[{}] Starting".format(rank) )

# Send a message to all other ranks
for i in range(1,size):
#   Decide who I will send the message to
#   And who my message will come from
    rank_send = (rank+i)%size
    rank_recv = (rank-i)%size
#   Send the message
    comm.send("Hello from {}".format(rank), dest=rank_send, tag=11)
#   collect my message
    message = comm.recv(source=rank_recv, tag=11)
#   Print what happened
    print("[{}] sent:{} recv:{} Message: {}".format(rank,rank_send,rank_recv,message))
