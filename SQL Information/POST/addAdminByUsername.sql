--Create a user that has admin privileges
DELIMITER //
DROP PROCEDURE IF EXISTS addAdminByUsername //

CREATE PROCEDURE addAdminByUsername(IN username VARCHAR(50))
BEGIN
	UPDATE user
	SET IS_ADMIN = TRUE
	WHERE USER_NAME = username;
END //
DELIMITER ;
