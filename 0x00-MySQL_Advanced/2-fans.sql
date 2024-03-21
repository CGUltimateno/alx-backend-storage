-- Write a SQL script that ranks country origins of bands,
-- ordered by the number of (non-unique) fans
SELECT origin,
       sum(fans) as total_fans
FROM metal_bands
GROUP BY origin
ORDER BY total_fans DESC;