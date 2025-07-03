--Save a feedback to the feedback table
DELIMITER //
DROP PROCEDURE IF EXISTS saveFeedback //

CREATE PROCEDURE saveFeedback(IN userID VARCHAR(50), IN feedbackIn VARCHAR(255))
BEGIN
	INSERT INTO feedback (USER_ID, FEEDBACK) VALUES (userId, feedbackIn);
END //
DELIMITER ;
