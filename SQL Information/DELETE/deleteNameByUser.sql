--Delete a full name by their ID from the saved_name table
DELIMITER //
DROP PROCEDURE IF EXISTS deleteNameByUser //

CREATE PROCEDURE deleteNameByUser(IN userIn VARCHAR(50), IN nameIn VARCHAR(100), IN confirmDeleteAll VARCHAR(10))
BEGIN
	IF confirmDeleteAll = "no" THEN
		DELETE FROM saved_name WHERE (USER_ID = userIn AND NAME = nameIn);
	ELSE
		DELETE FROM saved_name WHERE USER_ID = userIn;
	END IF;
END //
DELIMITER ;
