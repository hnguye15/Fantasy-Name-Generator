--Create a last name
DELIMITER //
DROP PROCEDURE IF EXISTS addLastName //

CREATE PROCEDURE addLastName(IN lastName VARCHAR(100),  IN genderIn VARCHAR(50), IN backgroundIn VARCHAR(50))
BEGIN
	INSERT INTO last_name (LAST_NAME, GENDER, BACKGROUND) VALUES (lastName, genderIn, backgroundIn);
END //
DELIMITER ;