import unittest
import enrich
import dates
class Enrichment(unittest.TestCase):
 def test_explicit_author_mapping_only(self):
  html='<div class="ltx_role_author"><span class="ltx_personname">A</span><div class="ltx_role_affiliation">Institute A</div></div><div class="ltx_role_author"><span class="ltx_personname">B</span></div><span class="ltx_role_affiliation">Institute B</span>'
  orgs,authors=enrich.affiliations(html)
  self.assertEqual(orgs,['Institute A','Institute B'])
  self.assertEqual(authors[0]['institutions'],['Institute A'])
  self.assertEqual(authors[1]['institutions'],[])
 def test_note_invalidated_by_version_or_abstract(self):
  p={'id':'1','version_id':'1v1','title':'Title','abstract':'An abstract.'}
  notes={'1':{'version_id':'1v1','abstract_sha256':enrich.digest(p),'zh':'导读','en':'Note'}}
  enrich.apply_notes(p,notes);self.assertEqual(p['intro_kind'],'bilingual_editorial')
  p['abstract']='Changed abstract.';enrich.apply_notes(p,notes);self.assertEqual(p['intro_kind'],'abstract_excerpt')
  p['abstract']='An abstract.';p['version_id']='1v2';enrich.apply_notes(p,notes);self.assertEqual(p['intro_kind'],'abstract_excerpt')
 def test_note_basis_and_source(self):
  p={'id':'1','version_id':'v1','title':'Title','abstract':''}
  n={'version_id':'v1','abstract_sha256':enrich.digest(p),'zh':'标题介绍','en':'','basis':'title only'}
  enrich.apply_notes(p,{'1':n});self.assertIn('仅依据标题',p['intro_basis'])
  n.update(basis='publisher text',source_url='https://doi.org/example',zh='正文导读')
  enrich.apply_notes(p,{'1':n});self.assertIn('出版社正文',p['intro_basis']);self.assertEqual(p['intro_source'],n['source_url'])
  p['abstract']='New metadata';enrich.apply_notes(p,{'1':n})
  self.assertEqual(p['intro_kind'],'abstract_excerpt');self.assertNotIn('intro_source',p)
 def test_rss_is_not_publication_date(self):
  p={'published':'2026-09-24','date_kind':'announcement','first_seen':'2026-09-24','version_date':'old'}
  dates.apply_dates(p,None);self.assertNotIn('publication_date',p);self.assertNotIn('version_date',p)
  dates.apply_dates(p,{'published':'2025-01-01','source':'arXiv'})
  self.assertEqual(p['publication_date'],'2025-01-01');self.assertEqual(p['first_seen'],'2026-09-24')
 def test_date_metadata(self):
  p=dates.Metadata();p.feed('<meta name="citation_date" content="2025/01/01"/>');self.assertEqual(p.date,'2025-01-01')
if __name__=='__main__':unittest.main()
