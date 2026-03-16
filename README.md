# Echo_Server
This project contains a simple echo server. When the client sends data to the host, it will be returned.
Python version
Run the server first and then the client or checker in another terminal
Run the server in one terminal with something like: python3 echo_server.py
Example command to run in terminal: python3 checker.py 0.0.0.0 9999 30 5 8 40
Where the 0.0.0.0 is the IP adress of the server, 9999 is the server port, 30 is the number of trials to run, 5 is the number
of reads and writes per run, 8 is the max number of bytes to write at a time, and 40 is the number of concurrent connections
I ran something similar to these commands and it printed "Success!"
Note: The # of reads and writes per run cannot be larger than the # of concurrent connections when testing.
Also note: Significant risk of timeout for messages where max number of bytes to write at a time is larger than 1000.
Don't force larger packets onto the server please split into smaller packets.
If you are getting a timeout error, change the timeouts in the checker.py file. This is what I changed them to:
RECV_TOTAL_TIMEOUT = 100
RECV_EACH_TIMEOUT = 10

Libraries needed:
socket
argparse
sys
random
os
time
select
