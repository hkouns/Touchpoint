DECLARE @AttendanceDaysBack INT = 180;
DECLARE @MinAttendanceDate DATETIME = DATEADD(DAY, -@AttendanceDaysBack, GETDATE());
DECLARE @VisitNum INT = 6;

	SELECT 
		a.PeopleId
    FROM 
		dbo.Attend a
    WHERE a.AttendanceFlag = 1
        AND a.MeetingDate > @MinAttendanceDate
        
    GROUP BY 
		a.PeopleId
	HAVING 
		COUNT(a.PeopleId) >= @VisitNum