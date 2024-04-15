import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('8.8.8.8', 80))

print(s.getsockname()[0])

# para acessar o conteúdo do servidor em outro dispositivo,
# rodar o comando:
# task run_local

# acessar em outro dispositivo na mesma rede:
# http://<ip-informado-no-print>:8000/
