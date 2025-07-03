--Get most recently saved names (including recently modified names)
DELIMITER //
DROP PROCEDURE IF EXISTS getNames //

CREATE PROCEDURE getNames(IN username VARCHAR(50), IN counter INT)
BEGIN
	IF counter > 0
	THEN
		SELECT *
		FROM saved_name
		WHERE USER_ID = username
		ORDER BY LAST_MODIFIED
		DESC
		LIMIT counter;
	ELSE
		SELECT *
		FROM saved_name
		WHERE USER_ID = username
		ORDER BY LAST_MODIFIED
		DESC
	END IF;
	
END //
DELIMITER ;
