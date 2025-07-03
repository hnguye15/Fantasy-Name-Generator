--Get a user by inputting the user's username and password
DELIMITER //
DROP PROCEDURE IF EXISTS getUserByUsernameAndPassword //

CREATE PROCEDURE getUserByUsernameAndPassword(IN username VARCHAR(50), IN password VARCHAR(255))
BEGIN
	SELECT *
	FROM user
	WHERE user.USER_NAME = username
	AND user.PASSWORD = Password(password);
END //
DELIMITER ;