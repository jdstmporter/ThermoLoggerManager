use AllSaints;

UPDATE records
SET sensor = (
    SELECT name FROM (
        SELECT r.seq as pk, IFNULL(s.name, r.mac) as name, r.mac
        FROM records r
        LEFT JOIN sensors s ON r.mac = s.mac) t
    WHERE seq = t.pk)
WHERE true;