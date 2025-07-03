--Create a middle name
DELIMITER //
DROP PROCEDURE IF EXISTS addMiddleName //

CREATE PROCEDURE addMiddleName(IN middleName VARCHAR(100), IN genderIn VARCHAR(50), IN backgroundIn VARCHAR(50))
BEGIN
	INSERT INTO middle_name (MIDDLE_NAME, GENDER, BACKGROUND) VALUES (middleName, genderIn, backgroundIn);
END //
DELIMITER ;