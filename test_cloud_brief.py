import datetime as dt
import unittest
from build_catalog import daily_brief

class CloudBriefTests(unittest.TestCase):
 def test_beijing_dates_older_additions_and_failed_sources_stay_distinct(self):
  papers=[{'id':'recent','first_seen':'2026-10-14T17:00:00Z','publication_date':'2026-10-14'},
          {'id':'older','first_seen':'2026-10-15T01:00:00Z','publication_date':'2026-03'},
          {'id':'updated','first_seen':'2026-10-01','version_date':'2026-10-15','source':'arXiv','version_id':'2610.00001v2'},
          {'id':'previous','first_seen':'2026-10-14T15:59:59Z','publication_date':'2026-10-14'}]
  result=daily_brief(papers,{'arXiv':{'status':'failed'},'journal:disabled':{'status':'failed'}},{'journals':[{'id':'disabled','enabled':False}]},dt.datetime(2026,10,15,2,tzinfo=dt.timezone.utc))
  self.assertEqual(result['new_count'],2)
  self.assertEqual(result['recent_ids'],['recent'])
  self.assertEqual(result['older_ids'],['older'])
  self.assertEqual(result['updated_ids'],['updated'])
  self.assertEqual(result['source_issues'],[{'name':'arXiv','status':'failed'}])
