"""Regression checks for the daily publication-date intake policy."""
import datetime as dt
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import daily_intake


def paper(identifier, published, score=70, source='journal', version_date=''):
    return {'id': identifier, 'title': identifier, 'source': source,
            'publication_date': published, 'published': published,
            'version_date': version_date, 'updated': version_date,
            'fit_score': score, 'status': 'candidate', 'variants': []}


class DailyIntakeTests(unittest.TestCase):
    def setUp(self):
        self.today = dt.date(2026, 9, 29)

    def test_recent_uses_publication_or_arxiv_version_not_indexing(self):
        old = paper('old-journal', '2026-08-01')
        old['updated'] = '2026-09-29T00:00:00Z'
        self.assertFalse(daily_intake.recent(old, self.today))
        self.assertTrue(daily_intake.recent(paper('new', '2026-09-28'), self.today))
        revised = paper('revised', '2026-08-01', source='arXiv',
                        version_date='2026-09-28T17:30:00Z')
        self.assertTrue(daily_intake.recent(revised, self.today))

    def test_fallback_requires_day_precision_and_last_year(self):
        self.assertTrue(daily_intake.in_fallback_year(paper('one', '2026-05-01'), self.today))
        self.assertFalse(daily_intake.in_fallback_year(paper('month', '2026-05'), self.today))
        self.assertFalse(daily_intake.in_fallback_year(paper('old', '2025-09-01'), self.today))

    def test_recent_new_record_blocks_fallback_search(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'topics.json').write_text('{}')
            with patch.object(daily_intake, 'candidates', return_value=[
                paper('recent', '2026-09-29'), paper('older', '2026-07-01')]), \
                 patch.object(daily_intake, 'search_one_year') as search:
                daily_intake.select(root, self.today)
            intake = json.loads((root / 'intake.json').read_text())
            self.assertEqual(intake['selected'], ['recent'])
            self.assertEqual(intake['mode'], 'recent')
            search.assert_not_called()

    def test_quiet_day_admits_only_high_fit_one_year_papers(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'topics.json').write_text('{}')
            with patch.object(daily_intake, 'candidates', return_value=[
                paper('high', '2026-06-01', 82),
                paper('low', '2026-06-01', 64),
                paper('ancient', '2025-01-01', 90)]):
                daily_intake.select(root, self.today, online=False)
            intake = json.loads((root / 'intake.json').read_text())
            self.assertEqual(intake['selected'], ['high'])
            self.assertEqual(intake['kinds']['high'], 'one_year_fallback')


if __name__ == '__main__':
    unittest.main()
