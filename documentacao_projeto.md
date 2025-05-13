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
* **Fórmula**: `(COUNTIF(status = 'Cancelled') / COUNT(*)) * 100`
* **Fonte dos dados**:
  * Tabela: `order_items`
  * Coluna: `status`

---

### **Percentual de pedidos devolvidos**

* **Descrição**: porcentagem de pedidos devolvidos. Pode indicar insatisfação com produto ou serviço.
* **Fórmula**: `(COUNTIF(status = 'Returned') / COUNT(*)) * 100`
* **Fonte dos dados**:
  * Tabela: `order_items`
  * Coluna: `status`

---

### Observação:

Todos os indicadores acima foram extraídos da base pública **bigquery-public-data.thelook_ecommerce**, disponível no Google BigQuery. O campo `status` foi usado para filtrar apenas pedidos finalizados ou enviados, quando necessário.
