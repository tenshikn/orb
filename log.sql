

SELECT vault.photo, vault.title, entries.date_added, entries.entry_heading, entries.entry FROM
vault JOIN entries ON vault.title=entries.title WHERE vault.user_id=1 GROUP BY entries.title;