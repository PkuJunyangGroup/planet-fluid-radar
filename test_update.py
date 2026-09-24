import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import update

CONFIG=json.loads(Path('topics.json').read_text())
class Rules(unittest.TestCase):
 def test_cryosphere_primary_and_unrelated_ice(self):
  for title in ['Ice shell convection on Europa','Sea ice rheology and basal melting','High-pressure ice phase transitions','Glacier dynamics and basal sliding']:
   result=update.classify(self.paper(title),CONFIG)
   self.assertIn('cryosphere',result['topics'])
   self.assertEqual(result['status'],'candidate')
  for title in ['Quantum spin ice dynamics','Water ice in interstellar molecular clouds']:
   self.assertNotIn('cryosphere',update.classify(self.paper(title),CONFIG)['topics'])
 def paper(self,title,abstract='',categories=None):
  return {'id':'test','title':title,'abstract':abstract,'categories':categories or []}
 def test_planetary_chemistry_and_models_are_primary(self):
  for text,topic in [('Photochemical haze formation in the atmosphere of Titan','chemistry'),('A general circulation model for the climate of Mars','models')]:
   result=update.classify(self.paper(text),CONFIG)
   self.assertIn(topic,result['topics'])
   self.assertEqual(result['status'],'candidate')
 def test_planetary_chemistry_and_models_require_relevant_context(self):
  for text in ['Chemical kinetics in a laboratory reactor','Photochemistry in interstellar molecular clouds','A general circulation model of the ocean','Chemical equilibrium in planetary interiors']:
   result=update.classify(self.paper(text),CONFIG)
   self.assertNotIn('chemistry',result['topics'])
   self.assertNotIn('models',result['topics'])
 def test_mechanism_bridge(self):
  self.assertEqual(update.classify(self.paper('Rossby waves in rotating fluid'),CONFIG)['status'],'candidate')
 def test_atmospheric_dynamics_separate_from_climate(self):
  topics=update.classify(self.paper('Atmospheric Rossby waves and jet streams'),CONFIG)['topics']
  self.assertIn('dynamics',topics);self.assertIn('gfd',topics);self.assertNotIn('climate',topics)
 def test_climate_dynamics_separate_from_atmospheric(self):
  topics=update.classify(self.paper('ENSO and coupled climate feedback'),CONFIG)['topics']
  self.assertIn('climate',topics);self.assertNotIn('dynamics',topics)
 def test_geophysical_fluid_separate_from_ocean(self):
  topics=update.classify(self.paper('Quasi-geostrophic rotating stratified flow in a laboratory'),CONFIG)['topics']
  self.assertIn('gfd',topics);self.assertNotIn('ocean',topics)
 def test_physical_ocean_and_shared_waves(self):
  topics=update.classify(self.paper('Ocean heat transport and thermocline changes'),CONFIG)['topics']
  self.assertIn('ocean',topics);self.assertNotIn('gfd',topics)
  topics=update.classify(self.paper('Internal waves and ocean mixing'),CONFIG)['topics']
  self.assertIn('ocean',topics);self.assertIn('gfd',topics)
 def test_ocean_jet_and_atmospheric_overturning_stay_separate(self):
  self.assertNotIn('dynamics',update.classify(self.paper('Ocean jet stream and mesoscale eddies'),CONFIG)['topics'])
  self.assertNotIn('ocean',update.classify(self.paper('Walker overturning circulation with sea surface warming'),CONFIG)['topics'])
 def test_galactic_turbulence_not_geophysical(self):
  self.assertNotIn('gfd',update.classify(self.paper('Inverse cascade in interstellar turbulence'),CONFIG)['topics'])
 def test_stellar_radial_velocity_is_not_planet_detection(self):
  self.assertNotIn('detection',update.classify(self.paper('Radial velocity of hypervelocity stars'),CONFIG)['topics'])
 def test_non_atmospheric_precipitation(self):
  for text in ['Precipitation in the cool circumgalactic medium of galaxies', 'Electron precipitation in atmospheric space physics']:
   self.assertNotIn('physics',update.classify(self.paper(text),CONFIG)['topics'])
  self.assertIn('physics',update.classify(self.paper('Cloud microphysics and precipitation in a changing climate'),CONFIG)['topics'])
 def test_disease_climate_is_outside_scope(self):
  self.assertEqual(update.classify(self.paper('Emerging infectious diseases','Climate and precipitation modify zoonotic risks'),CONFIG)['status'],'excluded')
 def test_orbital_system_is_not_atmospheric(self):
  self.assertNotIn('planetary',update.classify(self.paper('Orbital stability of a sub Neptune planetary system'),CONFIG)['topics'])
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
