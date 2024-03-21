-- Write a SQL script that lists all bands with
-- Glam rock as their main style,
-- ranked by their longevity
SELECT name,
       COALESCE(split, 2022) - formed AS longevity
FROM metal_bands
WHERE BINARY style LIKE '%Glam rock%'
ORDER BY longevity DESC;