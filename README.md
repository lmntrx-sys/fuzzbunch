## Workings of a proxy server

This repo dives into the creation of tunnels i.e proxies.
VPNs use the same principle to create a connection between the client and the server

For you to see this working 
  1. Open three instances of your terminal i.e server, client, proxy.
  2. Fisrt you will run the script `` python3 Forwarder.py 127.0.0.1:1337 127.0.0.1:1234`` This will start the proxy server.
  3. On the client side you will need netcat ``nc -l 1227`` that (port)number is dependent on what you input in the server.
  4. Now on the server side you will create the port in which to connect to `` nc 127.0.0.1 13337 ``.

When you type something on the client or server side you will see the message on the other side, depending on where you typed

# I will also try to implement some ecryption (From scartch)
