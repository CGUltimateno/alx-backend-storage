-- Define a stored procedure to compute and store
-- the average score

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