--Delete a middle name using its ID
DELIMITER //
DROP PROCEDURE IF EXISTS removeMiddleNameByInfo //

CREATE PROCEDURE removeMiddleNameByInfo(IN middleName VARCHAR(100), IN genderIn VARCHAR(50), IN backgroundIn VARCHAR(50))
BEGIN
	DELETE FROM middle_name WHERE (MIDDLE_NAME = middlename AND GENDER = genderIn AND BACKGROUND = backgroundIn);
END //
DELIMITER ;
