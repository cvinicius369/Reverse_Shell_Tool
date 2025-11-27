import socket
import sys
import argparse
import os

def start_client():
    parser = argparse.ArgumentParser(description="Client remote shell in python.")
    parser.add_argument('target_ip', type=str, help='O endereço IP do servidor remoto (ex: 203.0.113.45)')
    parser.add_argument(
        '-p', '--port', type=int, default=4444, help='A porta do servidor remoto (padrão: 4444)'
    )
    args = parser.parse_args()
    SERVER_IP = args.target_ip
    SERVER_PORT = args.port
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print(f" Tentando conectar a {SERVER_IP}:{SERVER_PORT}...")

    try:
        client.connect((SERVER_IP, SERVER_PORT))
        print(f"Conexão estabelecida com o servidor remoto.")

        while True:
            data = client.recv(4096).decode('utf-8')
            if not data:
                print("\nServidor fechou a conexão.")
                break
            print(data, end="", flush=True)
            if data.strip().endswith('$') or data.strip().endswith('#'):
                try:
                    command = input()
                except EOFError:
                    command = 'exit'
                    print("exit")
                
                if not command:
                    client.sendall(b"\n")
                    continue
                client.sendall((command + '\n').encode('utf-8'))
                if command.lower() == 'exit':
                    break
    except ConnectionRefusedError:
        print(f"Conexão recusada.")
        sys.exit(1)
    except socket.gaierror:
        print(f"Erro de endereço. IP ou hostname inválido: {SERVER_IP}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nSinal de interrupção (Ctrl+C) recebido. Encerrando...")
    except Exception as e:
        print(f"\nUm erro inesperado ocorreu: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    start_client()