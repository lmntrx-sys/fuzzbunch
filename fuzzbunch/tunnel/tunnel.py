import socket
import select
from logzero import logger

class Forward:
    def __init__(self, src_host, src_port, dst_host, dst_port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Allows immediate restart
        self.sock.bind((src_host, int(src_port)))
        self.sock.listen(5)
        self.target = (dst_host, int(dst_port))

    def exchange_info(self, client, remote):
        while True:
            # select.select watches for which socket has data ready to read
            r, w, e = select.select([client, remote], [], [])

            if client in r:
                data = client.recv(4096)
                logger.debug(f"CLIENT -> REMOTE: {len(data)} bytes")
                remote.sendall(data)
            
            if remote in r:
                data = remote.recv(4096)
                logger.debug(f"REMOTE -> CLIENT: {len(data)} bytes")
                client.sendall(data)

    def run(self):
        try:
            while True: 
                client, addr = self.sock.accept()
                logger.info(f"[NEW] Connection from {addr[0]} forwarded to {self.target[0]}:{self.target[1]}")

                remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
                    remote.connect(self.target)
                    self.exchange_info(client, remote)
                except Exception as e:
                    logger.error(f"Could not connect to target: {e}")
                finally:
                    client.close()
                    remote.close()
                    logger.info(f"[CLOSE] Connection with {addr[0]} finished.")
        except KeyboardInterrupt:
            logger.info("Server stopping...")
        finally:
            self.sock.close()

if __name__ == "__main__":
    import sys
    src_ip, src_port = sys.argv[1].split(':')
    dst_ip, dst_port = sys.argv[2].split(':')
    
    logger.info(f"TCP forwarder starting on {src_ip}:{src_port} -> {dst_ip}:{dst_port}")

    proxy = Forward(src_ip, src_port, dst_ip, dst_port)
    proxy.run()