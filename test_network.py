import json
import re
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import build_network
import enrich
from author_names import chinese_name
from institution_utils import parents,verified_units,verified_hierarchy,orcid_url

class NetworkRules(unittest.TestCase):
 def test_names_require_explicit_unambiguous_hanzi(self):
  self.assertIsNone(chinese_name({'name':{'given-names':{'value':'Minghuai'},'family-name':{'value':'Wang'}}}))
  self.assertEqual(chinese_name({'other-names':{'other-name':[{'content':'汪名怀'}]}}),'汪名怀')
  self.assertIsNone(chinese_name({'other-names':{'other-name':[{'content':'汪名怀'},{'content':'王明怀'}]}}))
 def test_chinese_family_name_precedes_given_name(self):
  self.assertEqual(chinese_name({'name':{'given-names':{'value':'名怀'},'family-name':{'value':'汪'}}}),'汪名怀')
 def test_longer_university_name_does_not_become_academy(self):
  aliases=[{'name':'CAS','match':['Chinese Academy of Sciences']},{'name':'UCAS','match':['University of Chinese Academy of Sciences']}]
  self.assertEqual(parents('College of Earth Sciences University of Chinese Academy of Sciences Beijing China',aliases),['UCAS'])
  self.assertEqual(parents('100871 Beijing postcode=100871',aliases),[])
 def test_short_ambiguous_name_requires_location(self):
  a=[{'name':'Western University (Canada)','match':['Western University'],'context':['Ontario']}]
  self.assertEqual(parents('Western University Phnom Penh',a),[])
  self.assertEqual(parents('Western University Ontario Canada',a),['Western University (Canada)'])
 def test_orcid_checksum_and_author_locality(self):
  url='https://orcid.org/0000-0002-1825-0097'
  self.assertEqual(orcid_url(url),url)
  self.assertIsNone(orcid_url('0000-0002-1825-0098'))
  self.assertIsNone(orcid_url('https://evil.test/0000-0002-1825-0097'))
  _,authors=enrich.affiliations('<div class="ltx_role_author"><span class="ltx_personname">A</span><a href="'+url+'">ORCID</a></div><div class="ltx_role_author"><span class="ltx_personname">B</span></div>')
  self.assertEqual(authors[0]['orcid'],url);self.assertIsNone(authors[1]['orcid'])
 def test_nested_institute_name_is_not_another_unit(self):
  units={'CAS':[{'name':n,'_patterns':[re.compile(re.escape(n.lower()))]} for n in ['Institute of Geochemistry','Guangzhou Institute of Geochemistry']]}
  self.assertEqual([u['name'] for u in verified_units('Guangzhou Institute of Geochemistry Chinese Academy of Sciences','CAS',units)],['Guangzhou Institute of Geochemistry'])
 def test_same_parent_has_one_paper_and_no_internal_edge(self):
  aliases=[{'name':'Example University','match':['Example University']}]
  units={'Example University':[{'name':n,'source':'https://example.edu/','_patterns':[re.compile(n.lower())]} for n in ['Department of Physics','Department of Chemistry']]}
  raw=['Department of Physics Example University','Department of Chemistry Example University']
  paper={'id':'p','status':'candidate','institutions':raw,'author_affiliations':[{'name':'Author','institutions':raw,'orcid':'0000-0002-1825-0097'}]}
  with tempfile.TemporaryDirectory() as d,patch.object(build_network,'ROOT',Path(d)),patch.object(build_network,'verified_hierarchy',return_value=(aliases,units,{'Example University':{}})):
   result=build_network.build({'generated_at':'test','papers':[paper]})
  self.assertEqual(len(result['nodes']),1);self.assertEqual(result['edges'],[])
  n=result['nodes'][0];self.assertEqual(n['papers'],['p']);self.assertEqual(len(n['units']),2)
  self.assertEqual(n['authors'][0]['papers'],['p']);self.assertEqual(len(n['authors'][0]['unit_papers']),2)
if __name__=='__main__':unittest.main()
