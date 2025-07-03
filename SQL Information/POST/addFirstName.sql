--Create a first name
DELIMITER //
DROP PROCEDURE IF EXISTS addFirstName //

CREATE PROCEDURE addFirstName(IN firstName VARCHAR(100), IN genderIn VARCHAR(50), IN backgroundIn VARCHAR(50))
BEGIN
	INSERT INTO first_name (FIRST_NAME, GENDER, BACKGROUND) VALUES (firstName, genderIn, backgroundIn);
END //
DELIMITER ;