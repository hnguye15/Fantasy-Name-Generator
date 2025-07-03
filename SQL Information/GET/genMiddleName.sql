--Generate a random middle name based on the input criteria
DELIMITER //
DROP PROCEDURE IF EXISTS genMiddleName //

CREATE PROCEDURE genMiddleName(IN genderIn VARCHAR(50), IN backgroundIn VARCHAR(50), IN counter INT)
BEGIN
	IF counter IS NULL THEN
		SELECT *
		FROM middle_name
		WHERE GENDER = genderIn AND BACKGROUND = backgroundIn
		ORDER BY RAND()
		LIMIT 1;
	ELSE
		SELECT *
		FROM middle_name
		WHERE GENDER = genderIn AND BACKGROUND = backgroundIn
		ORDER BY RAND()
		LIMIT counter;
	END IF;
END //
DELIMITER ;