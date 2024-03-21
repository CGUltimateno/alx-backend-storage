-- Write a SQL script that lists all bands with
-- Glam rock as their main style,
-- ranked by their longevity
SELECT band_name,
       COALESCE(split, 2022) - formed lifespan
FROM metal_bands
WHERE BINARY style LIKE '%Glam rock%'
ORDER BY lifespan DESC;