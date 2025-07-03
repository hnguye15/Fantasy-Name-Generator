--Revoke admin status of a user by their username
DELIMITER //
DROP PROCEDURE IF EXISTS deleteAdminByUsername //

CREATE PROCEDURE deleteAdminByUsername(IN username VARCHAR(50))
BEGIN
	UPDATE user
	SET IS_ADMIN = FALSE
	WHERE USER_NAME = username;
END //
DELIMITER ;