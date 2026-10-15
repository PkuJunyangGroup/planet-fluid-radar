import unittest
from build_catalog import author_override_matches
class AuthorIdentity(unittest.TestCase):
 def test_no_name_only_mapping(self):
  self.assertFalse(author_override_matches({'names':['Bo Ma']},{'name':'Bo Ma'},{'id':'p'},lambda x:[x]))
 def test_paper_scope(self):
  item={'names':['Bo Ma'],'paper_ids':['p']}
  self.assertTrue(author_override_matches(item,{'name':'Bo Ma'},{'id':'p'},lambda x:[x]))
  self.assertFalse(author_override_matches(item,{'name':'Bo Ma'},{'id':'q'},lambda x:[x]))
  self.assertFalse(author_override_matches(item,{'name':'B. Ma'},{'id':'p'},lambda x:[x]))
 def test_orcid_conflict_does_not_fall_back(self):
  item={'names':['Bo Ma'],'orcid':'https://orcid.org/0000-0002-6540-7042','paper_ids':['p']}
  self.assertFalse(author_override_matches(item,{'name':'Bo Ma','orcid':'https://orcid.org/0000-0003-2509-6558'},{'id':'p'},lambda x:[x]))
 def test_explicit_orcid_scope(self):
  oid='https://orcid.org/0000-0002-6540-7042'
  item={'names':['Lile Wang'],'orcid':oid}
  self.assertTrue(author_override_matches(item,{'name':'Lile Wang','orcid':oid},{'id':'p'},lambda x:[x]))
  self.assertFalse(author_override_matches(item,{'name':'Another Wang','orcid':oid},{'id':'p'},lambda x:[x]))
 def test_paper_scope_never_creates_identifier(self):
  a={'name':'Y. Kasai','institutions':[],'orcid':None}
  self.assertTrue(author_override_matches({'names':['Y. Kasai'],'paper_ids':['2609.27569']},a,{'id':'2609.27569'},lambda x:[x]))
  self.assertIsNone(a['orcid']);self.assertEqual(a['institutions'],[])
 def test_existing_institution_scope(self):
  item={'names':['Bo Ma'],'institution':'University A'}
  self.assertTrue(author_override_matches(item,{'name':'Bo Ma','institutions':['University A']},{'id':'p'},lambda x:[x]))
  self.assertFalse(author_override_matches(item,{'name':'Bo Ma','institutions':['University B']},{'id':'p'},lambda x:[x]))
if __name__=='__main__':unittest.main()
