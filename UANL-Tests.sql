USE [UANL]


SELECT * FROM Classroom
SELECT * FROM Schedule
SELECT * FROM StudentSchedule
GO

/*
INSERT INTO Classroom(ID_faculty, classroom, banches) VALUES(8, 101, 45);
INSERT INTO Classroom(ID_faculty, classroom, banches) VALUES(8, 102, 34);
INSERT INTO Classroom(ID_faculty, classroom, banches) VALUES(8, 103, 55);
INSERT INTO Classroom(ID_faculty, classroom, banches) VALUES(8, 104, 20);
*/
CREATE PROCEDURE example AS
	DECLARE @id_career INT
		SET @id_career=(
				SELECT ID_career FROM Schedule
				WHERE ID_faculty=(
						SELECT ID_faculty FROM Faculty
						WHERE name_faculty='CIENCIAS FISICO-MATEMATICAS'
					  ) 
						AND
					  ID_classroom=(
						SELECT ID_classroom FROM Classroom
						WHERE classroom='101'
					  )
						AND
					  schedule='07:00-07:30;07:30-08:00;08:00-08:30;'
			)
		
		SELECT c.name_career, t.middle_name, t.last_name, t.name_ FROM Schedule s
			INNER JOIN(
				SELECT ID_career, name_career FROM Career
			)c
			ON c.ID_career=@id_career

			INNER JOIN(
				SELECT ID_teacher, middle_name, last_name, name_ FROM Teacher
			)t
			ON t.ID_teacher=s.ID_teacher
GO

EXECUTE example

DROP PROCEDURE example



