--Get most recently saved feedback
DELIMITER //
DROP PROCEDURE IF EXISTS getFeedback//

CREATE PROCEDURE getFeedback()
BEGIN
	SELECT * FROM feedback;
END //
DELIMITER ;
