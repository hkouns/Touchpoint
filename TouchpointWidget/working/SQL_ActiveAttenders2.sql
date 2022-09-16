DECLARE @AttendanceDaysBack INT = 180;
DECLARE @MinAttendanceDate DATETIME = DATEADD(DAY, -@AttendanceDaysBack, GETDATE());
DECLARE @VisitNum INT = 6;
DECLARE @AttendanceDiv INT = 18; --Div 18 = Worship Attendance

	SELECT 
		a.PeopleId
    FROM 
		dbo.Attend a
    WHERE a.AttendanceFlag = 1
        AND a.MeetingDate > @MinAttendanceDate
        AND (EXISTS(
            SELECT NULL AS EMPTY
            FROM dbo.Organizations AS t2, dbo.DivOrg AS t3
            WHERE ((t3.DivId) = @AttendanceDiv) 
            AND (t2.OrganizationId = a.OrganizationId) 
            AND (t3.OrgId = t2.OrganizationId)
            ))
    GROUP BY 
		a.PeopleId
	HAVING 
		COUNT(a.PeopleId) >= @VisitNum