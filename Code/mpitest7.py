from mpi4py import MPI
import numpy as np

# Set up communication stuff
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

print( "[{}] Starting".format(rank) )

# Send an array (or buffer like object) to all other ranks
data_s = np.random.randint(1,9,(200))
data_r = np.zeros((200), dtype='int')


for i in range(1,size):
#   Decide who I will send the message to
#   And who my message will come from
    rank_send = (rank+i)%size
    rank_recv = (rank-i)%size
#   Send the message, note capital "S"

#   Create recieve
    request = comm.Irecv(data_r, source=rank_recv, tag=11)
#   Create request
    comm.Isend(data_s, dest=rank_send, tag=11)
    
#   Count while I wait for message to arrive
    i=0
    while not request.Get_status():
        i+=1

#   collect my message, note capital "R"
#   Print what happened
print("[{}] while waiting I counted to ".format(rank),i)
