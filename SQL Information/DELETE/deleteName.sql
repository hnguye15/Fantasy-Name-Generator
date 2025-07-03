--Delete a full name by their ID from the saved_name table
DELIMITER //
DROP PROCEDURE IF EXISTS deleteName //

CREATE PROCEDURE deleteName(IN ID INT)
BEGIN
	DELETE FROM saved_name
	WHERE NAME_CODE = ID;
END //
DELIMITER ;