--Delete a last name using its ID
DELIMITER //
DROP PROCEDURE IF EXISTS removeLastNameByInfo //

CREATE PROCEDURE removeLastNameByInfo(IN lastName VARCHAR(100), IN genderIn VARCHAR(50), IN backgroundIn VARCHAR(50))
BEGIN
	DELETE FROM last_name WHERE (LAST_NAME = lastname AND GENDER = genderIn AND BACKGROUND = backgroundIn);
END //
DELIMITER ;
