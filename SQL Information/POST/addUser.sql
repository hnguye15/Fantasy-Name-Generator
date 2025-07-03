--Add a user by inputting a username
DELIMITER //
DROP PROCEDURE IF EXISTS addUser //

CREATE PROCEDURE addUser(IN username VARCHAR(50), IN password VARCHAR(50), IN email VARCHAR(150))
BEGIN
	INSERT INTO user (user.USER_NAME, user.PASSWORD, user.EMAIL) VALUES (username, Password(password), email);
END //
DELIMITER ;
