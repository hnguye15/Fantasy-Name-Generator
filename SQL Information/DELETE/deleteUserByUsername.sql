--Delete a user by their username
DELIMITER //
DROP PROCEDURE IF EXISTS deleteUserByUsername //

CREATE PROCEDURE deleteUserByUsername(IN username VARCHAR(50))
BEGIN
	DELETE FROM user
	WHERE USER_NAME = username;
END //
DELIMITER ;