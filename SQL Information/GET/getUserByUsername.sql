--Get a user by inputting the user's username
DELIMITER //
DROP PROCEDURE IF EXISTS getUserByUsername //

CREATE PROCEDURE getUserByUsername(IN username VARCHAR(50))
BEGIN
	SELECT *
	FROM user
	WHERE user.USER_NAME = username;
END //
DELIMITER ;