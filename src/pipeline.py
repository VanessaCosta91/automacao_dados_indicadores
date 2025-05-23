import os
from google.cloud import bigquery

def extrair_dados(): # função para extrair dados
    # autorização
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "chave_bigquery.json"

    # Cria o cliente BigQuery
    client = bigquery.Client()

    # consultas sql dos indicadores (KPI)

    query_vendas = '''
    # Total de vendas por mês
    SELECT 
          FORMAT_DATE('%Y-%m', DATE(created_at)) AS Mes,
          SUM(sale_price) AS Vendas
    FROM bigquery-public-data.thelook_ecommerce.order_items
    WHERE status IN ('Complete','Shipped')
    GROUP BY Mes
    ORDER BY Mes;
    '''

    query_ticket = '''
    # ticket médio por mês
    SELECT 
          pro.category AS Categoria,
          FORMAT_DATE('%Y-%m', DATE(oi.created_at)) AS Mes,
          ROUND(AVG(oi.sale_price),2) AS Media_venda
    FROM bigquery-public-data.thelook_ecommerce.order_items AS oi
    JOIN bigquery-public-data.thelook_ecommerce.products AS pro
    ON pro.id = oi.product_id
    WHERE oi.status IN ('Complete', 'Shipped')
    GROUP BY pro.category, Mes
    ORDER BY Mes;
    '''

    query_pedidos = '''
    # Total de pedidos por mês (volume total de transações)
    SELECT
          FORMAT_DATE('%Y-%m', DATE(created_at)) AS Mes,
          count(*) AS Total_pedidos
    FROM bigquery-public-data.thelook_ecommerce.order_items
    GROUP BY Mes
    ORDER BY Mes;
    '''

    query_entrega = '''
    # tempo médio de entregas
    SELECT      
          FORMAT_DATE('%Y-%m', DATE(created_at)) AS Mes,
          ROUND(AVG(TIMESTAMP_DIFF(shipped_at, created_at, HOUR))/ 24,2) AS Tempo_medio_dias
    FROM bigquery-public-data.thelook_ecommerce.order_items
    WHERE 
          status IN ('Complete', 'Shipped') 
          AND shipped_at IS NOT NULL
    GROUP BY Mes
    ORDER BY Mes;
    '''

    query_cancelados = '''
    # porcentagem de pedidos cancelados
    SELECT 
        ROUND(COUNTIF(status = 'Cancelled') / COUNT(*),2) AS Pct_cancelados,
        FORMAT_DATE('%Y-%m', DATE(created_at)) AS Mes
    FROM bigquery-public-data.thelook_ecommerce.order_items
    GROUP BY Mes
    ORDER BY Mes;   
    '''

    query_devolvidos = '''
    # porcentagem de pedidos devolvidos
    SELECT 
        ROUND(COUNTIF(status = "Returned") / COUNT(*),2) AS Pct_devolvidos,
        FORMAT_DATE('%Y-%m', DATE(created_at)) AS Mes
    FROM bigquery-public-data.thelook_ecommerce.order_items
    GROUP BY Mes
    ORDER BY Mes;
    '''

    # Executa e salva as consultas como DataFrames
    df_vendas = client.query(query_vendas).to_dataframe()
    df_pedidos = client.query(query_pedidos).to_dataframe()
    df_ticket = client.query(query_ticket).to_dataframe()
    df_entrega = client.query(query_entrega).to_dataframe()
    df_cancelados = client.query(query_cancelados).to_dataframe()
    df_devolvidos = client.query(query_devolvidos).to_dataframe()
    return df_vendas, df_pedidos, df_ticket, df_entrega, df_cancelados, df_devolvidos

def transformar_dados(df_vendas, df_pedidos, df_ticket, df_entrega):   # função criar colunas
    # variação percentual das Vendas
    df_vendas['crescimento_pct'] = df_vendas['Vendas'].pct_change() * 100
    df_vendas['crescimento_pct'] = df_vendas['crescimento_pct'].round(2)

    # media movel de 3 meses de venda
    df_vendas['Media_movies_3m'] = df_vendas['Vendas'].rolling(window=3).mean().round(2)

    # variação percentual da quantidade de pedidos
    df_pedidos['crescimento_pct'] = df_pedidos['Total_pedidos'].pct_change() * 100
    df_pedidos['Total_pedidos'] = df_pedidos['Total_pedidos'].round(2)

    # media móvel de 3 meses da quantidade de pedidos
    df_pedidos['Media_movies_3m'] = df_pedidos['Total_pedidos'].rolling(window=3).mean().round(2)

    # variação percentual tempo de entrega
    df_entrega['crescimento_pct'] = df_entrega['Tempo_medio_dias'].pct_change() * 100
    df_entrega['Tempo_medio_dias'] = df_entrega['Tempo_medio_dias'].round(2)

    # media móvel de 3 meses do tempo de entrega
    df_entrega['Media_movies_3m'] = df_entrega['Tempo_medio_dias'].rolling(window=3).mean().round(2)

    # Ticket médio – classificar categorias por volume
    df_ticket_total = df_ticket.groupby("Categoria")["Media_venda"].sum().reset_index()
    df_ticket_total = df_ticket_total.sort_values(by="Media_venda", ascending=False)
    df_ticket_total.columns = ['Categoria', 'Total_Media_Venda']
    return df_ticket_total


def salvar_arquivos(df_vendas, df_pedidos, df_ticket, df_entrega, df_cancelados, df_devolvidos, df_ticket_total):
    dataframes = {
        "vendas_mensais.csv": df_vendas,
        "qtde_pedidos.csv": df_pedidos,
        "ticket_medio.csv": df_ticket,
        "tempo_medio_entrega.csv": df_entrega,
        "pct_cancelamentos.csv": df_cancelados,
        "pct_devolvidos.csv": df_devolvidos,
        'ranking_categorias.csv': df_ticket_total
    }

    # salvar arquivos csv
    for arquivos, df in dataframes.items():
        for col in df.select_dtypes(include=['float']):
            df[col] = df[col].astype(str).str.replace('.', ',', regex=False)
        df.to_csv(arquivos, index=False, sep=';', encoding='utf-8-sig')
    return (df_vendas, df_pedidos, df_ticket, df_entrega, df_cancelados, df_devolvidos, df_ticket_total)


if __name__ == "__main__":
    df_vendas, df_pedidos, df_ticket, df_entrega, df_cancelados, df_devolvidos = extrair_dados()
    df_ticket_total = transformar_dados(df_vendas, df_pedidos, df_ticket, df_entrega)
    salvar_arquivos(df_vendas, df_pedidos, df_ticket, df_entrega, df_cancelados, df_devolvidos, df_ticket_total)