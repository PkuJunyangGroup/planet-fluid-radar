import copy
import unittest
from build_catalog import apply_publisher_supplements
from update import classify

class ReviewOverrides(unittest.TestCase):
 def test_affiliation_repair_is_scoped_and_preserves_abstract_and_dates(self):
  p={'id':'doi:10/example','doi':'10/example','abstract':'Journal abstract','first_seen':'2026-10-17','publication_date':'2026-10-16','institutions':['University of California'],'author_affiliations':[{'name':'A Author','orcid':'https://orcid.org/0000-0001-6635-5080','institutions':['University of California']}]}
  other=copy.deepcopy(p);other['doi']='10/other'
  mismatch=copy.deepcopy(p);mismatch['author_affiliations'][0]['orcid']='different'
  repair={'name':'A Author','orcid':'https://orcid.org/0000-0001-6635-5080','institutions':['University of California, Los Angeles'],'source_url':'https://arxiv.org/html/2607.04629v2','checked_date':'2026-10-17'}
  apply_publisher_supplements([p,other,mismatch],{'10/example':{'author_affiliation_repairs':[repair]}})
  self.assertEqual(p['institutions'],repair['institutions'])
  self.assertEqual(other['institutions'],['University of California'])
  self.assertEqual(mismatch['institutions'],['University of California'])
  self.assertEqual(p['abstract'],'Journal abstract')
  self.assertEqual(p['first_seen'],'2026-10-17')
  self.assertEqual(p['publication_date'],'2026-10-16')
 def test_review_tags_override_only_target(self):
  config={'exclude_terms':[],'topics':[],'mechanisms':[{'label':'Broad tag','terms':['surface']}],'overrides':{'target':{'status':'candidate','reason':'Read','tags':['Clouds']}}}
  p={'id':'target','title':'surface gravity','abstract':'','authors':[]}
  self.assertEqual(classify(p,config)['tags'],['Clouds'])
  self.assertEqual(classify({**p,'id':'other'},config)['tags'],['Broad tag'])

if __name__=='__main__':unittest.main()
