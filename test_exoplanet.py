import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import update_exoplanet as exo

FIXTURE = '''<ul><li class="list-group-item publication" id="publication_33128">
<h5 class="card-title">Transport and Thermochemical Kinetics of Alkali Species in Hot Jupiter Atmospheres</h5>
<p class="card-text"><span><time datetime="2026">publication date: 2026</time></span><br>
<span><time datetime="Sept. 25, 2026">last update: 25/09/2026</time></span><br>
CHRISTIE D., EVANS-SOMA T. & HEBRARD E.<br>MNRAS , in press<br>
<a href="https://doi.org/10.1093/mnras/stag1805">paper</a>
<a href="https://doi.org/10.48550/arXiv.2609.26432">arxiv</a></p></li></ul>'''

class Exoplanet(unittest.TestCase):
    def test_parse_current_bibliography_metadata(self):
        parser = exo.BibliographyParser(); parser.feed(FIXTURE)
        self.assertEqual(len(parser.rows), 1)
        row = parser.rows[0]
        self.assertEqual(row['title'], 'Transport and Thermochemical Kinetics of Alkali Species in Hot Jupiter Atmospheres')
        self.assertIn('last update: 25/09/2026', row['text'])
        self.assertEqual(exo.arxiv_id('https://doi.org/10.48550/arXiv.2609.26432'), '2609.26432')
        record = exo.parse_row(row, '2026-09-26T10:00:00+08:00', json.loads(Path('topics.json').read_text()))
        self.assertEqual(record['doi'], '10.1093/mnras/stag1805')
        self.assertEqual(record['relations']['preprint'][0]['id'], 'https://arxiv.org/abs/2609.26432')
        self.assertEqual(record['journal'], 'MNRAS')
        self.assertEqual(record['authors'][0], 'CHRISTIE D.')
        self.assertIn('chemistry', record['topics'])
        self.assertEqual(record['status'], 'candidate')

    def test_initial_run_scans_only_current_and_previous_beijing_day(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'topics.json').write_text(Path('topics.json').read_text())
            (root / 'exoplanet_records.json').write_text(json.dumps({'papers': [], 'sources': {}}))
            with patch.object(exo, 'ROOT', root), patch.object(exo, 'fetch_page', return_value=[]):
                fixed = exo.dt.datetime(2026, 9, 26, 10, 0, tzinfo=exo.TZ)
                self.assertFalse(exo.update(now=fixed))
            saved = json.loads((root / 'exoplanet_records.json').read_text())
            self.assertEqual(saved['sources']['exoplanet.eu']['coverage_since'], '2026-09-25')
            self.assertEqual(saved['sources']['exoplanet.eu']['status'], 'ok')

    def test_publisher_abstract_supplements_apply_when_feed_fails(self):
        doi = '10.1038/s41550-026-02984-6'
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'topics.json').write_text(Path('topics.json').read_text())
            (root / 'exoplanet_metadata_overrides.json').write_text(json.dumps({doi: {
                'abstract': 'Verified publisher abstract', 'source_url': 'https://publisher.example/article'
            }}))
            record = {'id': 'doi:' + doi, 'doi': doi, 'title': 'A rocky planet paper', 'abstract': '',
                      'first_seen': '2026-09-26T00:00:00+08:00'}
            (root / 'exoplanet_records.json').write_text(json.dumps({'papers': [record], 'sources': {}}))
            with patch.object(exo, 'ROOT', root), patch.object(exo, 'fetch_page', side_effect=RuntimeError('offline')):
                self.assertTrue(exo.update(now=exo.dt.datetime(2026, 9, 26, 10, 0, tzinfo=exo.TZ)))
            saved = json.loads((root / 'exoplanet_records.json').read_text())
            self.assertEqual(saved['sources']['exoplanet.eu']['status'], 'error')
            self.assertEqual(saved['papers'][0]['abstract'], 'Verified publisher abstract')
            self.assertEqual(saved['papers'][0]['abstract_source'], 'https://publisher.example/article')

if __name__ == '__main__': unittest.main()
