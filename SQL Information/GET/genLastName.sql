--Generate a random last name based on the input criteria
DELIMITER //
DROP PROCEDURE IF EXISTS genLastName //

CREATE PROCEDURE genLastName(IN genderIn VARCHAR(50), IN backgroundIn VARCHAR(50), IN counter INT)
BEGIN
	IF counter IS NULL THEN
		SELECT *
		FROM last_name
		WHERE GENDER = genderIn AND BACKGROUND = backgroundIn
		ORDER BY RAND()
		LIMIT 1;
	ELSE
		SELECT *
		FROM last_name
		WHERE GENDER = genderIn AND BACKGROUND = backgroundIn
		ORDER BY RAND()
		LIMIT counter;
	END IF;
END //
DELIMITER ;