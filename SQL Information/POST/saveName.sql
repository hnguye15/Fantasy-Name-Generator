--Save a full name to the user's list
DELIMITER //
DROP PROCEDURE IF EXISTS saveName //

CREATE PROCEDURE saveName(IN userID VARCHAR(50), IN nameIn VARCHAR(255), IN genderIn VARCHAR(50), IN backgroundIn VARCHAR(50))
BEGIN
	INSERT INTO saved_name (USER_ID, NAME, GENDER, BACKGROUND) VALUES (userId, nameIn, genderIn, backgroundIn);
END //
DELIMITER ;
