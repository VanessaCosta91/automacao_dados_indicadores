# porcentagem de pedidos devolvidos
SELECT ROUND(COUNTIF(status = "Returned")*100 / COUNT(*),2) AS Pct_devolvidos
FROM bigquery-public-data.thelook_ecommerce.order_items;