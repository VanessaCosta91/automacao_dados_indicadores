# porcentagem de pedidos cancelados
SELECT 
    ROUND(COUNTIF(status = 'Cancelled')*100 / COUNT(*),2) AS Pct_cancelados,
    FORMAT_DATE('%Y-%m', DATE(created_at)) AS Mes
FROM bigquery-public-data.thelook_ecommerce.order_items
GROUP BY Mes
ORDER BY Mes;
