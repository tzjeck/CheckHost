Check Host status
=================

Check host status and push response to the Xively

Usage: chk.py [ -f filename] [ -i ip-address] 
File format -> id;ip

Using parameter -i you will not push result to the Xively.

-----------------
example:
 -  python chk.py -i ip-addr(IPv4||IPv6) 
 -  python chk.py -f ip.file   


ip.file


host_1;(IPv4||IPv6) 
host_2;(IPv4||IPv6) 
host_3;(IPv4||IPv6) 

