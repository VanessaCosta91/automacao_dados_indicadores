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