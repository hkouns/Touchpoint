DECLARE @KeywordList VARCHAR(MAX) = '8,9,11,12,13,14,15,16,34';
DECLARE @ContactsDaysBack INT = 365;
DECLARE @mincontactdate DATETIME = DATEADD(DAY, -@ContactsDaysBack, GETDATE());

;WITH TaskNoteKeywordCriteria AS (
	SELECT [Value] AS KeywordId FROM [dbo].[SplitInts](@KeywordList)
)

SELECT 
	t1.AboutPersonId,
    min(DATEDIFF(Day, DueDate, GETDATE())) as daysback
FROM 
	dbo.TaskNote AS t1
WHERE 1=1
	AND t1.IsNote = 1
    AND t1.DueDate >= @mincontactdate
    AND EXISTS (
			SELECT 
				NULL AS EMPTY
			FROM 
				dbo.TaskNoteKeyword AS t2
					INNER JOIN TaskNoteKeywordCriteria tnk ON t2.KeywordId = tnk.KeywordId
			WHERE 
				t2.TaskNoteId = t1.TaskNoteId
		)
GROUP BY 
	t1.AboutPersonId