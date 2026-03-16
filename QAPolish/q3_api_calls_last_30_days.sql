-- SQL (Postgres) to find users with more than 5 API calls in the last 30 days
-- Adjust the interval syntax if using MySQL (use DATE_SUB/INTERVAL) or other dialects

SELECT
    u.user_id,
    u.username
FROM users u
JOIN api_logs l ON l.user_id = u.user_id
WHERE l.timestamp >= NOW() - INTERVAL '30 days'
GROUP BY u.user_id, u.username
HAVING COUNT(*) > 5;

-- MySQL equivalent (commented):
-- SELECT u.user_id, u.username
-- FROM users u
-- JOIN api_logs l ON l.user_id = u.user_id
-- WHERE l.timestamp >= DATE_SUB(NOW(), INTERVAL 30 DAY)
-- GROUP BY u.user_id, u.username
-- HAVING COUNT(*) > 5;
