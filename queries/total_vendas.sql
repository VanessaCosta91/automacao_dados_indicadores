# Total de vendas por mês
SELECT 
      FORMAT_DATE('%Y-%m', DATE(created_at)) AS Mes,
      SUM(sale_price) AS Vendas
FROM bigquery-public-data.thelook_ecommerce.order_items
WHERE status IN ('Complete','Shipped')
GROUP BY Mes
ORDER BY Mes;