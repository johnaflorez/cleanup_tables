DELETE
  FROM {db_table_name}
  WHERE {primary_key_name} IN (
    SELECT
    {primary_key_name}
    FROM {db_table_name}
    WHERE {db_condition}
    ORDER BY
      {primary_key_name} DESC
    OFFSET 0 ROWS
    FETCH NEXT {limit} ROWS ONLY)
