-- Define a stored procedure to compute and store
-- the weighted average score obtained by a student.

DELIMITER $$

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
	DECLARE u_id INT;
	DECLARE s_avg FLOAT;
	DECLARE flag INT DEFAULT 0;
	DECLARE user_ids CURSOR FOR SELECT id FROM users;
	DECLARE CONTINUE HANDLER FOR NOT FOUND SET flag = 1;

	OPEN user_ids;

	iteration: LOOP
		FETCH user_ids INTO u_id;
		IF flag = 1 THEN
			LEAVE iteration;
		END IF;

		SELECT SUM(score * weight) / sum(weight) INTO s_avg
	        FROM corrections INNER JOIN projects
        	ON id = project_id
	        WHERE user_id = u_id;

        	UPDATE users
	        SET average_score = s_avg
        	WHERE id = u_id;
	END LOOP;

	CLOSE user_ids;
END;
$$

DELIMITER ;