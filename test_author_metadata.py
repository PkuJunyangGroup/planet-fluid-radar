"""Regressions for arXiv RSS bylines and experimental HTML conversion defects."""
import unittest
import enrich
import update

class AuthorMetadata(unittest.TestCase):
 def test_official_arxiv_byline_fixtures(self):
  import json
  from pathlib import Path
  fixtures=json.loads((Path(__file__).parent/'tests/fixtures/arxiv_author_bylines.json').read_text())
  self.assertEqual([len(x['expected']) for x in fixtures],[33,5,3])
  for fixture in fixtures:
   with self.subTest(source=fixture['source']):self.assertEqual(enrich.byline(fixture['html']),fixture['expected'])
 def test_author_links_preserve_commas_accents_hyphens_and_initials(self):
  html='<div class="authors"><span>Authors:</span><a>Doe, Jane</a>, <a>Éric Hébrard</a>, <a>K. Vida</a>, <a>Shang-Min Tsai</a></div><a>Not an author</a>'
  self.assertEqual(enrich.byline(html),['Doe, Jane','Éric Hébrard','K. Vida','Shang-Min Tsai'])
 def test_rss_creator_is_not_a_person(self):
  xml='''<feed xmlns="http://www.w3.org/2005/Atom" xmlns:dc="http://purl.org/dc/elements/1.1/"><entry><id>oai:arXiv.org:2609.28001v1</id><title>Title</title><dc:creator>K. Vida, B. Seli, B. Edwards</dc:creator></entry></feed>'''
  paper=update.parse_rss(xml)[0]
  self.assertEqual(paper['authors'],[])
  self.assertEqual(paper['authors_raw'],'K. Vida, B. Seli, B. Edwards')
 def test_affiliation_markup_is_not_a_person(self):
  html='<span class="ltx_role_author"><span class="ltx_personname">K. Vida</span></span><span class="ltx_role_author"><span class="ltx_personname">1,2 B. Seli1,2 B. Edwards3,4 1Konkoly Observatory</span></span>'
  self.assertEqual(enrich.affiliations(html,['K. Vida','B. Seli','B. Edwards'])[1],[])
 def test_grouped_names_do_not_inherit_union_of_institutions(self):
  html='<span class="ltx_role_author"><span class="ltx_personname">Patryk Sofia Lykawka Timothy R. Holt Brad Carter</span><span class="ltx_role_affiliation">Kindai University</span></span>'
  orgs,authors=enrich.affiliations(html,['Patryk Sofia Lykawka','Timothy R. Holt','Brad Carter'])
  self.assertEqual(orgs,['Kindai University']);self.assertEqual(authors,[])
 def test_tex_conversion_contamination_is_rejected(self):
  authors=[{'name':r'\newauthorOlivia Venot','institutions':[]},{'name':'France','institutions':[]}]
  self.assertEqual(enrich.reconcile_affiliations(authors,['Olivia Venot']),[])
 def test_valid_associations_and_initial_variants_are_preserved(self):
  authors=[{'name':'J. Smith','institutions':['Institute A'],'orcid':None},{'name':'Éric Hébrard','institutions':['Institute B'],'orcid':None}]
  self.assertEqual(enrich.reconcile_affiliations(authors,['John Smith','Éric Hébrard']),authors)
 def test_explicit_numeric_collaboration_name_preserved(self):
  authors=[{'name':'3D Collaboration','institutions':[]}]
  self.assertEqual(enrich.reconcile_affiliations(authors,['3D Collaboration']),authors)

if __name__=='__main__':unittest.main()

class AuthorMetadataCache(unittest.TestCase):
 def test_offline_recovery_preserves_provenance(self):
  import tempfile,json
  from pathlib import Path
  from unittest.mock import patch
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp)
   paper={'id':'2609.28001','version_id':'2609.28001v1','title':'Title','abstract':'','authors':['K. Vida, B. Seli, B. Edwards'],'first_seen':'original','doi':'10.example/original'}
   cache={'2609.28001v1':{'institutions':['Institute'],'author_affiliations':[{'name':'1,2 B. Seli1,2','institutions':['Institute']}],'status':'verified','source_url':'https://arxiv.org/html/2609.28001v1','checked_at':'2026-09-24T00:00:00+00:00','byline_authors':['K. Vida','B. Seli','B. Edwards'],'byline_source':'https://arxiv.org/abs/2609.28001v1'}}
   (root/'papers.json').write_text(json.dumps({'papers':[paper]}));(root/'affiliations.json').write_text(json.dumps(cache))
   with patch.object(enrich,'ROOT',root):enrich.enrich(fetch=False)
   result=json.loads((root/'papers.json').read_text())['papers'][0]
   self.assertEqual(result['authors'],['K. Vida','B. Seli','B. Edwards'])
   self.assertEqual(result['author_affiliations'],[])
   self.assertEqual(result['institutions'],['Institute'])
   self.assertEqual(result['first_seen'],'original');self.assertEqual(result['doi'],'10.example/original')
   saved=json.loads((root/'affiliations.json').read_text())['2609.28001v1']
   self.assertEqual(saved['rejected_author_affiliations'],cache['2609.28001v1']['author_affiliations'])
   self.assertEqual(saved['author_affiliation_status'],'unavailable')
