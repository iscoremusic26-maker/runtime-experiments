"""Pruebas adversariales del extractor (logs SINTETICOS coherentes; ningun log real en el repo).
Opcional: POSTURE_REAL_A1 / POSTURE_REAL_B1 = rutas a los logs reales de POST04 para revalidar las cifras del cierre."""
import hashlib
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import extract_posture_runtime as X  # noqa: E402

M = '[INFO | dev.posture.post04_numeric_observer] '


def hit(ev, aid, gen, fam='SWORD', at='0x04000002', hp='220>200', lethal=0, kind='HIT_CONFIRMED', life='ACTIVE', mode='4>5', extra=''):
    fin = kind.startswith('FINISH')
    return (M + 'POST03_HIT_EVENT event=%d call=%d id=%d generation=%d life=%s kind=%s branch=%s cc_at_check=UNDETERMINED origin=UNDETERMINED tg=%s dual=0 distinct=0 '
            'collider_src=%s collider=%s sel_class=%s raw_class=%s family=%s native_first=%s basis=NATIVE_BRANCH_ORDER at=%s hp=%s lethal=%d mode=%s old_mode=4 state=0>0 '
            'cd=0>10 cutdown=%d eligible=%s reason=X%s') % (ev, ev * 10, aid, gen, life, kind, 'FINISH' if fin else 'PROCESSED', 'none' if fin else 'cc1', 'none' if fin else 'cc1',
                                                             'NO_SELECTED_COLLIDER' if fin else 'SELECTED_FRESH_MATCH_CC1', 'null' if fin else 'mod8_4',
                                                             'null/null' if fin else 'null/mod8_4', 'UNAVAILABLE' if fin else fam, 'NA' if fin else fam,
                                                             'UNAVAILABLE' if fin else at, hp, lethal, mode, 1 if fin else 0, 'NO' if fin else 'CONFIRMED', extra)


def phit(ev, aid, gen, fam, before, delta, after, action, reason, lethal=0, at='0x04000002', tick=100):
    return M + ('POST04_POSTURE_HIT id=%d generation=%d event=%d family=%s at=%s eligible=CONFIRMED lethal=%d before=%d delta=%d after=%d action=%s reason=%s tick=%d'
                % (aid, gen, ev, fam, at, lethal, before, delta, after, action, reason, tick))


def build(mut=None):
    L = ["[INFO | dev.posture.post04_numeric_observer] found 'Enemy Posture System - POST04' v0.4.0 by Someone (~\\OneDrive\\Documentos\\mods\\X.dusk)",
         '[INFO | dusk::mods::loader] 1/1 mod(s) active',
         M + 'POST03_1_INIT id=x version=0.4.0 source_commit=' + 'ab' * 20 + ' host=2.0.3.0 host_build_id=' + 'cd' * 16 + ' passive=1',
         M + 'POST04_INIT id=x version=0.4.0 source_commit=' + 'ab' * 20 + ' policy_id=P passive=1 writes_to_game=0 game_actions=NONE capacity=64',
         M + 'POST03_TARGET resolve=MOD_OK declared_target_resolved=1 same_address=1 flags=0x09 inline_sites_flag=0 multi_name_flag=1 (inline_sites_flag=1 => NOT_APPROVED)',
         M + 'POST04_POSTURE_BIND id=10 generation=1 initial=0 tick=1 reason=FIRST_OBSERVATION_NOT_SPAWN',
         hit(1, 10, 1), phit(1, 10, 1, 'SWORD', 0, 25, 25, 'APPLY', 'WEIGHTED_HIT'),
         hit(2, 10, 1, fam='SHIELD_ATTACK', at='0x00000010', hp='200>200'), phit(2, 10, 1, 'SHIELD_ATTACK', 25, 0, 25, 'SKIP', 'ZERO_WEIGHT_POLICY', at='0x00000010'),
         M + 'POST04_POSTURE_REGEN id=10 generation=1 from=25 to=20 ticks=30 cause=INTERRUPTED_BY_HIT tick=300',
         hit(3, 10, 1, hp='200>180'), phit(3, 10, 1, 'SWORD', 20, 25, 45, 'APPLY', 'WEIGHTED_HIT', tick=300),
         M + 'POST03_SUMMARY v=0.4.0 tag=PERIODIC calls=100 records_created=1 active=1',
         M + 'POST03_HIT_SUMMARY v=0.4.0 tag=PERIODIC confirmed=3 finish=0 events_emitted=3',
         M + 'POST04_SUMMARY v=0.4.0 tag=PERIODIC ticks=300 reports_new=3 confirmed_consumable=3 weighted=2',
         hit(4, 10, 1, hp='180>0', lethal=1, life='DEATH_SEEN', mode='4>6'), phit(4, 10, 1, 'SWORD', 45, 0, 45, 'SKIP', 'LETHAL', lethal=1),
         hit(5, 11, 2, kind='FINISH_NATIVE_OBSERVED', hp='50>0', lethal=1, life='DEATH_SEEN', mode='6>9'),
         M + 'POST04_POSTURE_RETIRE id=10 generation=1 reason=LOOKUP_ABSENT_VERIFIED final=45 latched=0 dead=1 delete_claim=1 tick=400',
         M + 'POST03_SUMMARY v=0.4.0 tag=SHUTDOWN calls=200 records_created=2 active=1',
         M + 'POST03_HIT_SUMMARY v=0.4.0 tag=SHUTDOWN confirmed=4 finish=1 events_emitted=5',
         M + 'POST03_1_COLLIDER_DIAG v=0.4.0 tag=SHUTDOWN confirmed=4',
         M + 'POST03_CONSERVATION v=0.4.0 tag=SHUTDOWN ok=1 started=5 judged=5 pending=0',
         M + 'POST04_SUMMARY v=0.4.0 tag=SHUTDOWN ticks=500 reports_new=5 dup_consume_calls=0 finish=1 not_confirmed=0 confirmed_consumable=4 weighted=2 '
             'skipped(stale/unbound/dead/lethal/unknown_fam/ambiguous/zero_weight/frozen/latched)=0/0/0/1/0/0/1/0/0 binds=1 retired=1 bound_now=0 crossings=0 '
             'units(added/recovered/closed/live)=50/5/45/0 underflow=0 overflow=0 generation_leak=0 multi_consume=0 ring_dropped=0 log(written/dropped)=9/0',
         M + 'POST04_CONSERVATION v=0.4.0 tag=SHUTDOWN ok=1 e1_consumable=1 e2_reports=1 e3_binds=1 e4_threshold=1 e5_units=1 invariants=1 units_live=0',
         M + 'POST03_SHUTDOWN hook_removal=HOST_DETACH instances_dereferenced=0', '[INFO | dusk::mods::loader] all mods unloaded',
         '[WARNING | dusk] CalcDivideInfo: xDiv var1 out of range: 3']
    if mut:
        L = mut(L)
    return '\n'.join(L) + '\n'


class T(unittest.TestCase):
    def setUp(self):
        self.d = Path(tempfile.mkdtemp())

    def run_on(self, text, expects=None, words=()):
        p = self.d / 'a.log'
        p.write_bytes(text.encode())
        return X.run({'S': p}, self.d / ('o%d' % len(list(self.d.iterdir()))), expects, words=words)

    def viol(self, mut):
        return self.run_on(build(mut))['violations']

    def test_coherent_session_has_no_violations(self):
        s = self.run_on(build())
        self.assertEqual(s['violations'], [])
        d = s['sessions']['S']['derived']
        self.assertEqual((d['hit_confirmed'], d['finish'], d['weighted'], d['units_added'], d['units_recovered_from_regen_lines'], d['units_closed_from_retire_lines']), (4, 1, 2, 50, 5, 45))

    def test_determinism(self):
        p = self.d / 'a.log'
        p.write_bytes(build().encode())
        X.run({'S': p}, self.d / 'k1')
        X.run({'S': p}, self.d / 'k2')
        for f in (self.d / 'k1').iterdir():
            self.assertEqual(f.read_bytes(), (self.d / 'k2' / f.name).read_bytes())

    def test_hash_bytes_lines(self):
        t = build()
        good = hashlib.sha256(t.encode()).hexdigest()
        for e in ({'sha256': '0' * 64}, {'sha256': good, 'bytes': 1}, {'sha256': good, 'splitlines': 1}):
            with self.assertRaises(SystemExit):
                self.run_on(t, {'S': e})

    def test_rejects_out_of_allowlist(self):
        for mut in (lambda L: L + [M + 'POST04_SECRET x=1'],
                    lambda L: [l.replace('reason=WEIGHTED_HIT tick=100', 'reason=WEIGHTED_HIT tick=100 extra=1') for l in L],
                    lambda L: [l.replace('family=SHIELD_ATTACK native_first', 'family=UNKNOWN native_first') for l in L],
                    lambda L: [l.replace('reason=ZERO_WEIGHT_POLICY', 'reason=C:\\Users\\x') for l in L],
                    lambda L: [l.replace('cause=INTERRUPTED_BY_HIT', 'cause=/mnt/c/x') for l in L]):
            with self.assertRaises((ValueError, SystemExit)):
                self.run_on(build(mut))

    def test_privacy(self):
        out = self.run_on(build())
        blob = ''.join(f.read_text() for d in self.d.iterdir() if d.is_dir() for f in d.iterdir())
        for bad in ('OneDrive', 'Someone', 'cdcdcdcd', 'host_build_id', '.dusk'):
            self.assertNotIn(bad, blob)
        self.assertEqual(out['violations'], [])
        for leak in ('SomeAccount', '10.1.2.3', 'DEADBEEFDEADBEEF'):  # rechazo por patron de campo (ValueError) o por el escaner final (SystemExit)
            with self.assertRaises((ValueError, SystemExit)):
                self.run_on(build(lambda L: [l.replace('reason=LETHAL', 'reason=' + leak) for l in L]), words=('SomeAccount',))
        with self.assertRaises(SystemExit):  # el escaner final, por si un campo permitido llevara una palabra prohibida
            X.privacy_check('ok SomeAccount ok', (), ('SomeAccount',))

    def test_truncated_session_fails(self):
        self.assertTrue(self.viol(lambda L: [l for l in L if 'tag=SHUTDOWN' not in l]))
        self.assertTrue(self.viol(lambda L: [l for l in L if 'all mods unloaded' not in l]))

    def test_serial_and_consumption_faults(self):
        self.assertTrue(any('duplicate' in v for v in self.viol(lambda L: L[:8] + [hit(2, 10, 1, fam='SHIELD_ATTACK', at='0x00000010', hp='200>200')] + L[8:])))
        self.assertTrue(any('double consumption' in v for v in self.viol(lambda L: [x for l in L for x in ([l, l] if 'event=3 family=SWORD' in l else [l])])))
        self.assertTrue(any('without POST04_POSTURE_HIT' in v for v in self.viol(lambda L: [l for l in L if 'event=3 family' not in l])))
        self.assertTrue(any('contiguous' in v for v in self.viol(lambda L: [l.replace('event=5 ', 'event=7 ') for l in L])))

    def test_arithmetic_policy_and_markers(self):
        self.assertTrue(self.viol(lambda L: [l.replace('before=20 delta=25 after=45', 'before=20 delta=25 after=46') for l in L]))
        self.assertTrue(self.viol(lambda L: [l.replace('before=0 delta=25 after=25 action=APPLY', 'before=0 delta=30 after=30 action=APPLY') for l in L]))
        self.assertTrue(any('skip reason ZERO_WEIGHT_POLICY, expected LETHAL' in v for v in self.viol(lambda L: [l.replace('action=SKIP reason=LETHAL', 'action=SKIP reason=ZERO_WEIGHT_POLICY') for l in L])))
        two = M + 'POST04_BREAK_READY id=10 generation=1 before=75 after=100 threshold=100 cause=WEIGHTED_HIT game_action=NONE tick=9'
        self.assertTrue(any('more than one BREAK_READY' in v for v in self.viol(lambda L: L + [two, two])))
        self.assertTrue(self.viol(lambda L: [l.replace('from=25 to=20', 'from=25 to=30') for l in L]))
        self.assertTrue(self.viol(lambda L: [l.replace('reason=LOOKUP_ABSENT_VERIFIED', 'reason=CONTEXT_RETIRED') for l in L]))

    def test_false_ok_and_counter_tampering(self):
        self.assertTrue(any('E1 does not hold' in v for v in self.viol(lambda L: [l.replace('confirmed_consumable=4 weighted=2', 'confirmed_consumable=5 weighted=2') for l in L])))  # ok=1 sigue escrito
        self.assertTrue(any('units_closed' in v for v in self.viol(lambda L: [l.replace('units(added/recovered/closed/live)=50/5/45/0', 'units(added/recovered/closed/live)=50/10/40/0') for l in L])))
        self.assertTrue(self.viol(lambda L: [l.replace('overflow=0', 'overflow=1') for l in L]))
        self.assertTrue(self.viol(lambda L: [l.replace('e5_units=1', 'e5_units=0') for l in L]))
        self.assertTrue(self.viol(lambda L: [l.replace('started=5 judged=5', 'started=5 judged=4') for l in L]))
        self.assertTrue(self.viol(lambda L: [l.replace('calls=100', 'calls=900') for l in L]))      # un periodico mayor que el cierre: el contador habria bajado
        self.assertTrue(self.viol(lambda L: [l.replace('inline_sites_flag=0 multi', 'inline_sites_flag=1 multi') for l in L]))
        self.assertTrue(self.viol(lambda L: [l.replace('writes_to_game=0', 'writes_to_game=1') for l in L]))

    @unittest.skipUnless(os.environ.get('POSTURE_REAL_A1') and os.environ.get('POSTURE_REAL_B1'), 'real logs not supplied')
    def test_real_post04_logs(self):
        s = X.run({'A1': os.environ['POSTURE_REAL_A1'], 'B1': os.environ['POSTURE_REAL_B1']}, self.d / 'real',
                  {'A1': {'sha256': '12fa22d0871b9f56661becd307db2e583408fa69a3e649662e8c4357f9c7ef17', 'bytes': 160072, 'splitlines': 1960},
                   'B1': {'sha256': 'd3595694ffe1856124074b66482815a8d5b52778bd8944d6a93c7e4464adb70c', 'bytes': 982863, 'splitlines': 5847}})
        self.assertEqual(s['violations'], [])
        a = s['aggregate']
        self.assertEqual((a['events'], a['hit_confirmed'], a['finish'], a['weighted'], a['crossings'], a['units_recovered_from_regen_lines']), (27, 24, 3, 12, 2, 7))


if __name__ == '__main__':
    unittest.main()
