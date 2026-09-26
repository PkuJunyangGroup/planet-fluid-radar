import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import update

CONFIG=json.loads(Path('topics.json').read_text())
class Rules(unittest.TestCase):

 def test_orbital_dynamics_requires_planet_context(self):
  for title in ['Long-term orbital stability of a resonant planetary system','Mean-motion resonances among exoplanets','Orbital migration of a hot Jupiter']:
   self.assertIn('orbital',update.classify(self.paper(title),CONFIG)['topics'])
  for title in ['Orbital dynamics of a stellar binary','Galactic orbital resonances','Celestial mechanics of a spacecraft']:
   self.assertNotIn('orbital',update.classify(self.paper(title),CONFIG)['topics'])
 def test_incremental_arxiv_window_starts_at_checkpoint(self):
  now=update.dt.datetime.fromisoformat('2026-09-26T01:00:00+00:00')
  previous={'last_success':'2026-09-25T01:17:00+00:00'}
  self.assertEqual(update.checkpoint_since(previous,now,1).isoformat(),previous['last_success'])
  self.assertEqual(update.checkpoint_since({},now,1).isoformat(),'2026-09-25T01:00:00+00:00')

 def test_rss_fallback_keeps_only_recent_records_and_is_nonfatal(self):
  import datetime as dt
  now=dt.datetime.now(dt.timezone.utc)
  fresh={'id':'fresh','version_id':'freshv1','title':'Orbital resonance in a planetary system','abstract':'','authors':['A Author'],'categories':['astro-ph.EP'],'published':now.isoformat(),'updated':(now-dt.timedelta(hours=1)).isoformat(),'url':'https://arxiv.org/abs/fresh','pdf':'https://arxiv.org/pdf/freshv1','source':'arXiv'}
  old={**fresh,'id':'old','version_id':'oldv1','title':'Old planetary orbital stability','updated':(now-dt.timedelta(days=3)).isoformat()}
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);(root/'topics.json').write_text(json.dumps({**CONFIG,'categories':['astro-ph.EP']}))
   (root/'papers.json').write_text(json.dumps({'papers':[],'sources':{}}))
   with patch.object(update,'ROOT',root),patch.object(update,'request_feed',side_effect=RuntimeError('HTTP 503')),patch.object(update,'rss_feed',return_value=[fresh,old]),patch.object(update.time,'sleep'):
    self.assertFalse(update.update(days=1))
   result=json.loads((root/'papers.json').read_text())
   self.assertEqual(result['sources']['astro-ph.EP']['status'],'partial')
   self.assertEqual(result['sources']['astro-ph.EP']['last_rss_fetched'],1)
   self.assertEqual([p['id'] for p in result['papers']],['fresh'])
 def test_cryosphere_primary_and_unrelated_ice(self):
  for title in ['Ice shell convection on Europa','High-pressure ice phase transitions on Ganymede']:
   result=update.classify(self.paper(title),CONFIG)
   self.assertIn('cryosphere',result['topics'])
   self.assertEqual(result['status'],'candidate')
  earth_ice=update.classify(self.paper('Sea ice rheology and basal melting'),CONFIG)
  self.assertEqual(earth_ice['status'],'excluded')
  glacier=update.classify(self.paper('Glacier dynamics and basal sliding'),CONFIG)
  self.assertEqual(glacier['status'],'excluded')
  major={**self.paper('Sea ice rheology and basal melting'),'journal':'Science'}
  self.assertEqual(update.classify(major,CONFIG)['status'],'candidate')
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
 def test_low_priority_earth_topics_need_planetary_context_or_top_journal(self):
  generic=self.paper('Atmospheric Rossby waves and jet streams')
  self.assertEqual(update.classify(generic,CONFIG)['status'],'excluded')
  top={**generic,'journal':'Nature Climate Change'}
  self.assertEqual(update.classify(top,CONFIG)['status'],'candidate')
  planet=self.paper('Atmospheric circulation and Rossby waves on a hot Jupiter')
  self.assertEqual(update.classify(planet,CONFIG)['status'],'candidate')
 def test_single_incidental_planet_mention_does_not_rescue_earth_topic(self):
  p=self.paper('Atmospheric Rossby wave dynamics','We compare one case with conditions around an exoplanet.')
  self.assertEqual(update.classify(p,CONFIG)['status'],'excluded')
  p=self.paper('Atmospheric Rossby waves on a hot Jupiter')
  self.assertEqual(update.classify(p,CONFIG)['status'],'candidate')
 def test_broad_topics_do_not_admit_nonplanetary_papers_outside_top_journals(self):
  paper=self.paper('The Dense MORB Fraction Controls the Dynamic Stability and Hydration Potential of the Mantle Transition Zone', 'Geodynamical modeling examines mantle composition, hydration, density, viscosity and stability.')
  self.assertIn('evolution',update.classify(paper,CONFIG)['topics'])
  self.assertEqual(update.classify(paper,CONFIG)['status'],'excluded')
  paper['journal']='Nature Geoscience'
  self.assertEqual(update.classify(paper,CONFIG)['status'],'candidate')
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
 def test_new_scope_boundaries_keep_planetary_clouds_and_models(self):
  self.assertEqual(update.classify(self.paper('Cloud microphysics and aerosol feedback in Earth’s atmosphere'),CONFIG)['status'],'excluded')
  planet=update.classify(self.paper('Cloud microphysics in the atmosphere of a tidally locked exoplanet'),CONFIG)
  self.assertEqual(planet['status'],'candidate');self.assertIn('physics',planet['topics'])
  model=update.classify(self.paper('A general circulation model of the atmosphere of Mars'),CONFIG)
  self.assertEqual(model['status'],'candidate');self.assertIn('models',model['topics'])
 def test_earth_specific_science_and_regional_studies_are_excluded(self):
  for text in ['CMIP6 projections of global temperature','Plate tectonic reconstruction and regional geology','Earthquake hazard in the Himalaya','Space physics observations of the solar wind','Indian monsoon variability','Arctic Ocean circulation','Alpine regional climatology']:
   self.assertEqual(update.classify(self.paper(text),CONFIG)['status'],'excluded',text)
  global_theory=update.classify(self.paper('A theoretical scaling law for global ocean heat transport'),CONFIG)
  self.assertEqual(global_theory['status'],'excluded')
  nature={**self.paper('A theoretical scaling law for global ocean heat transport'),'journal':'Nature'}
  self.assertEqual(update.classify(nature,CONFIG)['status'],'candidate')
 def test_teacher_authored_papers_are_not_included_and_score_is_explainable(self):
  own=self.paper('Planetary atmospheres and climate',categories=['astro-ph.EP']);own['authors']=['Yang, Jun']
  self.assertEqual(update.classify(own,CONFIG)['status'],'excluded')
  relevant=update.classify(self.paper('Radiative transfer and ocean heat transport in a tidally locked exoplanet'),CONFIG)
  generic=update.classify(self.paper('Numerical methods for generic nonlinear equations'),CONFIG)
  self.assertGreater(relevant['fit_score'],generic['fit_score'])
  self.assertTrue(relevant['fit_matches'])
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
