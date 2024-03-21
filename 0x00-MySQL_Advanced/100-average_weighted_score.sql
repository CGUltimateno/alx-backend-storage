-- Define a stored procedure to compute and store
-- the average weighted score for each student.

DELIMITER $$

CREATE PROCEDURE average_weighted_score(user_id INT)
BEGIN
	DECLARE s_avg FLOAT;

	SELECT SUM(score * weight) / sum(weight) INTO s_avg
	FROM corrections INNER JOIN projects
	ON id = project_id
	WHERE user_id = u_id;

	UPDATE users
	SET average_score = s_avg
	WHERE id = u_id;
END;
$$

DELIMITER ;