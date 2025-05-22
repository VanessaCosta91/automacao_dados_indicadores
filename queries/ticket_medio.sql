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
