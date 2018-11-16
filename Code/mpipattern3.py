"""
This is a master slave MPI code for calculating n(n+1)/2 for a set of n
The communication code is quite general however
"""
from mpi4py import MPI

# 0 is master
# rest are slaves

# intiilise MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Master rank section
if rank==0:
    # define list of tasks
    tasklist = (i for i in range(10))
    
    #set count of finished ranks
    finished = 0
    
    #create status object for MPI_probe
    status = MPI.Status()
    
    #initial allocation of jobs
    for i in range(1,size):
        # check there are enough jobs for the number of ranks
        # -1 is a flag to say "no more work" 
        try:
            message = next(tasklist)
        except StopIteration:
            message = -1
        
        # now we send initial job ID's to slaves
        print("[{}] Sending task: {} to rank {}".format(rank,message,i))
        comm.isend(message, dest=i, tag=i)

    # Now we check for messages from complete jobs
    # then allocate new jobs to the slaves
    while finished<size-1:
        # Check for waiting messages with probe 
        flag = comm.iprobe(status=status, source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG)
        
        # if a message is waiting then enter this loop to recieve it
        if flag==True:
            # status object stores the origin of the message (and tag etc..)
            source = status.source
            #recv the message
            test = comm.irecv(source=source, tag=source)
            reply = test.wait()
            print("[{}] Recieving result: {} from rank {}".format(rank,reply,source))
            
            # now check the reply, -1 means the slave receieved a -1 and it's letting
            # us know that it's finished so we add it to our finshed count
            # otherwise we send it its next job ID (which may be -1 if there are 
            # no more jobs)
            if reply==-1:
                finished +=1
                print("[{}] Recieved termination finished count: {}".format(rank,finished))
            else:
                print("[{}] Done with result {}".format(rank,reply))
                try:
                    message = next(tasklist)
                except StopIteration:
                    message = -1
                print("[{}] Sending task: {} to rank {}".format(rank,message,i))
                comm.isend(message, dest=source, tag=source)

# Slave ranks section
else:
    # this loop keeps us checking for jobs until we recieve a -1
    while True:
        # recvout next job ID
        test = comm.irecv(source=0, tag=rank)
        task = test.wait()
        print("[{}] Recieving task: {} from rank {}".format(rank,task,0))
        
        # is job ID = -1 then no more jobs and we can stop
        # We let the master know we are stopping by sending -1 back
        # Otherwise we do the job associated with the ID we recieve
        if task==-1:
            comm.isend(-1, dest=0, tag=rank)
            print("[{}] Sending termination to rank {}".format(rank,0))
            break
        else:
            # This single line is the actual job
            result = task*(task+1)//2
            
            # now we send our result back to the master
            comm.isend(result, dest=0, tag=rank)
            print("[{}] Sending result {} to rank {}".format(rank,result,0))

# Finished message
print("[{}] I'm done".format(rank))
