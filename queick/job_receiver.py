import socket
import pickle

from .logger import logger

class JobReceiver:
    # Start tcp server for listening new job arrival messages
    def listen(self, event, qm):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('127.0.0.1', 9999))
        s.listen(1)

        while True:
            conn, addr = s.accept()
            data_bytes = conn.recv(1024)
            if not data_bytes: break

            try:
                data = pickle.loads(data_bytes)
                qm.enqueue(data)
                event.set()
                logger.info('Job received -> data: {}, addr: {}'.format(data, addr))
                response = pickle.dumps({ "success": True, "error": None})
                conn.sendall(response)
            except Exception as e:
                logger.error(str(e))
                response = pickle.dumps({ "success": False, "error": str(e)})
                conn.sendall(response)
        conn.close()
