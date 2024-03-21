--a SQL script that creates a stored procedure
-- ComputeAverageScoreForUser that computes
-- and store the average score for a student.
DELIMITER $$
CREATE PROCEDURE ComputeAverageScoreForUser (user_id INT)
BEGIN
    DECLARE avg_score FLOAT;
    SELECT AVG(score) INTO avg_score
    FROM corrections
    WHERE user_id = user_id;
	UPDATE users
	SET average_score = s_avg
	WHERE id = u_id;
END;