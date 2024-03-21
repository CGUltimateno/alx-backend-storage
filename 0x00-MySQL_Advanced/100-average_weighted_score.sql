-- Define a stored procedure to compute and store
-- the weighted average score obtained by a student.

DELIMITER $$

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(u_id INT)
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