import datetime as dt
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import update_journals as j

class JournalRecovery(unittest.TestCase):
 def test_month_boundaries(self):
  w=j.month_windows(dt.date(2024,3,12),3)
  self.assertEqual(w[0][0],'2024-01')
  self.assertEqual(w[1][2],dt.date(2024,2,29))
  self.assertEqual(w[2][2],dt.date(2024,3,12))
 def test_cached_publisher_abstract(self):
  p={'title':'Test','abstract':'','journal':'Nature Geoscience'}
  prior={'title':'Test','publisher_abstract':'Verified abstract','abstract_source':'https://www.nature.com/articles/test'}
  out=j.publisher_abstract(p,prior,'2026-09-24T00:00:00+00:00')
  self.assertEqual(out['abstract'],'Verified abstract');self.assertFalse(out['metadata_limited'])
 def test_failed_statistics_not_zero(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);(root/'journal_records.json').write_text(json.dumps({'papers':[],'sources':{}}))
   (root/'journals.json').write_text(json.dumps({'journals':[{'id':'test','issn':'test','name':'Test'}]}))
   with patch.object(j,'ROOT',root),patch.object(j,'get',side_effect=RuntimeError('offline')):out=j.update_monthly()
   self.assertTrue(all(x['status']=='error' and 'count' not in x for x in out['test'].values()))
 def test_overlapping_queries_deduplicate_and_preserve_dates(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);stamp='2026-01-01T00:00:00+00:00';journal={'id':'test','issn':'test','name':'Test','group':'ocean','enabled':True}
   raw={'DOI':'10.1/test','title':['Ocean circulation'],'published':{'date-parts':[[2026,9,1]]}}
   paper=j.parse_record(raw,journal,stamp)
   (root/'journal_records.json').write_text(json.dumps({'papers':[paper],'sources':{'test':{'last_success':stamp}},'monthly_statistics':{'test':{'old':'keep'}}}))
   (root/'journals.json').write_text(json.dumps({'journals':[journal]}));(root/'topics.json').write_text(Path('topics.json').read_text())
   with patch.object(j,'ROOT',root),patch.object(j,'get',return_value={'items':[raw]}) as get:
    self.assertFalse(j.update());self.assertEqual(get.call_count,2)
   out=json.loads((root/'journal_records.json').read_text());self.assertEqual(len(out['papers']),1);self.assertEqual(out['papers'][0]['first_seen'],stamp);self.assertEqual(out['sources']['test']['fetched'],1);self.assertEqual(out['monthly_statistics']['test']['old'],'keep')
