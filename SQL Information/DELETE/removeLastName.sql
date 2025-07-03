--Delete a last name using its ID
DELIMITER //
DROP PROCEDURE IF EXISTS removeLastName //

CREATE PROCEDURE removeLastName(IN lastCode INT)
BEGIN
	DELETE FROM last_name WHERE LAST_CODE = lastCode;
END //
DELIMITER ;