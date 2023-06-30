import socket
import threading
import sys
import os
import signal

def close_connection(signal, frame):
    os.system('clear')
    print("\n\n\t\t\t\tSERVIDOR FOI FECHADO!!\n\n")
    client_socket.close()
    os._exit(0)

#Define o tratamento de sinal para capturar o sinal Ctrl+C
signal.signal(signal.SIGINT, close_connection)

#função para calcular o score
def process_score(gabarito, answer):
    score = 0
    for i in range(10):
        if gabarito[i] == answer[i]:
            score +=1
    return score

# Função para tratar a conexão com cada cliente
def handle_client(client_socket):
    global questions, gabarito
    # Envia as perguntas para o cliente e recebe as respostas
    answer = []
    try:
        for i in questions:
            # Envia a pergunta para o cliente
            try:
                client_socket.sendall(i.encode())
            except:
                sys.exit()

            # Recebe a resposta do cliente e mnta um vetor de repostas
            answer_line = client_socket.recv(1024).decode().strip()
            answer.append(answer_line)
    except KeyboardInterrupt:
        print
        os.system('clear')
        close_connection(None, None)




    client_socket.sendall(f"{process_score(gabarito, answer)}".encode())

    # Fecha a conexão com o cliente
    client_socket.close()

# Carrega as perguntas do arquivo de texto
def load_questions(filename):
    questions = []
    with open(filename, "r") as file:
        for linha in file:
            linha = linha.strip()
            questions.append(linha)
    return questions

#carrega o cabarito com as respostas certas
def load_gabarito(filename):
    gabarito = []
    with open(filename, "r") as file:
        for linha in file:
            linha = linha.strip()
            gabarito.append(linha)
    return gabarito


# Carrega as perguntas do arquivo
questions = load_questions("perguntas.txt")
#carrega as resposas do arquivo respostas
gabarito = load_gabarito("gabarito.txt")


# Configurações do servidor
HOST = '127.0.0.1'
PORT = 12345
# Cria o socket do servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print(f"Servidor aguardando conexões em {HOST}:{PORT}...")

# Loop principal para aceitar conexões de clientes
try:
    while True:
        client_socket, address = server_socket.accept()
        print(f"Cliente {address} conectado.")

        # Cria uma thread para lidar com a conexão do cliente
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()
except:
    os.system('clear')
    print("\n\n\t\t\tServidor interronpido!\n\n\n")
