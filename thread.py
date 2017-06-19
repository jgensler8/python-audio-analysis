import threading
import time

shared_counter = 0

# Define a function for the thread
def print_time( threadName="qwer", delay=2):
   global shared_counter
   while True:
      time.sleep(delay)
      print "=== incr ==="
      shared_counter += 1

def respond_to_key(name="Qwer"):
    print name
    while True:
        raw_input("Hit any key to print shared_counter")
        print shared_counter

# Create two threads as follows
# try:
#    thread.start_new_thread( print_time, ("Thread-1", 2, ) )
#    thread.start_new_thread( respone_to_key, ("qwer"))
# except:
#    print "Error: unable to start thread"
#
# while 1:
#    pass

try:
    t=threading.Thread(target=print_time)
    t.daemon = True  # set thread to daemon ('ok' won't be printed in this case)
    t.start()

    t2=threading.Thread(target=respond_to_key)
    t2.daemon = True
    t2.start()
    t2.join()
    t.join()
except KeyboardInterrupt:
    print "Ctrl-c pressed ..."
    sys.exit(1)
