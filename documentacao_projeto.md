# Automação de Indicadores de E-commerce com BigQuery + Python


## 1. KPIs e Justificativas

### **Vendas por mês**

* **Descrição**: valor total de vendas realizadas mensalmente. Permite acompanha a evolução financeira da empresa ao longo do tempo.
* **Fórmula**: `SUM(sale_price)` agrupado por mês (`FORMAT_DATE('%Y-%m', created_at)`)
* **Fonte dos dados**:
  * Tabela: `order_items`
  * Colunas: `created_at`, `sale_price`
  * Filtro: `status IN ('Complete', 'Shipped')`

---

### **Quantidade de pedidos por mês**

* **Descrição**: total de pedidos realizados em cada mês, ajuda a identificar padrões de demanda e sazonalidade.
* **Fórmula**: `COUNT(*)` agrupado por mês (`FORMAT_DATE('%Y-%m', created_at)`)
* **Fonte dos dados**:
  * Tabela: `order_items`
  * Colunas: `created_at`

---

### **Ticket médio por mês por categoria**

* **Descrição**: valor médio de venda por categoria de produto a cada mês. Importante para identificar quais categorias geram maior faturamento e direcionar estratégias comerciais.
* **Fórmula**: `AVG(sale_price)` agrupado por `category` e `Mes`
* **Fonte dos dados**:
  * Tabelas: `order_items` (alias `oi`), `products` (alias `pro`)
  * Colunas: `sale_price`, `created_at`, `category`, `product_id`
  * Junção: `pro.id = oi.product_id`
  * Filtro: `status IN ('Complete', 'Shipped')`

---

### **Tempo médio de entrega**

* **Descrição**: tempo médio entre o momento do pedido e o momento da entrega. Mede a eficiência da logística.
* **Fórmula**: `AVG(TIMESTAMP_DIFF(shipped_at, created_at, HOUR))/ 24` agrupado por mês (`FORMAT_DATE('%Y-%m', created_at)`)
* **Fonte dos dados**:
  * Tabela: `order_items`
  * Colunas: `created_at`, `delivered_at`
  * Filtro: `status IN ('Complete', 'Shipped')`

---

### **Percentual de pedidos cancelados**

* **Descrição**: porcentagem de pedidos cancelados em relação ao total. Pode indicar falhas operacionais ou problemas de produto.
* **Fórmula**: `ROUND(COUNTIF(status = 'Cancelled') / COUNT(*),2)` agrupado por mês (`FORMAT_DATE('%Y-%m', created_at)`)
* **Fonte dos dados**:
  * Tabela: `order_items`
  * Coluna: `status`

---

### **Percentual de pedidos devolvidos**

* **Descrição**: porcentagem de pedidos devolvidos. Pode indicar insatisfação com produto ou serviço.
* **Fórmula**: `ROUND(COUNTIF(status = "Returned") / COUNT(*),2)` agrupado por mês (`FORMAT_DATE('%Y-%m', created_at)`)
* **Fonte dos dados**:
  * Tabela: `order_items`
  * Coluna: `status`



### Observação:

Todos os indicadores acima foram extraídos da base pública **bigquery-public-data.thelook_ecommerce**, disponível no Google BigQuery. O campo `status` foi usado para filtrar apenas pedidos finalizados ou enviados, quando necessário.

---

## 2. Agregações e cálculos em Python

Após a extração dos dados via SQL no Google BigQuery, as consultas foram convertidas em DataFrames no Python para facilitar o tratamento e análise dos indicadores.

### Conversão de consultas SQL para DataFrame
Cada KPI foi consultado diretamente no BigQuery utilizando a biblioteca `google.cloud.bigquery`, com autenticação por chave de serviço (JSON). Os resultados das queries foram transformados em DataFrame para posterior manipulação.

```
df = client.query(query).to_dataframe()
```

### Cálculos Complementares
Foram adicionados dois cálculos estatísticos:

* **Crescimento percentual mês a mês** 
Mede a variação percentual entre o mês atual e o anterior

```
#Exemplo
df['crescimento_pct'] = df['Tempo_medio_dias'].pct_change() * 100
```

* **Média móvel de 3 meses**
Atenua o efeito de variações atípicas  e facilita a visualização de tendências no tempo.

```
#Exempo
df['media_movel_3m'] = df['Tempo_medio_dias'].rolling(window=3).mean().round(2)
```

### Exportação dos Resultados

Os dados tratados foram exportados em formato .csv com codificação UTF-8 e separador ;, a fim de garantir a visualização no PowerBI.

```
df.to_csv('arquivo.csv', index=False, sep=';', encoding='utf-8-sig')
```

---

## 3. Dashboard

Desenvolvido no Power BI, utilizando os arquivos `.csv` gerados. Visualiza: vendas, pedidos, ticket médio, cancelamentos e devoluções.

---

## 4. Automação da Pipeline

- Script Python (`run_pipeline.py`)
- Arquivo BAT (`executar_pipeline.bat`)
- Agendador de Tarefas (Windows)
- Geração de `pipeline.log`

---

## 5. Estrutura de Arquivos

| Arquivo | Descrição |
|---------|----------|
| `pipeline.py` | ETL |
| `run_pipeline.py` | Automação |
| `manage_pipeline.py` | Alternativa |
| `requirements.txt` | Dependências |
| `executar_pipeline.bat` | Execução no Windows |
| `chave_bigquery.json` | Autenticação |
| `pipeline.log` | Log |
| `dashboard/` | Arquivos gráficos |

---

## 6. Instalação e Execução

1. Clonar o repositório  
2. Criar e ativar o ambiente virtual  
3. Instalar dependências  
4. Configurar chave  
5. Executar pipeline

---

## 7. Logs e Monitoramento

Registro em `pipeline.log` com erros e sucessos.

---

## 8. Conclusão

Automação completa de indicadores de e-commerce, integrando SQL, Python e BI.

---


Desenvolvido por Vanessa Costa — Portfólio em Análise de Dados.







