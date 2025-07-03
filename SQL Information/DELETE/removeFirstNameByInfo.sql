--Delete a first name using its ID
DELIMITER //
DROP PROCEDURE IF EXISTS removeFirstNameByInfo //

CREATE PROCEDURE removeFirstNameByInfo(IN firstName VARCHAR(100), IN genderIn VARCHAR(50), IN backgroundIn VARCHAR(50))
BEGIN
	DELETE FROM first_name WHERE (FIRST_NAME = firstname AND GENDER = genderIn AND BACKGROUND = backgroundIn);
END //
DELIMITER ;
