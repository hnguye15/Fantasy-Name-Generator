--Get a user by inputting the user's username and password
DELIMITER //
DROP PROCEDURE IF EXISTS changePasswordByUsernameAndPassword //

CREATE PROCEDURE changePasswordByUsernameAndPassword(IN username VARCHAR(50), IN old_password VARCHAR(255), IN new_password VARCHAR(255))
BEGIN
	UPDATE user
	SET user.PASSWORD = Password(new_password)
	WHERE user.USER_NAME = username
	AND user.PASSWORD = Password(old_password);
END //
DELIMITER ;