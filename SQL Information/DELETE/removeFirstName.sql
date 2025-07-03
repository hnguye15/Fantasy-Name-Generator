--Delete a first name using its ID
DELIMITER //
DROP PROCEDURE IF EXISTS removeFirstName //

CREATE PROCEDURE removeFirstName(IN firstCode INT)
BEGIN
	DELETE FROM first_name WHERE FIRST_CODE = firstCode;
END //
DELIMITER ;