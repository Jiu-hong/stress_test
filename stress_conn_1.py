# import modules
from threading import *

from stress_conn import start_sidecar

# creating a thread
threads_list = [Thread(target=start_sidecar, args=(x,),
                       daemon=True) for x in range(5)]

# starting of Thread T
[x.start()for x in threads_list]
[x.join()for x in threads_list]
print('this is Main Thread')
