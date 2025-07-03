--Delete all feedback of a user
DELIMITER //
DROP PROCEDURE IF EXISTS deleteFeedbackByUser //

CREATE PROCEDURE deleteFeedbackByUser(IN username VARCHAR(50))
BEGIN
	DELETE FROM feedback
	WHERE USER_ID = username;
END //
DELIMITER ;