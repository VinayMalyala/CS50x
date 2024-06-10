SELECT language, COUNT(*) AS n
FROM favorites
GROUP BY language
ORDER BY n DESC
LIMIT 1;
