USE [UANL]

DROP TRIGGER deleteAllFromStudent
DROP TRIGGER deleteAllFromTeacher
DROP TRIGGER deleteAllFromClassroom
DROP TRIGGER deleteAllFromSchedule
GO


CREATE TRIGGER deleteAllFromStudent
	ON Student
	AFTER DELETE AS
		DECLARE @id INT
		SET @id = (SELECT ID_student FROM deleted)

		DELETE FROM Kardex
		WHERE ID_student = @id

		DELETE FROM StudentSchedule
		WHERE ID_student = @id
GO

CREATE TRIGGER deleteALLFromTeacher
	ON Teacher
	AFTER DELETE AS
		DECLARE @id INT
		SET @id = (SELECT ID_teacher FROM deleted)

		DELETE FROM Schedule
		WHERE ID_schedule = @id

		DELETE FROM StudentSchedule
		WHERE ID_teacher = @id
GO

CREATE TRIGGER deleteAllFromClassroom
	ON StudentSchedule
	AFTER DELETE AS
		DECLARE @id INT
		SET @id = (SELECT ID_classroom FROM deleted)

		DELETE FROM Schedule
		WHERE ID_classroom = @id

		DELETE FROM Classroom
		WHERE ID_classroom = @id
GO

CREATE TRIGGER deleteAllFromSchedule
	ON StudentSchedule
		AFTER DELETE AS
			DECLARE @id INT
			SET @id = (SELECT d.ID_schedule FROM deleted d)

			DELETE FROM Schedule
			WHERE ID_schedule = @id
GO













