import unittest
import build_catalog as c
import build_network as n
import update_journals as j
class Catalog(unittest.TestCase):
 def paper(self,id,title='Physical mechanisms of clouds in tidally locked planetary atmospheres',authors=None,**kw):
  return {'id':id,'version_id':id,'title':title,'authors':authors or ['A Smith'],'abstract':'An abstract.','source':'arXiv','first_seen':'2026-09-01T00:00:00Z','topics':['planetary'],'tags':[],'status':'candidate',**kw}
 def test_same_doi(self):self.assertEqual(c.match(self.paper('1',doi='https://doi.org/10.1/ABC'),self.paper('2',doi='10.1/abc')),'DOI')
 def test_title_needs_author(self):
  self.assertIsNone(c.match(self.paper('1'),self.paper('2',authors=['B Jones'])))
  self.assertEqual(c.match(self.paper('1'),self.paper('2')),'exact title + author')
 def test_conflicting_dois_do_not_merge(self):self.assertIsNone(c.match(self.paper('1',doi='10.1/a'),self.paper('2',doi='10.1/b')))
 def test_relation_and_variant_dates(self):
  a=self.paper('2609.12345');b=self.paper('doi:10.1/a',title='A different journal title',relations={'has-preprint':[{'id':'https://arxiv.org/abs/2609.12345'}]})
  b['source']='journal';b['first_seen']='2026-09-24T00:00:00Z';b['publication_date']='2026-09-23'
  self.assertEqual(c.match(a,b),'publisher relation');out=c.merge_records([a,b],{});self.assertEqual(len(out),1);self.assertEqual(out[0]['first_seen'],a['first_seen']);self.assertEqual(out[0]['variants'][1]['first_seen'],b['first_seen'])
 def test_partial_dates_and_missing_abstract(self):
  raw={'DOI':'10.1/a','title':['Test'],'published-online':{'date-parts':[[2026,9]]},'author':[{'given':'A','family':'Smith','affiliation':[{'name':'University A'}]}]}
  p=j.parse_record(raw,{'name':'Journal','id':'x','group':'general'},'today');self.assertEqual(p['publication_date'],'2026-09');self.assertTrue(p['metadata_limited']);self.assertEqual(p['author_affiliations'][0]['institutions'],['University A'])
 def test_graph_does_not_treat_address_as_institution(self):
  self.assertEqual(n.identities('Kobe, Japan',[]),[]);self.assertEqual(n.identities('someone@example.com',[]),[])
 def test_graph_aliases_preserve_campuses(self):
  aliases=[{'name':'UC Santa Cruz','match':['university of california, santa cruz']},{'name':'UC Davis','match':['university of california, davis']}]
  self.assertEqual(n.identities('Dept, University of California, Santa Cruz, USA',aliases),['UC Santa Cruz'])
if __name__=='__main__':unittest.main()
