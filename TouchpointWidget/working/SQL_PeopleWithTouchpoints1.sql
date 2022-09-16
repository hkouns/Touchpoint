Select * FROM dbo.TaskNote AS t1
    WHERE (t1.IsNote = 'TRUE') AND (t1.DueDate >= '08/19/21 00:00:00') AND (EXISTS(
        SELECT NULL AS EMPTY
        FROM dbo.TaskNoteKeyword AS t2
        WHERE (t2.KeywordId IN (8, 9, 11, 12, 13, 14, 15, 16, 34)) AND (t2.TaskNoteId = t1.TaskNoteId) 
        )) 
    ORDER BY AboutPersonId