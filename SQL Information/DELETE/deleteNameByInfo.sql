--Delete a full name by their ID from the saved_name table
DELIMITER //
DROP PROCEDURE IF EXISTS deleteNameByInfo //

CREATE PROCEDURE deleteNameByInfo(IN userIn VARCHAR(50), IN name VARCHAR(100), IN genderIn VARCHAR(50), IN backgroundIn VARCHAR(50))
BEGIN
	DELETE FROM saved_name WHERE (USER_ID = userIn AND NAME = name AND GENDER = genderIn AND BACKGROUND = backgroundIn);
END //
DELIMITER ;
