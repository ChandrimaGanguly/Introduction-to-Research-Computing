from mpi4py import MPI
import numpy as np

# Set up communication stuff
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

print( "[{}] Starting".format(rank) )

# Send an array (or buffer like object) to all other ranks
data_s = np.random.randint(1,9,(4))
data_r = np.zeros((4), dtype='int')

print( "[{}] Starting with array ".format(rank), data_s )

for i in range(1,size):
    #   Decide who I will send the message to
    #   And who my message will come from
    rank_send = (rank+i)%size
    rank_recv = (rank-i)%size
    #   Send and recieves messages simultaneously
    comm.Sendrecv(data_s, dest=rank_send, recvbuf=data_r, source=rank_recv)
    #   Print what happened
    print("[{}] sent:{} recv:{} Array: ".format(rank,rank_send,rank_recv),data_r)
