SELECT title FROM movies
JOIN ratings ON ratings.movie_id = movies.id
JOIN stars ON movies.id = stars.movie_id
JOIN people ON  people.id = stars.person_id
WHERE people.name LIKE "Chadwick Boseman"
ORDER BY rating DESC
LIMIT 5;
