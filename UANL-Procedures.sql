USE [UANL]


----------- LOGIN --------------
DROP PROCEDURE verifyLoginStudent
DROP PROCEDURE verifyLoginRector
----------- SIASE ---------------
DROP PROCEDURE getInfo
DROP PROCEDURE getKardex
DROP PROCEDURE updateStudentStatus
DROP PROCEDURE getStudentStatus
DROP PROCEDURE getAvailableSchedules
DROP PROCEDURE getStudentSchedule
DROP PROCEDURE getSchedule
DROP PROCEDURE getClassroomFromSchedule
DROP PROCEDURE insertStudentSchedule
DROP PROCEDURE getInsertedSubjects
DROP PROCEDURE deleteStudentSchedule
DROP PROCEDURE updateClassroomPlus
DROP PROCEDURE updateClassroomMinus
------- R E C T O R I A ---------
------------ ADD ----------------
---------- Student --------------
DROP PROCEDURE getFaculties
DROP PROCEDURE getCareers
DROP PROCEDURE getSubjects
DROP PROCEDURE getIds
DROP PROCEDURE verifyExistingStudent
DROP PROCEDURE getStudent
DROP PROCEDURE verifyExistingEmail
DROP PROCEDURE saveStudent
DROP PROCEDURE saveKardex
---------------- Teacher -------------------
DROP PROCEDURE verifyExistingTeacherAsStudent
DROP PROCEDURE getTeacherIds
DROP PROCEDURE getTeacherEnrollment
DROP PROCEDURE verifyExistingTeacherEmail
DROP PROCEDURE verifyExistingTeacher
DROP PROCEDURE saveTeacher
------------- Classroom ----------------
DROP PROCEDURE getClassroomData
DROP PROCEDURE getIDFaculty
DROP PROCEDURE saveClassroom
DROP PROCEDURE getUnavailableSchedule
DROP PROCEDURE getTeachers
DROP PROCEDURE getIdTeacher
DROP PROCEDURE getAllClassrooms
DROP PROCEDURE saveSchedule
----------- U P D A T E --------------
------------- Student ----------------
DROP PROCEDURE updateStudent
DROP PROCEDURE deleteKardex
------------- Teacher ----------------
DROP PROCEDURE getTeacher
DROP PROCEDURE getIDFac_CarTeacher
DROP PROCEDURE updateTeacher
------------ Classroom ---------------
DROP PROCEDURE updateClassroom
------------- Schedule ---------------
DROP PROCEDURE updateSchedule
----------- D E L E T E --------------
------------- Student ----------------
DROP PROCEDURE getStudentInfo
DROP PROCEDURE deleteStudent
------------- Teacher ----------------
DROP PROCEDURE getTeacherCareers
DROP PROCEDURE getTeacherInfo
DROP PROCEDURE deleteTeacher
------------ Classroom ---------------
--DROP PROCEDURE getClassroomInfo
DROP PROCEDURE deleteClassroom
DROP PROCEDURE getClassroom
DROP PROCEDURE getClassrooms
DROP PROCEDURE getBanches
------------- Schedule ---------------
DROP PROCEDURE getSchedules
DROP PROCEDURE getC_T
DROP PROCEDURE getScheduleInfo
DROP PROCEDURE restartClassroom
DROP PROCEDURE deleteSchedule
GO

-------------------------------------- L O G I N ---------------------------------------------
CREATE PROCEDURE verifyLoginStudent(@enrollment INT, @password VARCHAR(16)) AS
	SELECT ISNULL(MAX(ID_student), '') FROM Student
	WHERE ID_student = @enrollment and password_ = @password
GO

CREATE PROCEDURE verifyLoginRector(@enrollment INT, @password VARCHAR(16)) AS
	SELECT ISNULL(MAX(ID_rector), '') FROM Rector 
	WHERE ID_rector = @enrollment and password_ = @password
GO

-------------------------------------- S I A S E ---------------------------------------------
CREATE PROCEDURE getInfo(@enrollment INT) AS
	SELECT s.ID_student, s.name_, s.middle_name, s.last_name, c.name_career FROM Student s
		INNER JOIN(
			SELECT c.ID_career, c.name_career FROM Career c
		)c
		ON s.ID_student = @enrollment and c.ID_career = s.ID_career
GO

CREATE PROCEDURE getKardex(@ID_student INT) AS
	SELECT s.ID_semester, s.name_subject, k.op1, k.op2, k.op3, k.op4, k.op5, k.op5, k.op6 FROM Kardex k
		INNER JOIN(
			SELECT ID_semester, ID_subject, name_subject FROM SemesterSubject
		)s
		ON s.ID_subject=k.ID_subject 
	WHERE k.ID_student=1000
GO

CREATE PROCEDURE updateStudentStatus(@enrollment INT, @status VARCHAR(MAX)) AS
	UPDATE Student
		SET student_status=@status
		WHERE ID_student=@enrollment
GO

CREATE PROCEDURE getStudentStatus(@enrollment INT) AS
	SELECT student_status FROM Student
	WHERE ID_student=@enrollment
GO

CREATE PROCEDURE getAvailableSchedules(@enrollment INT, @career VARCHAR(MAX), @subject VARCHAR(MAX)) AS
	DECLARE @id_career INT
	SET @id_career=(SELECT ID_career FROM Career WHERE name_career=@career)
	
	DECLARE @op1 VARCHAR(MAX)
	SET @op1 = (SELECT op1 FROM Kardex 
				WHERE ID_subject=(
						SELECT ID_subject FROM SemesterSubject
						WHERE name_subject=@subject AND ID_career=@id_career
					  )
						AND
					  ID_student=@enrollment
				)
	DECLARE @op3 VARCHAR(MAX)
	SET @op3 = (SELECT op3 FROM Kardex 
				WHERE ID_subject=(
						SELECT ID_subject FROM SemesterSubject
						WHERE name_subject=@subject AND ID_career=@id_career
					  )
						AND
					  ID_student=@enrollment
				)
	DECLARE @op5 VARCHAR(MAX)
	SET @op5 = (SELECT op5 FROM Kardex 
				WHERE ID_subject=(
						SELECT ID_subject FROM SemesterSubject
						WHERE name_subject=@subject AND ID_career=@id_career
					  )
						AND
					  ID_student=@enrollment
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

CREATE PROCEDURE getStudentSchedule(@ID_student INT) AS
	SELECT ss.name_subject, s2.ID_group, s2.schedule FROM StudentSchedule s
		INNER JOIN(
			SELECT ID_subject, name_subject FROM SemesterSubject
		)ss
		ON ss.ID_subject = s.ID_subject

		INNER JOIN(
			SELECT ID_schedule, ID_group, schedule FROM Schedule s
		)s2
		ON s2.ID_schedule = s.ID_schedule

	WHERE ID_student=@ID_student

GO

CREATE PROCEDURE getSchedule(@enrollment INT) AS
	SELECT ss2.name_subject, s.ID_group, s.schedule FROM StudentSchedule ss
		INNER JOIN(
			SELECT ID_subject, name_subject FROM SemesterSubject
		)ss2
		ON ss.ID_subject=ss2.ID_subject

		INNER JOIN(
			SELECT ID_schedule, ID_group, schedule FROM Schedule
		)s
		ON s.ID_schedule=ss.ID_schedule 
GO

CREATE PROCEDURE getClassroomFromSchedule(
					@career VARCHAR(MAX), @middle_name VARCHAR(MAX), @last_name VARCHAR(MAX),
					@name VARCHAR(MAX), @subject VARCHAR(MAX), @schedule VARCHAR(MAX)
				) AS
	DECLARE @id_career INT
	SET @id_career=(SELECT ID_career FROM Career WHERE name_career=@career)
	
	SELECT c.ID_classroom FROM Classroom c
		INNER JOIN(
			SELECT ID_classroom FROM Schedule s
			WHERE ID_career=@id_career 
					AND
				  ID_teacher=(
						SELECT ID_teacher FROM Teacher
						WHERE middle_name=@middle_name 
								AND 
							  last_name=@last_name 
								AND 
							  name_=@name 
								AND 
							  ID_career=@id_career
					)
					AND
				  ID_subject=(SELECT ID_subject FROM SemesterSubject WHERE ID_career=@id_career AND name_subject=@subject)
					AND
				  schedule=@schedule
		) s
		ON s.ID_classroom=c.ID_classroom
GO

CREATE PROCEDURE getInsertedSubjects(@enrollment INT) AS
	SELECT ss2.name_subject FROM StudentSchedule ss
		INNER JOIN(
			SELECT ID_career, ID_subject, name_subject FROM SemesterSubject
		)ss2
		ON ss2.ID_career=ss.ID_career and ss2.ID_subject = ss.ID_subject
	WHERE ID_student=@enrollment
GO

CREATE PROCEDURE insertStudentSchedule(@enrollment INT, @career VARCHAR(MAX), @id_classroom INT, @middle_name VARCHAR(MAX), @last_name VARCHAR(MAX), @name VARCHAR(MAX), @subject VARCHAR(MAX), @schedule VARCHAR(MAX)) AS
	DECLARE @id_career INT
	SET @id_career = (SELECT ID_career FROM Career WHERE name_career=@career)
	DECLARE @first_part TABLE(
		ID_faculty INT,
		ID_career INT,
		ID_student INT
	)
	INSERT INTO @first_part
		SELECT ID_faculty, ID_career, ID_student FROM Student
		WHERE ID_career=@id_career and ID_student=@enrollment
	------
	DECLARE @second_part TABLE(
		ID_classroom INT,
		ID_teacher INT,
		ID_subject INT,
		ID_schedule INT
	)
	INSERT INTO @second_part
		SELECT s.ID_classroom, t.ID_teacher, ss.ID_subject, s.ID_schedule FROM Schedule s
			INNER JOIN(
				SELECT ID_teacher FROM Teacher
				WHERE	ID_career=@id_career
							AND
						middle_name=@middle_name
							AND
						last_name=@last_name
							AND
						name_=@name
			)t
			ON s.ID_teacher=t.ID_teacher

			INNER JOIN(
				SELECT ID_subject FROM SemesterSubject
				WHERE	name_subject=@subject
							AND
						ID_career=@id_career
			)ss
			ON ss.ID_subject=s.ID_subject

		WHERE	s.ID_classroom=@id_classroom 
					AND
				s.schedule=@schedule
	
	
	INSERT INTO StudentSchedule
		SELECT ss.ID_faculty, s2.ID_classroom, ss.ID_career, s2.ID_teacher, ss.ID_student, s2.ID_subject, s2.ID_schedule FROM Schedule s
			FULL OUTER JOIN(
				SELECT * FROM @first_part
			)ss
			ON ss.ID_faculty=s.ID_faculty and ss.ID_career=s.ID_career

			INNER JOIN(
				SELECT * FROM @second_part
			)s2
			ON s2.ID_classroom=s.ID_classroom and s2.ID_schedule=s.ID_schedule and s2.ID_subject=s.ID_subject and s2.ID_teacher=s.ID_teacher
GO

CREATE PROCEDURE deleteStudentSchedule(@subject VARCHAR(MAX), @career VARCHAR(MAX), @enrollment INT) AS
	DECLARE @id_subject INT
	SET @id_subject=(SELECT ID_subject FROM SemesterSubject WHERE ID_career=(SELECT ID_career FROM Career WHERE name_career=@career) and name_subject=@subject) 
	
	DELETE FROM StudentSchedule
	WHERE ID_subject=@id_subject and ID_student=@enrollment
GO

CREATE PROCEDURE updateClassroomPlus(@id_classroom INT)AS
	UPDATE Classroom
		SET banches=(banches+1)
	WHERE ID_classroom=@id_classroom
GO

CREATE PROCEDURE updateClassroomMinus(@id_classroom INT) AS
	UPDATE Classroom
		SET banches=(banches-1)
	WHERE ID_classroom=@id_classroom
GO
------------------------------------- R E C T O R --------------------------------------------
--------------------------------------   A D D   ---------------------------------------------
------------------------------------ S t u d e n t -------------------------------------------

CREATE PROCEDURE getFaculties AS
	SELECT name_faculty FROM Faculty
GO

CREATE PROCEDURE getCareers(@faculty VARCHAR(100)) AS
	SELECT name_career FROM Career
		INNER JOIN (
			SELECT ID_faculty FROM Faculty
			WHERE Faculty.name_faculty = @faculty
		) facu
		ON facu.ID_faculty = Career.ID_faculty
GO

CREATE PROCEDURE getSubjects(@faculty VARCHAR(100), @career VARCHAR(100)) AS
	
	SELECT name_subject FROM SemesterSubject
	INNER JOIN(
		SELECT ID_faculty, name_faculty FROM Faculty
		WHERE name_faculty = @faculty
	) facu
	ON facu.ID_faculty = SemesterSubject.ID_faculty

	INNER JOIN(
		SELECT ID_faculty, ID_career, name_career FROM Career
		WHERE name_career = @career
	) career
	ON career.ID_career = SemesterSubject.ID_career		
GO

CREATE PROCEDURE getIds(@faculty VARCHAR(100), @career VARCHAR(100), @name_subject VARCHAR(100)) AS
	SELECT fac.ID_faculty, car.ID_career, s_b.ID_subject FROM SemesterSubject s_b
		INNER JOIN(
			SELECT ID_faculty FROM Faculty fac
			WHERE fac.name_faculty = @faculty
		) fac
		ON fac.ID_faculty = s_b.ID_faculty

		INNER JOIN(
			SELECT ID_career FROM Career car
			WHERE car.name_career = @career
		) car
		ON car.ID_career = s_b.ID_career

						INNER JOIN(
			SELECT ID_subject FROM SemesterSubject s_b2
			WHERE s_b2.name_subject = @name_subject
		) s_b2
		ON s_b2.ID_subject = s_b.ID_subject
GO

CREATE PROCEDURE verifyExistingStudent(@middle_name VARCHAR(20), @last_name VARCHAR(20), @name VARCHAR(40), @date_birth DATE) AS
	SELECT ISNULL(MAX(s.name_), '') AS Estudiante FROM Student s
		WHERE s.middle_name = @middle_name and s.last_name = @last_name and s.name_ = @name and s.date_birth = @date_birth
GO

CREATE PROCEDURE getStudent(@middle_name VARCHAR(20), @last_name VARCHAR(20), @name VARCHAR(40)) AS
	SELECT ISNULL(ID_faculty,''),ISNULL(ID_career,''),ISNULL(ID_student,''),ISNULL(middle_name,''),ISNULL(last_name,''),ISNULL(name_,''),ISNULL(date_birth,''),ISNULL(email,''),ISNULL(password_, '')
		FROM Student s
		RIGHT JOIN(
			SELECT ISNULL(MAX(s.name_), '') AS Estudiante FROM Student s
				WHERE s.middle_name = @middle_name and s.last_name = @last_name and s.name_ = @name
		) s2
		ON s2.Estudiante = '' or s2.Estudiante != ''
GO

CREATE PROCEDURE verifyExistingEmail(@email VARCHAR(40)) AS
	SELECT ISNULL(MAX(email), '') FROM Student
	WHERE email = @email
GO

CREATE PROCEDURE saveStudent @ID_faculty INT, @ID_career INT, @middle_name VARCHAR(20), @last_name VARCHAR(20), @name VARCHAR(40), @date_birth DATE, @email VARCHAR(50), @password VARCHAR(16), @student_status VARCHAR(4) AS
	INSERT INTO Student(ID_faculty , ID_career, middle_name, last_name, name_, date_birth, email, password_, student_status)
		VALUES(@ID_faculty , @ID_career, @middle_name, @last_name, @name, @date_birth, @email, @password, @student_status);
GO

CREATE PROCEDURE saveKardex(@ID_faculty INT, @ID_career INT, @ID_student INT, @ID_subject INT,@op1 VARCHAR(3),@op2 VARCHAR(3),@op3 VARCHAR(3),@op4 VARCHAR(3),@op5 VARCHAR(3),@op6 VARCHAR(3)) AS
	INSERT INTO Kardex (ID_faculty,ID_career,ID_student,ID_subject,op1,op2,op3,op4,op5,op6) 
		VALUES(@ID_faculty,@ID_career,@ID_student,@ID_subject,@op1,@op2,@op3,@op4,@op5,@op6);
GO
------------------------------------ T e a c h e r -------------------------------------------
CREATE PROCEDURE verifyExistingTeacherAsStudent(@middle_name VARCHAR(20), @last_name VARCHAR(20), @name VARCHAR(40)) AS
	SELECT ISNULL(MAX(s.name_), '') AS Estudiante FROM Student s
		WHERE s.middle_name = @middle_name and s.last_name = @last_name and s.name_ = @name
GO

CREATE PROCEDURE getTeacherIds(@faculty VARCHAR(100), @career VARCHAR(100)) AS
	SELECT fac.ID_faculty, car.ID_career FROM Career car
		INNER JOIN(
			SELECT ID_faculty FROM Faculty fac
			WHERE fac.name_faculty = @faculty
		) fac
		ON fac.ID_faculty = car.ID_faculty

		INNER JOIN(
			SELECT ID_career FROM Career car
			WHERE car.name_career = @career
		) car2
		ON car2.ID_career = car.ID_career
GO

CREATE PROCEDURE getTeacherEnrollment AS
	SELECT ISNULL(MAX(enrollment), 1000) FROM Teacher
GO

CREATE PROCEDURE verifyExistingTeacherEmail(@email VARCHAR(40)) AS
	SELECT ISNULL(MAX(email), '') FROM Student
	WHERE email = @email
GO

CREATE PROCEDURE verifyExistingTeacher(@middle_name VARCHAR(20), @last_name VARCHAR(20), @name VARCHAR(40), @email VARCHAR(50)) AS
	SELECT ISNULL(MAX(ID_faculty), 0), ISNULL(MAX(ID_career), 0), ISNULL(MAX(ID_teacher), 0), 
		   ISNULL(MAX(enrollment), 0),ISNULL(MAX(middle_name), ''), ISNULL(MAX(last_name), ''), ISNULL(MAX(name_), ''), 
		   ISNULL(MAX(email), ''), ISNULL(MAX(password_), ''), ISNULL(MAX(teacher_status), '')
			FROM Teacher t
	WHERE middle_name=@middle_name and last_name=@last_name and name_=@name and email=@email
GO

CREATE PROCEDURE saveTeacher(@ID_faculty INT, @ID_career INT, @enrollment INT, @middle_name VARCHAR(20), @last_name VARCHAR(20), @name VARCHAR(40), @email VARCHAR(50), @password VARCHAR(16), @teacher_status VARCHAR(4)) AS
	INSERT INTO Teacher(ID_faculty , ID_career, enrollment, middle_name, last_name, name_, email, password_, teacher_status)
		VALUES(@ID_faculty , @ID_career, @enrollment, @middle_name, @last_name, @name, @email, @password, @teacher_status);
GO
---------------------------------- C l a s s r o o m -----------------------------------------
CREATE PROCEDURE getClassroomData(@faculty VARCHAR(50),  @classroom VARCHAR(50)) AS
	SELECT ISNULL(MAX(f.ID_faculty), 0), ISNULL(MAX(c.ID_classroom), 0), ISNULL(MAX(banches), 0) FROM Classroom c
		INNER JOIN(
			SELECT ID_faculty FROM Faculty f
			WHERE f.name_faculty = @faculty
		) f
		ON f.ID_faculty = c.ID_faculty
	
		INNER JOIN(
			SELECT ID_faculty, ID_classroom FROM Classroom c
			WHERE classroom = @classroom
		) c2
		ON c2.ID_faculty = c.ID_faculty and c2.ID_classroom = c.ID_classroom
GO

CREATE PROCEDURE getIDFaculty(@faculty VARCHAR(50)) AS
	SELECT ID_faculty FROM Faculty f
	WHERE name_faculty = @faculty
GO

CREATE PROCEDURE getClassroom(@id_faculty INT, @classroom VARCHAR(MAX)) AS
	SELECT ISNULL(MAX(classroom),'') FROM Classroom
	WHERE ID_faculty = @id_faculty and classroom = @classroom
GO

CREATE PROCEDURE saveClassroom(@id_faculty INT, @classroom VARCHAR(MAX),@banches INT) AS
	INSERT INTO Classroom(ID_faculty, classroom, banches)
		VALUES(@id_faculty, @classroom, @banches)
GO

CREATE PROCEDURE getUnavailableSchedule(@id_faculty INT, @id_classroom INT) AS
	SELECT ID_career, ID_teacher, ID_subject,ID_schedule,ID_group,schedule FROM Schedule s
	WHERE s.ID_faculty = @id_faculty and s.ID_classroom = @id_classroom
GO

CREATE PROCEDURE getTeachers(@faculty VARCHAR(MAX), @career VARCHAR(MAX)) AS
	SELECT middle_name, last_name, name_ FROM Teacher t
		INNER JOIN(
			SELECT ID_faculty FROM Faculty f
			WHERE f.name_faculty = @faculty
		)f
		ON f.ID_faculty = t.ID_faculty

		INNER JOIN(
			SELECT ID_career FROM Career c
			WHERE c.name_career = @career
		)c
		ON c.ID_career = t.ID_career
GO

CREATE PROCEDURE getIdTeacher(@id_faculty INT, @id_career INT, @middle_name VARCHAR(MAX), @last_name VARCHAR(MAX), @name VARCHAR(MAX)) AS
	SELECT ID_teacher FROM Teacher t
	WHERE t.ID_faculty = @id_faculty and t.ID_career = @id_career and t.middle_name = @middle_name and t.last_name = @last_name and name_ = @name
GO

CREATE PROCEDURE getAllClassrooms(@id_faculty INT, @id_group VARCHAR(MAX)) AS
	SELECT schedule FROM Schedule
	WHERE @id_faculty=ID_faculty and @id_group=ID_group
GO

CREATE PROCEDURE saveSchedule(@id_faculty INT, @id_classroom INT, @id_career INT, @id_teacher INT, @id_subject INT, @ID_group VARCHAR(MAX), @schedule VARCHAR(MAX)) AS
	INSERT INTO Schedule(ID_faculty, ID_classroom, ID_career, ID_teacher, ID_subject, ID_group, schedule)
		VALUES(@id_faculty,@id_classroom,@id_career,@id_teacher,@id_subject,@ID_group,@schedule)
GO

--
--
-------------------------------------- U P D A T E -------------------------------------------
---------------------------------------- Student ---------------------------------------------
CREATE PROCEDURE updateStudent(@ID_student INT, @faculty VARCHAR(MAX), @career VARCHAR(MAX), @middle_name VARCHAR(MAX), @last_name VARCHAR(MAX), @name VARCHAR(MAX), @date_birth VARCHAR(MAX), @email VARCHAR(MAX), @password VARCHAR(MAX), @status VARCHAR(MAX)) AS
	UPDATE Student
		SET ID_faculty=(SELECT ID_faculty FROM Faculty WHERE name_faculty=@faculty),
			ID_career=(SELECT ID_career FROM Career WHERE name_career=@career),
			middle_name=@middle_name,
			last_name=@last_name,
			name_=@name,
			date_birth=@date_birth,
			email=@email,
			password_=@password,
			student_status=@status
		WHERE ID_student=@ID_student
GO

CREATE PROCEDURE deleteKardex(@ID_student VARCHAR(MAX)) AS
	DELETE FROM Kardex
	WHERE ID_student=@ID_student
GO

---------------------------------------- Teacher ---------------------------------------------
CREATE PROCEDURE getTeacher(@middle_name VARCHAR(20), @last_name VARCHAR(20), @name VARCHAR(40), @career VARCHAR(MAX)) AS
	SELECT ISNULL(ID_teacher,'') FROM Teacher t
	WHERE	middle_name=@middle_name
				AND
			last_name=@last_name
				AND
			name_=@name
				AND
			ID_career=(SELECT ID_career FROM Career WHERE name_career=@career)
GO

CREATE PROCEDURE getIDFac_CarTeacher(@faculty VARCHAR(MAX), @career VARCHAR(MAX)) AS
	SELECT ID_faculty, ID_career FROM Career
	WHERE	ID_faculty=(SELECT ID_faculty FROM Faculty WHERE name_faculty=@faculty)
				AND
			ID_career=(SELECT ID_career FROM Career WHERE name_career=@career)
GO

CREATE PROCEDURE updateTeacher(@id_faculty INT, @id_career INT, @enrollment INT, @faculty VARCHAR(MAX), @career VARCHAR(MAX), @middle_name VARCHAR(MAX), @last_name VARCHAR(MAX), @name VARCHAR(MAX), @email VARCHAR(MAX), @password VARCHAR(MAX), @status VARCHAR(MAX)) AS
	UPDATE Teacher
		SET ID_faculty=(SELECT ID_faculty FROM Faculty WHERE name_faculty=@faculty),
			ID_career=(SELECT ID_career FROM Career WHERE name_career=@career)
		WHERE ID_faculty=@id_faculty AND ID_career=@id_career AND enrollment=@enrollment
	
	UPDATE Teacher
		SET	middle_name=@middle_name,
			last_name=@last_name,
			name_=@name,
			email=@email,
			password_=@password,
			teacher_status=@status
		WHERE enrollment=@enrollment
GO
--------------------------------------- Classroom --------------------------------------------
CREATE PROCEDURE updateClassroom(@faculty VARCHAR(MAX), @classroom VARCHAR(MAX), @classroom2 VARCHAR(MAX), @banches VARCHAR(MAX), @banches2 VARCHAR(MAX)) AS
	UPDATE Classroom
		SET		classroom=@classroom2,
				banches=@banches2

		WHERE	ID_faculty=(SELECT ID_faculty FROM Faculty WHERE name_faculty=@faculty)
					AND
				classroom=@classroom
					AND
				banches=@banches
GO
------------------------------------ S C H E D U L E -----------------------------------------
CREATE PROCEDURE updateSchedule(@faculty VARCHAR(MAX), @career VARCHAR(MAX), @classroom VARCHAR(MAX), @schedule VARCHAR(MAX), @new_schedule VARCHAR(MAX)) AS
	DECLARE @id_faculty INT
	SET @id_faculty=(SELECT ID_faculty FROM Faculty WHERE name_faculty=@faculty)
	
	DECLARE @id_career INT
	SET @id_career=(SELECT ID_career FROM Career WHERE name_career=@career)

	DECLARE @id_classroom INT
	SET @id_classroom=(SELECT ID_classroom FROM Classroom WHERE classroom=@classroom AND ID_faculty=@id_faculty)

	UPDATE Schedule
		SET schedule=@new_schedule

		WHERE ID_faculty=@id_faculty AND ID_career=@id_career AND ID_classroom=@ID_classroom AND schedule=@schedule
GO
-------------------------------------- D E L E T E -------------------------------------------
---------------------------------------- Student ---------------------------------------------
CREATE PROCEDURE getStudentInfo(@ID_student INT) AS
	SELECT f.name_faculty, c.name_career, s.middle_name, s.last_name, s.name_, s.date_birth, s.email, s.password_, s.student_status
	FROM Student s
		INNER JOIN(
			SELECT ID_faculty, name_faculty FROM Faculty
		)f
		ON f.ID_faculty = s.ID_faculty

		INNER JOIN(
			SELECT ID_career, name_career FROM Career c
		)c
		ON c.ID_career = s.ID_career
	WHERE @ID_student = s.ID_student
GO

CREATE PROCEDURE deleteStudent(@ID_student INT) AS
	ALTER TABLE Kardex 
		DROP CONSTRAINT STUDENT_FK_KARDEX

	ALTER TABLE StudentSchedule
		DROP CONSTRAINT STUDENT_FK_STUDENTSCHEDULE

	DELETE FROM Student
	WHERE ID_student = @ID_student;

	ALTER TABLE Kardex
		ADD CONSTRAINT STUDENT_FK_KARDEX FOREIGN KEY(ID_student)
		REFERENCES Student(ID_student)

	ALTER TABLE StudentSchedule
		ADD CONSTRAINT STUDENT_FK_STUDENTSCHEDULE FOREIGN KEY(ID_student)
		REFERENCES Student(ID_student)
GO
---------------------------------------- Teacher ------------------------------------------------
CREATE PROCEDURE getTeacherCareers(@enrollment INT) AS
	SELECT c.name_career FROM Career c
		INNER JOIN(
			SELECT ID_career, enrollment FROM Teacher t
		) t
		ON t.enrollment = @enrollment
	WHERE c.ID_career = t.ID_career
GO

CREATE PROCEDURE getTeacherInfo(@enrollment INT, @career VARCHAR(MAX)) AS
	SELECT f.name_faculty, c.name_career, t.middle_name, t.last_name, t.name_, t.email, t.password_, t.teacher_status 
	FROM Teacher t
		INNER JOIN(
			SELECT ID_faculty, name_faculty FROM Faculty
		)f
		ON f.ID_faculty = t.ID_faculty

		INNER JOIN(
			SELECT ID_career, name_career FROM Career
		)c
		ON c.name_career = @career

	WHERE t.enrollment = @enrollment
GO

CREATE PROCEDURE deleteTeacher(@enrollment INT, @career VARCHAR(MAX)) AS
	ALTER TABLE Schedule
		DROP CONSTRAINT TEACHER_FK_SCHEDULE

	ALTER TABLE StudentSchedule
		DROP CONSTRAINT TEACHER_FK_STUDENTSCHEDULE

	DELETE FROM Teacher
	WHERE enrollment=@enrollment and ID_career=(SELECT ID_career FROM Career WHERE name_career=@career)

	ALTER TABLE Schedule
		ADD CONSTRAINT TEACHER_FK_SCHEDULE FOREIGN KEY(ID_student)
		REFERENCES Student(ID_student)

	ALTER TABLE StudentSchedule
		ADD CONSTRAINT TEACHER_FK_STUDENTSCHEDULE FOREIGN KEY(ID_student)
		REFERENCES Student(ID_student)
GO
---------------------------------------- Classroom ------------------------------------------------
/*
CREATE PROCEDURE getClassroomInfo(@faculty VARCHAR(MAX), @classroom VARCHAR(MAX)) AS
	SELECT f.name_faculty, c.classroom, c.banches FROM Classroom c
		INNER JOIN(
			SELECT ID_faculty, name_faculty FROM Faculty
		)f
		ON f.ID_faculty = c.ID_faculty and f.name_faculty = @faculty
	WHERE c.classroom = @classroom
GO
*/

CREATE PROCEDURE getClassrooms(@faculty VARCHAR(MAX)) AS
	SELECT classroom FROM Classroom
	WHERE ID_faculty=(SELECT ID_faculty FROM Faculty WHERE name_faculty=@faculty)
GO

CREATE PROCEDURE getBanches(@faculty VARCHAR(MAX), @classroom VARCHAR(MAX)) AS
	SELECT banches FROM Classroom
	WHERE ID_faculty=(SELECT ID_faculty FROM Faculty WHERE name_faculty=@faculty) 
			and 
		  ID_classroom=(SELECT ID_classroom FROM Classroom WHERE classroom=@classroom)
GO

CREATE PROCEDURE deleteClassroom(@faculty VARCHAR(MAX), @classroom VARCHAR(MAX)) AS
	ALTER TABLE Schedule
		DROP CONSTRAINT CLASSROOM_FK_SCHEDULE

	ALTER TABLE StudentSchedule
		DROP CONSTRAINT CLASSROOM_FK_STUDENTSCHEDULE

	DELETE FROM Classroom
	WHERE ID_faculty = (SELECT ID_faculty FROM Faculty WHERE name_faculty=@faculty)
			and
		  classroom = @classroom

	ALTER TABLE Schedule
		ADD CONSTRAINT CLASSROOM_FK_SCHEDULE FOREIGN KEY(ID_classroom)
		REFERENCES Schedule(ID_schedule)

	ALTER TABLE StudentSchedule
		ADD CONSTRAINT CLASSROOM_FK_STUDENTSCHEDULE FOREIGN KEY(ID_classroom)
		REFERENCES StudentSchedule(ID_student_schedule)
GO
----------------------------------------- Schedule ------------------------------------------------
CREATE PROCEDURE getSchedules(@faculty VARCHAR(MAX), @classroom VARCHAR(MAX)) AS
	SELECT schedule FROM Schedule
	WHERE ID_faculty=(SELECT ID_faculty FROM Faculty WHERE name_faculty=@faculty)
			and
		  ID_classroom=(SELECT ID_classroom FROM Classroom WHERE classroom=@classroom)
GO

CREATE PROCEDURE getC_T(@faculty VARCHAR(MAX), @classroom VARCHAR(MAX), @schedule VARCHAR(MAX)) AS-- C = CAREER & T = TEACHER
	DECLARE @id_career INT
	SET @id_career=(
			SELECT ID_career FROM Schedule
			WHERE ID_faculty=(
					SELECT ID_faculty FROM Faculty
					WHERE name_faculty=@faculty
				  ) 
					AND
				  ID_classroom=(
					SELECT ID_classroom FROM Classroom
					WHERE classroom=@classroom
				  )
					AND
				  schedule=@schedule	
		)
	
	SELECT c.name_career, t.middle_name, t.last_name, t.name_ FROM Teacher t
		INNER JOIN(
			SELECT ID_career, name_career FROM Career
		)c
		ON c.ID_career=@id_career 
GO

CREATE PROCEDURE getScheduleInfo(@subject VARCHAR(MAX), @id_group VARCHAR(MAX)) AS
	SELECT f.name_faculty, c.classroom, c2.name_career, t.middle_name, t.last_name, t.name_, s_s.name_subject, s.ID_group, s.schedule
	FROM Schedule s
		INNER JOIN(
			SELECT ID_faculty, name_faculty FROM Faculty
		)f
		ON f.ID_faculty = s.ID_faculty

		INNER JOIN(
			SELECT ID_classroom, classroom FROM Classroom
		)c
		ON c.ID_classroom=s.ID_classroom

		INNER JOIN(
			SELECT ID_career, name_career FROM Career
		)c2
		ON c2.ID_career = s.ID_career

		INNER JOIN(
			SELECT ID_teacher, middle_name, last_name, name_ FROM Teacher
		)t
		ON t.ID_teacher = s.ID_teacher

		INNER JOIN(
			SELECT ID_subject, name_subject FROM SemesterSubject 
		)s_s
		ON s_s.ID_subject = s.ID_subject and s_s.name_subject = @subject

	WHERE s.ID_group=@id_group
GO

CREATE PROCEDURE restartClassroom(@faculty VARCHAR(MAX), @classroom VARCHAR(MAX)) AS
	ALTER TABLE StudentSchedule
		DROP CONSTRAINT SCHEDULE_FK_STUDENTSCHEDULE

	DELETE FROM Schedule
	WHERE ID_faculty=(
			SELECT ID_faculty FROM Faculty
			WHERE name_faculty=@faculty
		  )
			AND
		  ID_classroom=(
			SELECT ID_classroom FROM Classroom
			WHERE classroom=@classroom
		  )

	ALTER TABLE StudentSchedule
		ADD CONSTRAINT SCHEDULE_FK_STUDENTSCHEDULE FOREIGN KEY(ID_schedule)
		REFERENCES Schedule(ID_schedule)
GO

CREATE PROCEDURE deleteSchedule(@faculty VARCHAR(MAX), @classroom VARCHAR(MAX), @schedule VARCHAR(MAX)) AS
	ALTER TABLE StudentSchedule
		DROP CONSTRAINT SCHEDULE_FK_STUDENTSCHEDULE

	DELETE FROM Schedule
	WHERE ID_faculty=(
			SELECT ID_faculty FROM Faculty
			WHERE name_faculty=@faculty
		  )
			AND
		  ID_classroom=(
			SELECT ID_classroom FROM Classroom
			WHERE classroom=@classroom
		  )
			AND
		  schedule=@schedule

	ALTER TABLE StudentSchedule
		ADD CONSTRAINT SCHEDULE_FK_STUDENTSCHEDULE FOREIGN KEY(ID_schedule)
		REFERENCES Schedule(ID_schedule)
GO

