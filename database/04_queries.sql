-- Tickets abiertos por prioridad
SELECT prioridad, COUNT(*) AS total
FROM tickets
WHERE estado NOT IN ('CERRADO', 'RESUELTO')
GROUP BY prioridad
ORDER BY prioridad;

-- Inventario que requiere reposición
SELECT sku, nombre, stock, stock_minimo
FROM inventario
WHERE activo = 'S' AND stock <= stock_minimo
ORDER BY stock ASC;

-- Resumen de operación para el dashboard
SELECT
    (SELECT COUNT(*) FROM tickets WHERE estado NOT IN ('CERRADO', 'RESUELTO')) AS tickets_abiertos,
    (SELECT COUNT(*) FROM tickets WHERE prioridad = 'P1' AND estado NOT IN ('CERRADO', 'RESUELTO')) AS tickets_criticos,
    (SELECT COUNT(*) FROM ordenes_trabajo WHERE estado NOT IN ('COMPLETADA', 'CANCELADA')) AS ordenes_activas,
    (SELECT COUNT(*) FROM inventario WHERE activo = 'S' AND stock <= stock_minimo) AS stock_critico
FROM dual;
