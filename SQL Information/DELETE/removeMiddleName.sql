--Delete a middle name using its ID
DELIMITER //
DROP PROCEDURE IF EXISTS removeMiddleName //

CREATE PROCEDURE removeMiddleName(IN middleCode INT)
BEGIN
	DELETE FROM middle_name WHERE MIDDLE_CODE = middleCode;
END //
DELIMITER ;