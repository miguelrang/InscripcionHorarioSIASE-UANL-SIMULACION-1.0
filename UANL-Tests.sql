USE [UANL]


DROP PROCEDURE example
GO

CREATE PROCEDURE example(@career VARCHAR(MAX), @subject VARCHAR(MAX)) AS
	DECLARE @id_career INT
	SET @id_career=(SELECT ID_career FROM Career WHERE name_career=@career)
	
	DECLARE @op1 VARCHAR(MAX)
	SET @op1 = (SELECT op1 FROM Kardex 
				WHERE ID_subject=(
						SELECT ID_subject FROM SemesterSubject
						WHERE name_subject=@subject AND ID_career=@id_career
					  )
						AND
						ID_student=100
				)
	DECLARE @op3 VARCHAR(MAX)
	SET @op3 = (SELECT op3 FROM Kardex 
				WHERE ID_subject=(
						SELECT ID_subject FROM SemesterSubject
						WHERE name_subject=@subject AND ID_career=@id_career
					  )
						AND
						ID_student=100
				)
	DECLARE @op5 VARCHAR(MAX)
	SET @op5 = (SELECT op5 FROM Kardex 
				WHERE ID_subject=(
						SELECT ID_subject FROM SemesterSubject
						WHERE name_subject=@subject AND ID_career=@id_career
					  )
					AND
						ID_student=100
				)
	
	SELECT  t.middle_name,
			t.last_name,
			t.name_, 
			s.ID_group,
			CASE
				WHEN @op1 = '' THEN 'op1'
					
				WHEN @op3 = '' THEN 'op3'

				WHEN @op5 = '' THEN 'op5'
			END AS op,
				s.schedule FROM Schedule s
					INNER JOIN(
						SELECT ID_career, ID_teacher, middle_name, last_name, name_ FROM Teacher
					)t
					ON t.ID_teacher=s.ID_teacher and t.ID_career=@id_career

					INNER JOIN(
						SELECT ID_classroom, banches FROM Classroom
					)c
					ON c.banches > 0 AND c.ID_classroom=s.ID_classroom
	WHERE s.ID_career=@id_career
			AND
		  s.ID_subject=(SELECT ID_subject FROM SemesterSubject WHERE ID_career=@id_career and name_subject=@subject)
GO

EXECUTE example 'LICENCIADO EN SEGURIDAD EN TECNOLOGIAS DE INFORMACION', 'ÁLGEBRA'
go