-- ============================================================
-- CRICKET DATA ENGINEERING PIPELINE
-- Redshift Data Validation Tests
-- ============================================================
-- Purpose:
-- Validate that cricket match data has been loaded correctly
-- from Amazon S3 into the Redshift cricket_matches table.
--
-- Last validated: 2026-08-12
-- ============================================================


-- ============================================================
-- TEST CASE TC-RED-001
-- Verify that the cricket_matches table contains data
-- ============================================================

SELECT COUNT(*) AS total_matches
FROM cricket_matches;

-- Expected Result:
-- 25 matches
-- Status: PASS


-- ============================================================
-- TEST CASE TC-RED-002
-- Verify match status distribution
-- ============================================================

SELECT
    match_started,
    match_ended,
    COUNT(*) AS matches
FROM cricket_matches
GROUP BY match_started, match_ended
ORDER BY match_started DESC, match_ended DESC;

-- Expected Result:
-- match_started | match_ended | matches
-- true          | true        | 16
-- true          | false       | 1
-- false         | false       | 8
--
-- Status: PASS


-- ============================================================
-- TEST CASE TC-RED-003
-- Verify that match_id is populated
-- ============================================================

SELECT COUNT(*) AS missing_match_ids
FROM cricket_matches
WHERE match_id IS NULL
   OR TRIM(match_id) = '';

-- Expected Result:
-- 0
-- Status: PASS if result = 0


-- ============================================================
-- TEST CASE TC-RED-004
-- Verify that match_name is populated
-- ============================================================

SELECT COUNT(*) AS missing_match_names
FROM cricket_matches
WHERE match_name IS NULL
   OR TRIM(match_name) = '';

-- Expected Result:
-- 0
-- Status: PASS if result = 0


-- ============================================================
-- TEST CASE TC-RED-005
-- Verify that match dates are populated
-- ============================================================

SELECT COUNT(*) AS missing_match_dates
FROM cricket_matches
WHERE match_date IS NULL;

-- Expected Result:
-- 0
-- Status: PASS if result = 0


-- ============================================================
-- TEST CASE TC-RED-006
-- Verify that teams are populated
-- ============================================================

SELECT COUNT(*) AS missing_teams
FROM cricket_matches
WHERE team1 IS NULL
   OR team2 IS NULL;

-- Expected Result:
-- 0
-- Status: PASS if result = 0


-- ============================================================
-- TEST CASE TC-RED-007
-- Verify that venue is populated
-- ============================================================

SELECT COUNT(*) AS missing_venues
FROM cricket_matches
WHERE venue IS NULL
   OR TRIM(venue) = '';

-- Expected Result:
-- 0
-- Status: PASS if result = 0


-- ============================================================
-- TEST CASE TC-RED-008
-- Verify that series_id is populated
-- ============================================================

SELECT COUNT(*) AS missing_series_ids
FROM cricket_matches
WHERE series_id IS NULL
   OR TRIM(series_id) = '';

-- Expected Result:
-- 0
-- Status: PASS if result = 0


-- ============================================================
-- TEST CASE TC-RED-009
-- Verify that match_id values are unique
-- ============================================================

SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT match_id) AS unique_match_ids
FROM cricket_matches;

-- Expected Result:
-- total_rows = unique_match_ids
-- Status: PASS if both values are equal


-- ============================================================
-- TEST CASE TC-RED-010
-- Verify that match_date and match_datetime_gmt are consistent
-- ============================================================

SELECT COUNT(*) AS inconsistent_dates
FROM cricket_matches
WHERE match_datetime_gmt IS NOT NULL
  AND match_date <> CAST(match_datetime_gmt AS DATE);

-- Expected Result:
-- 0
-- Status: PASS if result = 0


-- ============================================================
-- TEST CASE TC-RED-011
-- Verify that the table can be queried successfully
-- ============================================================

SELECT *
FROM cricket_matches
LIMIT 10;

-- Expected Result:
-- Query executes successfully and returns cricket match records.
-- Status: PASS