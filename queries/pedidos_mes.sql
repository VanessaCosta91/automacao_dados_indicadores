# Total de pedidos por mês (volume total de transações)
SELECT
      FORMAT_DATE('%Y-%m', DATE(created_at)) AS Mes,
      count(*) AS Total_pedidos
FROM bigquery-public-data.thelook_ecommerce.order_items
GROUP BY Mes
ORDER BY Mes;