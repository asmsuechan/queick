import socket
import pickle

from .logger import logger
from .constants import TCP_SERVER_HOST, TCP_SERVER_PORT

class JobReceiver:
    # Start tcp server for listening new job arrival messages
    def listen(self, event, qm):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((TCP_SERVER_HOST, TCP_SERVER_PORT))
        s.listen(1)

        while True:
            conn, addr = s.accept()
            data_bytes = conn.recv(1024)
            if not data_bytes: break

            try:
                data = pickle.loads(data_bytes)
                qm.enqueue(data)
                logger.info('Job received -> data: {}, addr: {}'.format(data, addr))
                response = pickle.dumps({ "success": True, "error": None})
                conn.sendall(response)
                event.set()
            except Exception as e:
                logger.error(str(e))
                response = pickle.dumps({ "success": False, "error": str(e)})
                conn.sendall(response)
        conn.close()
