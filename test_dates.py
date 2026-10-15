import unittest
from dates import apply_dates

class PublicationDateTests(unittest.TestCase):
 def test_utc_evening_is_next_beijing_day(self):
  p={'published':'2026-10-13T23:01:21Z','first_seen':'2026-10-15T01:38:21Z'}
  apply_dates(p,{'published':'2026-10-13','source':'arXiv abstract','version_date':'2026-10-13T23:01:21+00:00'})
  self.assertEqual(p['publication_date'],'2026-10-14')
  self.assertEqual(p['published'],'2026-10-13T23:01:21Z')
  self.assertEqual(p['first_seen'],'2026-10-15T01:38:21Z')
  self.assertEqual(p['version_date'],'2026-10-13T23:01:21+00:00')

 def test_api_timestamp_without_cached_date(self):
  p={'published':'2026-10-13T17:59:34+00:00'}
  apply_dates(p,None)
  self.assertEqual(p['publication_date'],'2026-10-14')

 def test_date_only_metadata_keeps_its_precision(self):
  for value in ['2026-10-13','2026-10','2026']:
   p={'published':value}
   apply_dates(p,None)
   self.assertEqual(p['publication_date'],value)

 def test_rss_announcement_is_not_first_submission(self):
  p={'published':'2026-10-14T01:00:00Z','date_kind':'announcement'}
  apply_dates(p,{'published':'2026-10-12','source':'arXiv abstract'})
  self.assertEqual(p['publication_date'],'2026-10-12')

 def test_disagreement_preserves_verified_date(self):
  p={'published':'2026-10-13T23:00:00Z'}
  apply_dates(p,{'published':'2026-10-12','source':'arXiv abstract'})
  self.assertEqual(p['publication_date'],'2026-10-12')

 def test_offset_and_utc_day_boundary(self):
  p={'published':'2026-10-14T09:24:35+08:00'}
  apply_dates(p,{'published':'2026-10-14','source':'arXiv abstract'})
  self.assertEqual(p['publication_date'],'2026-10-14')

if __name__=='__main__':unittest.main()
