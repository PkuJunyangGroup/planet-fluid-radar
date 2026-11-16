import unittest
from update_journals import publication

class JournalDatePrecisionTests(unittest.TestCase):
    def test_same_month_print_does_not_hide_online_day(self):
        self.assertEqual(publication({'published-online': {'date-parts': [[2026,11,15]]}, 'published-print': {'date-parts': [[2026,11]]}, 'published': {'date-parts': [[2026,11]]}}), '2026-11-15')
    def test_earlier_uncertain_month_is_not_fabricated(self):
        self.assertEqual(publication({'published-online': {'date-parts': [[2026,11,15]]}, 'published-print': {'date-parts': [[2026,10]]}}), '2026-10')
    def test_month_only_stays_month_only(self):
        self.assertEqual(publication({'published': {'date-parts': [[2026,11]]}}), '2026-11')

    def test_verified_supplement_preserves_first_seen(self):
        from build_catalog import apply_publisher_supplements
        record={'doi':'10.1029/2026je009903', 'published':'2026-11', 'publication_date':'2026-11', 'first_seen':'2026-11-16T07:57:40.825502+00:00'}
        apply_publisher_supplements([record], {'10.1029/2026je009903': {'publication_date':'2026-11-15', 'source_url':'https://api.crossref.org/works/10.1029/2026je009903'}})
        self.assertEqual(record['publication_date'], '2026-11-15')
        self.assertEqual(record['first_seen'], '2026-11-16T07:57:40.825502+00:00')
