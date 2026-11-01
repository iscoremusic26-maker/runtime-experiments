"""Pruebas del extractor A1/B1 con logs SINTETICOS (ningun log real en el repo). Opcional: POST031_REAL_LOG_A1 / POST031_REAL_LOG_B1 validan los logs reales."""
import hashlib
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import extract_runtime_evidence_a1_b1 as X  # noqa: E402

TAG = '[INFO | dev.posture.post03_1_collider_classification] '


def hit(n, call, aid, gen, kind='HIT_CONFIRMED', fam='SWORD', sel='mod8_4', raw='null/mod8_4', tg='cc1', at='0x04000002', hp='220>200', reason='COOLDOWN_SET_AND_REACTION_COMMITTED', extra=''):
    fin = kind == 'FINISH_NATIVE_OBSERVED'
    return (TAG + 'POST03_HIT_EVENT event=%d call=%d id=%d generation=%d life=ACTIVE kind=%s branch=%s cc_at_check=UNDETERMINED origin=UNDETERMINED tg=%s dual=0 distinct=0 '
            'collider_src=%s collider=%s sel_class=%s raw_class=%s family=%s native_first=%s basis=NATIVE_BRANCH_ORDER at=%s hp=%s lethal=%d mode=3>5 old_mode=3 state=3>0 cd=0>10 '
            'cutdown=%d eligible=%s reason=%s%s' % (n, call, aid, gen, kind, 'FINISH' if fin else 'PROCESSED', 'none' if fin else tg, 'none' if fin else 'cc1',
                                                    'NO_SELECTED_COLLIDER' if fin else 'SELECTED_FRESH_MATCH_CC1', 'null' if fin else sel, 'null/null' if fin else raw,
                                                    'UNAVAILABLE' if fin else fam, 'NA' if fin else fam, 'UNAVAILABLE' if fin else at, hp, 1 if fin else 0, 1 if fin else 0,
                                                    'NO' if fin else 'CONFIRMED', reason, extra))


def synth(events=None, mutate=None, summary=None, drop_summary=False, extra_lines=()):
    events = events if events is not None else [hit(1, 100, 161, 8), hit(2, 200, 161, 8, fam='IRON_BALL', hp='200>80'), hit(3, 300, 161, 8, kind='FINISH_NATIVE_OBSERVED', hp='20>0')]
    L = ['  Backend: D3D12', "[INFO | com.blueflaregames.zora_swim] found 'Zora Swim' v1.3.0",
         "[INFO | dev.posture.post03_1_collider_classification] found 'Enemy Posture System - POST03.1' v0.3.1 by Someone (~\\OneDrive\\Documentos\\Juegos\\mods\\X.dusk)",
         '[INFO | dusk::mods::loader] 2/2 mod(s) active',
         TAG + 'POST03_1_INIT id=x version=0.3.1 source_commit=' + 'ab' * 20 + ' host=2.0.3.0 host_build_id=' + 'cd' * 16 + ' passive=1 pmf_bytes=8 capacity=64 log_cap=2000 deref_gate=eq_raw_hit_obj+align4 sizeof_cCcD_Obj=136',
         TAG + 'POST03_TARGET resolve=MOD_OK declared_target_resolved=1 same_address=1 flags=0x09 inline_sites_flag=0 multi_name_flag=1 (inline_sites_flag=1 => NOT_APPROVED)',
         TAG + 'POST03_HOOK_INSTALLED target=daE_OC_c::damage_check post=MOD_OK pre=MOD_OK pre_returns=HOOK_CONTINUE_ALWAYS',
         '[INFO | dusk] fpcBs_Create: pid=105 profname=fpcNm_ALINK_e',
         TAG + 'POST03_INSTANCE_FIRST_SEEN call=1 id=161 generation=8 epoch=3 adm=E_OC_CANDIDATE reason=FIRST_HOOK_CALL origin=UNDETERMINED (not SPAWN_CONFIRMED)']
    L += list(extra_lines) + events
    L += [TAG + 'POST03_INSTANCE_DEATH_SEEN call=300 id=161 generation=8 evidence=HP_OR_NATIVE_MODE (NO_DELETE_CLAIM)',
          TAG + 'POST03_INSTANCE_RETIRED call=400 id=161 generation=8 reason=LOOKUP_ABSENT_VERIFIED delete_claim=1 context_changed=0 epoch=3']
    conf = [e for e in events if 'kind=HIT_CONFIRMED' in e]
    sw = sum('family=SWORD' in e for e in conf)
    iron = sum('family=IRON_BALL' in e for e in conf)
    fin = len(events) - len(conf)
    s = dict(confirmed=len(conf), finish=fin, events=len(events), sword=sw, iron=iron, other=len(conf) - sw - iron, m4=len(conf), started=len(events), fstarted=fin, cstarted=len(conf))
    if summary:
        s.update(summary)
    if not drop_summary:
        L += [TAG + 'POST03_SUMMARY v=0.3.1 tag=SHUTDOWN calls=500 adm(cand/e_oc2/other/unsafe)=5/0/0/0 records_created=1 active=0 death_seen=1 absent_verified=1 admission_changes=0 pending=0',
              TAG + 'POST03_HIT_SUMMARY v=0.3.1 tag=SHUTDOWN pre(finish/cooldown/no_tg/tg/unknown)=1/0/0/2/0 cand_started=%(cstarted)d raw_tg=%(cstarted)d dual_tg=0 pair_distinct=0 confirmed=%(confirmed)d '
              'finish_started=%(fstarted)d finish=%(finish)d collider_unmatched=0 classification_unavailable=0 family(sword/shield/arrow/bomb/iron/boomerang/at40/sling/other/ambiguous/unavail)='
              '%(sword)d/0/0/0/%(iron)d/0/0/0/%(other)d/0/0 lethal=%(finish)d hp_changed=%(events)d anomalies=0 events_emitted=%(events)d' % s,
              TAG + 'POST03_1_COLLIDER_DIAG v=0.3.1 tag=SHUTDOWN confirmed=%(confirmed)d reason(no_selected/too_low/alignment/raw_null/not_equal_raw/match_cc0/match_cc1)=0/0/0/0/0/0/%(confirmed)d '
              'sel_class(null/too_low/mod8_0/mod8_4/mod4_bad)=0/0/0/%(m4)d/0 raw_cc0_class=0/0/0/0/0 raw_cc1_class=0/0/0/0/0 deref_ok_mod8_0=0 deref_ok_mod8_4=%(m4)d classification_unavailable=0' % s,
              TAG + 'POST03_CONSERVATION v=0.3.1 tag=SHUTDOWN ok=1 started=%(started)d judged=%(started)d pending=0' % s]
    L += [TAG + 'POST03_SHUTDOWN hook_removal=HOST_DETACH instances_dereferenced=0', '[INFO | dusk::mods::loader] all mods unloaded',
          '[WARNING | dusk] CalcDivideInfo: xDiv var1 out of range: 3', '[WARNING | aurora::texture] texture_replacement: missing']
    if mutate:
        L = mutate(L)
    return '\n'.join(L) + '\n'


class T(unittest.TestCase):
    def setUp(self):
        self.d = Path(tempfile.mkdtemp())

    def write(self, name, text):
        p = self.d / name
        p.write_bytes(text.encode('utf-8'))
        return p

    def run_x(self, a, b, out='o', expects=None):
        return X.run({'A1': a, 'B1': b}, self.d / out, expects)

    def test_counters_and_zero_discrepancies(self):
        a = self.write('a.log', synth())
        b = self.write('b.log', synth())
        s = self.run_x(a, b)
        agg = s['aggregate']
        self.assertEqual((agg['events'], agg['hit_confirmed'], agg['finish_native'], agg['discrepancies']), (6, 4, 2, 0))
        self.assertEqual((agg['family']['sword'], agg['family']['iron'], agg['sel_class']['mod8_4']), (2, 2, 4))
        self.assertEqual(s['sessions']['A1']['hook_target']['inline_sites_flag'], '0')  # leyenda final no cuenta
        self.assertTrue(s['sessions']['A1']['shutdown_precedes_unload'])

    def test_determinism_byte_identical(self):
        a = self.write('a.log', synth())
        b = self.write('b.log', synth())
        self.run_x(a, b, 'o1')
        self.run_x(a, b, 'o2')
        for f in (self.d / 'o1').iterdir():
            self.assertEqual(f.read_bytes(), (self.d / 'o2' / f.name).read_bytes())

    def test_privacy_nothing_leaks(self):
        a = self.write('a.log', synth())
        self.run_x(a, a)
        blob = ''.join(f.read_text() for f in (self.d / 'o').iterdir())
        for bad in ('OneDrive', 'Documentos', '.dusk"', 'cdcdcdcd', 'host_build_id', 'Someone'):
            self.assertNotIn(bad, blob)

    def test_wrong_hash_bytes_lines_rejected(self):
        a = self.write('a.log', synth())
        good = hashlib.sha256(a.read_bytes()).hexdigest()
        with self.assertRaises(SystemExit):
            self.run_x(a, a, 'x1', {'A1': {'sha256': '0' * 64}})
        with self.assertRaises(SystemExit):
            self.run_x(a, a, 'x2', {'A1': {'sha256': good, 'bytes': 1}})
        with self.assertRaises(SystemExit):
            self.run_x(a, a, 'x3', {'A1': {'sha256': good, 'splitlines': 1}})
        self.run_x(a, a, 'x4', {'A1': {'sha256': good, 'bytes': a.stat().st_size, 'splitlines': len(a.read_text().splitlines())}})

    def test_out_of_allowlist_events_rejected(self):
        for bad in (hit(1, 1, 161, 8, fam='SECRET_FAMILY'), hit(1, 1, 161, 8, kind='SOMETHING_ELSE'), hit(1, 1, 161, 8, extra=' foo=bar'),
                    hit(1, 1, 161, 8, reason='C:\\Users\\x'), hit(1, 1, 161, 8, reason='path/to/file'), hit(1, 1, 161, 8, at='0x0000000012345678'),
                    hit(1, 1, 161, 8, raw='mod8_0'), hit(1, 1, 161, 8, reason='{"a":1}')):
            a = self.write('a.log', synth([bad]))
            with self.assertRaises((ValueError, SystemExit)):
                self.run_x(a, a)

    def test_unknown_post03_tag_rejected(self):
        a = self.write('a.log', synth(extra_lines=[TAG + 'POST03_NEW_THING secret=1']))
        with self.assertRaises(ValueError):
            self.run_x(a, a)

    def test_privacy_scan_catches_ip_hex_username_in_allowed_shape(self):
        for leak in ('10.0.0.1', 'deadbeefdeadbeef', 'SomeAccount'):
            a = self.write('a.log', synth([hit(1, 1, 161, 8, reason=leak)], ))
            with self.assertRaises(SystemExit):
                X.run({'A1': a, 'B1': a}, self.d / 'o', None, forbidden_words=('SomeAccount',))

    def test_incomplete_input_flags_discrepancies(self):
        a = self.write('a.log', synth(drop_summary=True))
        s = self.run_x(a, a)
        self.assertGreater(s['aggregate']['discrepancies'], 0)
        b = self.write('b.log', synth(summary={'confirmed': 99}))
        s2 = self.run_x(b, b, 'o3')
        self.assertTrue(any(d['name'] == 'confirmed' for d in s2['sessions']['A1']['derived']['discrepancies']))

    def test_truncated_log_without_shutdown(self):
        txt = synth(mutate=lambda L: [l for l in L if 'POST03_SHUTDOWN' not in l])
        a = self.write('a.log', txt)
        s = self.run_x(a, a)
        self.assertNotIn('post03_shutdown', s['sessions']['A1'])

    def test_actor_reconstruction(self):
        a = self.write('a.log', synth())
        s = self.run_x(a, a)
        ac = s['sessions']['A1']['actors'][0]
        self.assertEqual((ac['id'], ac['generation'], ac['events'], ac['delete_claim']), (161, 8, [1, 2, 3], 1))

    @unittest.skipUnless(os.environ.get('POST031_REAL_LOG_A1') and os.environ.get('POST031_REAL_LOG_B1'), 'logs reales no suministrados')
    def test_real_logs(self):
        s = X.run({'A1': os.environ['POST031_REAL_LOG_A1'], 'B1': os.environ['POST031_REAL_LOG_B1']}, self.d / 'real',
                  {'A1': {'sha256': 'b8424dbda469c18c88358047ec92369ad6faaf845d2acbee66a31ac61d031b55', 'bytes': 332709, 'splitlines': 4200},
                   'B1': {'sha256': '427ef9f66da5ba054a652413382b8b8cc0c2cc46e8fb6fb3b00541878118372f', 'bytes': 890364, 'splitlines': 7007}})
        a = s['aggregate']
        self.assertEqual((a['events'], a['hit_confirmed'], a['finish_native'], a['discrepancies']), (36, 33, 3, 0))
        self.assertEqual((a['family']['sword'], a['family']['iron'], a['family']['boomerang'], a['family']['other'], a['family']['unavail']), (23, 4, 1, 5, 0))
        self.assertEqual(a['sel_class']['mod8_4'], 21)


if __name__ == '__main__':
    unittest.main()
