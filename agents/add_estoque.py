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

command = f'SELECT ID_PROD, ID_CATEGORIA, Nome, Quantidade, lote, origem, Data_fabricacao, Data_vencimento  ' \
          f'FROM produto ' \
          f'INNER JOIN categorias ' \
          f'ON fk_Categorias_ID_CATEGORIA = ID_CATEGORIA'
cursor.execute(command)
query_result = cursor.fetchall() # Retorna a lista de produtos geral
print(query_result)

# Aqui você passa os argumentos para a procedure a ordem seria
# ID_PROD, ID_CATEGORIA, Quantidade, Data_fabricacao,
# Data_vencimento, lote, origem , result -> Deixar 0 por padrão
args = [1, 1, 1, "2001-01-22", "2010-10-23", 17, "Nestlé Campinas", 0]
result_args = cursor.callproc('recebe_produto', args)
result = cursor.fetchall()

print(result[0][0])

cursor.close()
cursor = connexion.cursor()

connexion.commit()


cursor.close()
connexion.close()