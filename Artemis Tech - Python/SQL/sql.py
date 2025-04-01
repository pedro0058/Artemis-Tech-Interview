import sqlite3
import pandas as pd

query_1 = """
SELECT 
    c.Nome,
    p.PedidoID,
    p.DataPedido,
    p.ValorTotal
FROM
    clientes c
LEFT JOIN pedidos p 
    ON c.ClienteID = p.ClienteID
"""
query_2 = """
SELECT 
    c.Nome,
    COUNT(p.PedidoID) as QuantidadePedidos,
    SUM(p.ValorTotal) as ValorTotalPedidos
FROM
    clientes c
JOIN pedidos p 
    ON c.ClienteID = p.ClienteID
GROUP BY c.Nome
"""

query_3 = """
SELECT 
    p.PedidoID,
    p.DataPedido,
    p.ValorTotal
FROM
    pedidos p
LEFT JOIN pagamentos pg 
    ON p.PedidoID = pg.PedidoID
WHERE pg.PagamentoID IS NULL;
"""

question_1 = "Escreva uma consulta SQL que mostre a lista de todos os clientes e seus respectivos pedidos, mesmo que o cliente não tenha feito nenhum pedido. A tabela resultante deve conter as colunas: Nome, PedidoID, DataPedido e ValorTotal." 
question_2 = "Escreva uma consulta SQL que exiba o total de pedidos realizados e o valor total de pedidos por cliente, apenas para os clientes que possuem pedidos registrados. A tabela resultante deve conter as colunas: Nome, QuantidadePedidos e ValorTotalPedidos."
question_3 = "Escreva uma consulta SQL que exiba os pedidos que não possuem pagamentos registrados. A tabela resultante deve conter as colunas: PedidoID, DataPedido e ValorTotal."


def print_question(question: str, query: str, conn: sqlite3.Connection) -> None:
    print(f"Question: {question}\n")
    df_query = pd.read_sql_query(query, conn).fillna("")
    print(df_query)
    print("\n")

if __name__ == "__main__":

    try:
        conn = sqlite3.connect("Loja.sqlite")
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
    print("Connected to database successfully.\n")

    print_question(question_1, query_1, conn)
    print_question(question_2, query_2, conn)
    print_question(question_3, query_3, conn)
    conn.close()