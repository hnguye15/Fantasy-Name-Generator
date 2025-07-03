--Get an admin by inputting the admin's username
DELIMITER //
DROP PROCEDURE IF EXISTS getAdminByUsername //

CREATE PROCEDURE getAdminByUsername(IN username VARCHAR(50))
BEGIN
	SELECT *
	FROM user
	WHERE USER_NAME = username
	AND IS_ADMIN IS TRUE;
END //
DELIMITER ;