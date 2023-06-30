import socket
import os
import signal
import sys

# Função para encerrar a conexão com o servidor
def close_connection(signal, frame):
    os.system('clear')
    print("\n\n\t\t\t\tVOCÊ DESISTIU!!\n\n\t\t\tConexão encerrada pelo usuário")
    client_socket.close()
    os._exit(0)

# Configurações do servidor
HOST = '127.0.0.1'
PORT = 12345

# Cria o socket do cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client_socket.connect((HOST, PORT))
except:
    print("\n\t\t\tSrevidor não está ativo, sem conexão!\n\n\n")
    sys.exit()

# Define o tratamento de sinal para capturar o sinal Ctrl+C
signal.signal(signal.SIGINT, close_connection)

# Loop para receber e enviar respostas
os.system('clear')
print("\t\t\t\t\tBEM VINDO AO MEGA QUIZ\n\n\t\t Voce não saberá quais acertou somente a quantidade de acertos.\n\t\t\tResponda somente a aternativa que achar correta.\n\t\tQualquer outro caracter ou número será tratado como incrreto.\n\n\n\t\t\t\t\tVAMOS COMEÇAR!")
i = 1
try:
    for _ in range(10):
        # Recebe a pergunta do servidor
        question = client_socket.recv(1024).decode().strip()

        # Imprime a pergunta e solicita a resposta do usuário
        print(f"\nPergunta {i}: {question}")
        answer = input("Resposta: ")
        os.system('clear')

        # Envia a resposta para o servidor
        try:
            client_socket.sendall(answer.encode())
            i += 1
        except:
            print("\n\t\t\tSEVIDOR FOI ENCERRADO!!")
            sys.exit()

    # Recebe o resultado da resposta do servidor
    result = client_socket.recv(1024).decode().strip()
    print(f"\n\t\t\t\t\t\tSCORE {result}\n\n\n\n")

except KeyboardInterrupt:
    close_connection(None, None)
