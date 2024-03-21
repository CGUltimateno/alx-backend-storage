--a SQL script that creates a stored procedure
-- ComputeAverageScoreForUser that computes
-- and store the average score for a student.

DELIMITER $$

CREATE PROCEDURE ComputeAverageScoreForUser(u_id INT)
BEGIN
	DECLARE s_avg FLOAT;

	SELECT AVG(score) INTO s_avg
	FROM corrections
	WHERE user_id = u_id;

	UPDATE users
	SET average_score = s_avg
	WHERE id = u_id;
END;
$$

DELIMITER ;