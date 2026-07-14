-- Reference queries for ingestion cadence monitoring.
-- Runtime path: app/ingestion/cadence_stats.py (joins schedule intervals in Python).

-- Active catalog + fetch health inputs
SELECT
  id,
  name,
  platform,
  fetch_tier,
  is_active,
  consecutive_fetch_failures,
  last_successful_fetch_at
FROM companies
WHERE is_active
ORDER BY name ASC;

-- Recent successful polls (for observed interval between fetches)
SELECT company_id, completed_at
FROM (
  SELECT
    company_id,
    completed_at,
    ROW_NUMBER() OVER (
      PARTITION BY company_id
      ORDER BY completed_at DESC
    ) AS rn
  FROM company_run_results
  WHERE status = 'success'
    AND completed_at IS NOT NULL
) ranked
WHERE rn <= 8
ORDER BY company_id, completed_at DESC;
