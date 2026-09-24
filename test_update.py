import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import update

CONFIG=json.loads(Path('topics.json').read_text())
class Rules(unittest.TestCase):
 def paper(self,title,abstract='',categories=None):
  return {'id':'test','title':title,'abstract':abstract,'categories':categories or []}
 def test_mechanism_bridge(self):
  self.assertEqual(update.classify(self.paper('Rossby waves in rotating fluid'),CONFIG)['status'],'candidate')
 def test_pollution_review(self):
  self.assertEqual(update.classify(self.paper('Air pollution and convection'),CONFIG)['status'],'excluded')
 def test_no_blanket_aerosol_exclusion(self):
  self.assertEqual(update.classify(self.paper('Aerosol cloud feedback on planets'),CONFIG)['status'],'candidate')
 def test_boundary(self):
  self.assertEqual(update.classify(self.paper('Nonvolatile memory'),CONFIG)['status'],'unmatched')
 def test_manual_override(self):
  c={**CONFIG,'overrides':{'test':{'status':'candidate','reason':'Physical mechanism relevant'}}}
  self.assertEqual(update.classify(self.paper('Air pollution'),c)['method'],'manual')
 def test_failure_checkpoint(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d); (root/'topics.json').write_text(json.dumps({**CONFIG,'categories':['astro-ph.EP']}))
   (root/'papers.json').write_text(json.dumps({'papers':[],'sources':{'astro-ph.EP':{'last_success':'2026-01-01T00:00:00+00:00'}}}))
   with patch.object(update,'ROOT',root),patch.object(update,'request_feed',side_effect=RuntimeError('offline')),patch.object(update,'rss_feed',side_effect=RuntimeError('offline')):
    self.assertTrue(update.update())
   s=json.loads((root/'papers.json').read_text())['sources']['astro-ph.EP']
   self.assertEqual(s['last_success'],'2026-01-01T00:00:00+00:00');self.assertEqual(s['status'],'error')
 def test_duplicate_runs(self):
  p={**self.paper('Planet habitability',categories=['astro-ph.EP']),'id':'2609.00001','version_id':'2609.00001v1','published':'2026-09-24T00:00:00+00:00','updated':'2099-01-01T00:00:00+00:00'}
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);(root/'topics.json').write_text(json.dumps({**CONFIG,'categories':['astro-ph.EP']}))
   with patch.object(update,'ROOT',root),patch.object(update,'request_feed',side_effect=lambda *a:(1,[dict(p)])):
    update.update()
    first=json.loads((root/'papers.json').read_text())['papers'][0]['first_seen']
    update.update()
    self.assertEqual(first,json.loads((root/'papers.json').read_text())['papers'][0]['first_seen'])
   self.assertEqual(len(json.loads((root/'papers.json').read_text())['papers']),1)
if __name__=='__main__': unittest.main()
