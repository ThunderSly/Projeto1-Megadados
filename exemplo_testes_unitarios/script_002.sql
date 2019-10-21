USE socialNetwork;
DROP TABLE IF EXISTS Likes;
CREATE TABLE Likes (
	idUser INT NOT NULL,
	idPost INT NOT NULL,
	likeType TINYINT(1) NOT NULL DEFAULT 1,
	activeLike TINYINT(1) NOT NULL DEFAULT 1,
	PRIMARY KEY (idUser, idPost),
	FOREIGN KEY (idUser)
	REFERENCES Users (idUser) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (idPost)
	REFERENCES Posts (idPost) ON DELETE CASCADE ON UPDATE CASCADE
);

DROP TRIGGER IF EXISTS duplicateLikeTrigger;
DELIMITER //
CREATE TRIGGER duplicateLikeTrigger
BEFORE INSERT ON Likes 
FOR EACH ROW
BEGIN
	SELECT COUNT(*) INTO @rowcount FROM Likes WHERE idUser=NEW.idUser AND idPost=NEW.idPost;
	IF @rowcount > 0 THEN
		SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'Duplicate Like';
	END IF;
END //
DELIMITER ;

DROP TRIGGER IF EXISTS inactiveUserTrigger;
DELIMITER //
CREATE TRIGGER inactiveUserTrigger
AFTER UPDATE ON Users
FOR EACH ROW
BEGIN
	IF NEW.activeUser = 0 THEN
		UPDATE Posts SET activePost = 0
		WHERE NEW.idUser = Posts.idUser;
		UPDATE Mentions SET activeMention = 0
		WHERE NEW.idUser = Mentions.idUser;
		UPDATE Preferences SET activePreference = 0
		WHERE NEW.idUser = Preferences.idUser;
		UPDATE Likes SET activeLike = 0
		WHERE NEW.idUser = Likes.idUser;
	END IF;
END; //
DELIMITER ;

DROP TRIGGER IF EXISTS inactivePostTrigger;
DELIMITER //
CREATE TRIGGER inactivePostTrigger
AFTER UPDATE ON Posts
FOR EACH ROW
BEGIN
	IF NEW.activePost = 0 THEN
		UPDATE Mentions SET activeMention = 0
		WHERE NEW.idPost = Mentions.idPost;
		UPDATE Tags SET activeTag= 0
		WHERE NEW.idPost = Tags.idPost;
		UPDATE Likes SET activeLike= 0
		WHERE NEW.idPost = Likes.idPost;
	END IF;
END; //
DELIMITER ;

