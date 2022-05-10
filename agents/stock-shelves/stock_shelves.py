#!/usr/bin/env python3
from rabbitmq import subscriber

config = {
    'host': '172.40.1.13',
    'port': '5672',
    'exchange': 'main.exch',
}


sub = subscriber.Subscriber(config, 'oi')
print("STOCK-SHELVES")
sub.consume_from_queue('stock.shelves')

# Module Imports
import mariadb
import sys

# Connect to MariaDB Platform
try:
    connexion = mariadb.connect(
        user="root",
        password="root",
        host="127.0.0.1",
        port=3307,
        database="Storage"

    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cursor = connexion.cursor()
command = f'SELECT ID_PROD, ID_CATEGORIA, Nome, produto.Quantidade, estoque.quantidade, ' \
          f'lote, origem, Data_fabricacao, Data_vencimento FROM estoque INNER JOIN produto ' \
          f'ON fk_Produto_ID_PROD = ID_PROD INNER JOIN categorias ' \
          f'ON fk_Categorias_ID_CATEGORIA = ID_CATEGORIA;'

cursor.execute(command)
query_result = cursor.fetchall() # Retorna a lista de produtos no estoque
print(query_result)

# Aqui você passa os argumentos para a procedure a ordem seria
# ID_PROD, Quantidade, result -> Deixar 0 por padrão
args = [1, 1, 0]
result_args = cursor.callproc('move_gondula', args)
result = cursor.fetchall()

print(result[0][0])

cursor.close()
cursor = connexion.cursor()

connexion.commit()
cursor.close()
connexion.close()