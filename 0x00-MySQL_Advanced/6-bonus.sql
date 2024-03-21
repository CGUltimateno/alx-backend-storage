--a SQL script that creates a stored procedure
-- AddBonus that adds a new correction for a student.
-- The procedure must receive 2 arguments:
-- student_id INT and bonus INT.

DELIMITER $$

CREATE PROCEDURE AddBonus
(user_id INT, project_name VARCHAR(255), score INT)
BEGIN
	DECLARE p_id INT DEFAULT -1;
	SELECT id into p_id
	FROM projects
	WHERE name = project_name;
	IF p_id = -1 THEN
		INSERT INTO projects(name)
		VALUES(project_name);
		SELECT id INTO p_id
		FROM projects
		WHERE name = project_name;
	END IF;

	INSERT INTO corrections(user_id, project_id, score)
	VALUES(user_id, p_id, score);
END;
$$

DELIMITER ;