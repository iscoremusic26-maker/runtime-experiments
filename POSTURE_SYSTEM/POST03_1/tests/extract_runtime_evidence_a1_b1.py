"""POST03.1: extractor DETERMINISTA y SANEADO de la evidencia humana A1/B1 (sesiones reales de POST03.1 0.3.1).

Lee dos logs crudos (que NUNCA se versionan) y emite SOLO campos de una lista blanca:
  * eventos POST03_HIT_EVENT (36 esperados: 33 HIT_CONFIRMED + 3 FINISH_NATIVE_OBSERVED),
  * ciclo de vida por (id, generation), contadores SHUTDOWN de POST03/POST03_1_COLLIDER_DIAG,
  * versiones de mods, agregados de HM/Bars/DEVF/Expansion solo donde aparecen, e incidencias con criterio exacto.
No copia lineas completas, rutas, nombres de usuario, direcciones ni ids de build. Una linea POST03_* fuera de la lista blanca ABORTA.
Salida identica byte a byte para las mismas entradas (sin marcas de tiempo, claves ordenadas).
Uso: extract_runtime_evidence_a1_b1.py --log-a A1.log --log-b B1.log --output-dir DIR [--expect-sha-a H --expect-sha-b H ...]"""
import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path

SCHEMA_VERSION = 1
MODULE_TAG = 'dev.posture.post03_1_collider_classification'
TOKEN = r'[A-Za-z0-9_+>.\-/]+'  # sin '\\', ':' ni espacios; el '/' solo se admite en raw_class y se valida campo a campo (ver FIELD_PATTERNS)
HIT_FIELDS = ['event', 'call', 'id', 'generation', 'life', 'kind', 'branch', 'cc_at_check', 'origin', 'tg', 'dual', 'distinct', 'collider_src',
              'collider', 'sel_class', 'raw_class', 'family', 'native_first', 'basis', 'at', 'hp', 'lethal', 'mode', 'old_mode', 'state', 'cd',
              'cutdown', 'eligible', 'reason']
HIT_RE = re.compile(r'POST03_HIT_EVENT ((?:\w+=' + TOKEN + r'(?: |$))+)$')
FIELD_RE = re.compile(r'(\w+)=(' + TOKEN + r')')
KV_NUM = re.compile(r'(\w+)=(\d+)')
KNOWN_TAGS = ('POST03_1_INIT', 'POST03_TARGET', 'POST03_HOOK_INSTALLED', 'POST03_INSTANCE_FIRST_SEEN', 'POST03_INSTANCE_DEATH_SEEN',
              'POST03_INSTANCE_RETIRED', 'POST03_ADMISSION_CHANGED', 'POST03_HIT_EVENT', 'POST03_SUMMARY', 'POST03_HIT_SUMMARY',
              'POST03_1_COLLIDER_DIAG', 'POST03_CONSERVATION', 'POST03_SHUTDOWN')
TAG_RE = re.compile(r'\] (POST03\w*)\b')
FAMILIES = ['sword', 'shield', 'arrow', 'bomb', 'iron', 'boomerang', 'at40', 'sling', 'other', 'ambiguous', 'unavail']
FAMILY_NAME = {'SWORD': 'sword', 'SHIELD_ATTACK': 'shield', 'ARROW': 'arrow', 'BOMB': 'bomb', 'IRON_BALL': 'iron', 'BOOMERANG': 'boomerang',
               'AT_TYPE_40': 'at40', 'SLINGSHOT': 'sling', 'OTHER_VERIFIED': 'other', 'AMBIGUOUS': 'ambiguous', 'UNAVAILABLE': 'unavail'}
SEL_CLASSES = ['null', 'too_low', 'mod8_0', 'mod8_4', 'mod4_bad']
REASONS = ['no_selected', 'too_low', 'alignment', 'raw_null', 'not_equal_raw', 'match_cc0', 'match_cc1']
LINK_RE = re.compile(r'fpcBs_Create: pid=(\d+) profname=fpcNm_ALINK_e')
MOD_RE = re.compile(r"\[INFO \| ([\w.]+)\] found '([^']{1,80})' v([\w.\-]{1,40})(?: by |$)")
PRIVACY = [re.compile(p) for p in (r'[A-Za-z]:\\', r'\\Users\\', r'OneDrive', r'AppData', r'Documentos', r'/mnt/', r'/home/', r'~\\',
                                   r'\b[0-9a-fA-F]{12,}\b', r'\b\d{1,3}(?:\.\d{1,3}){3}\b', r'0x[0-9a-fA-F]{9,}', r'\.dusk\b')]
TSV_COLS = ['session', 'ord', 'event', 'call', 'id', 'generation', 'link_pid', 'epoch_first_seen', 'actor_hit_ord', 'life', 'kind', 'branch', 'tg', 'dual',
            'distinct', 'collider_src', 'collider', 'sel_class', 'raw_class', 'family', 'native_first', 'basis', 'at', 'hp_pre', 'hp_post', 'hp_delta',
            'lethal', 'mode_pre', 'mode_post', 'old_mode', 'state_pre', 'state_post', 'cd_pre', 'cd_post', 'cutdown', 'eligible', 'reason']
SCHEMA = {
    'schema_version': SCHEMA_VERSION,
    'tsv_columns': TSV_COLS,
    'notes': {
        'link_pid': 'pid de la instancia de Link (daAlink_c) vigente cuando se emitio el evento; cambia en cada carga de stage',
        'epoch_first_seen': 'epoch de stage del observador cuando se vio por primera vez (id, generation); NO es spawn nativo',
        'actor_hit_ord': 'orden 1-based del evento dentro de su (id, generation), contando HIT_CONFIRMED y FINISH',
        'hp_delta': 'hp_pre - hp_post (puede ser 0 con HIT_CONFIRMED: no equivale a perdida de vida)',
        'sel_class/raw_class': 'solo clases de residuo del puntero (null/too_low/mod8_0/mod8_4/mod4_bad); nunca direcciones',
        'at': 'mascara cruda de tipo AT leida (8 digitos hex) o UNAVAILABLE',
    },
}


def sha(b):
    return hashlib.sha256(b).hexdigest()


CLS = '(?:null|too_low|mod8_0|mod8_4|mod4_bad)'
FIELD_PATTERNS = {'raw_class': re.compile('^' + CLS + '/' + CLS + '$'), 'sel_class': re.compile('^' + CLS + '$'), 'at': re.compile(r'^(?:0x[0-9a-f]{8}|UNAVAILABLE)$')}
PLAIN = re.compile(r'^[A-Za-z0-9_+>.\-]+$')  # cualquier otro campo: sin '/' ni ':'


def parse_hit(line):
    m = HIT_RE.search(line)
    if not m:
        return None
    d = dict(FIELD_RE.findall(m.group(1)))
    if set(d) != set(HIT_FIELDS):
        raise ValueError('unexpected POST03_HIT_EVENT fields: %s' % sorted(set(d) ^ set(HIT_FIELDS)))
    for k, v in d.items():
        if not (FIELD_PATTERNS[k] if k in FIELD_PATTERNS else PLAIN).match(v):
            raise ValueError('POST03_HIT_EVENT field %s has a value outside its allowlist pattern' % k)
    row = {k: d[k] for k in HIT_FIELDS if k not in ('hp', 'mode', 'state', 'cd')}
    for k in ('hp', 'mode', 'state', 'cd'):
        a, b = d[k].split('>')
        row[k + '_pre'], row[k + '_post'] = int(a), int(b)
    for k in ('event', 'call', 'id', 'generation', 'dual', 'distinct', 'lethal', 'old_mode', 'cutdown'):
        row[k] = int(row[k])
    if row['family'] not in FAMILY_NAME or row['kind'] not in ('HIT_CONFIRMED', 'FINISH_NATIVE_OBSERVED'):
        raise ValueError('event outside allowlist: family=%s kind=%s' % (row['family'], row['kind']))
    return row


def group(body, name, labels):
    m = re.search(re.escape(name) + r'\(' + re.escape(labels) + r'\)=(\d+(?:/\d+)*)', body)
    return [int(x) for x in m.group(1).split('/')] if m else None


def parse_log(path, expect):
    raw = Path(path).read_bytes()
    digest = sha(raw)
    text = raw.decode('utf-8', errors='replace')
    lines = text.splitlines()
    for key, val in (('sha256', digest), ('bytes', len(raw)), ('splitlines', len(lines))):
        if expect.get(key) is not None and expect[key] != val:
            raise SystemExit('%s mismatch for %s: %s' % (key, Path(path).name, val))
    out = {'file_name': Path(path).name, 'sha256': digest, 'bytes': len(raw), 'splitlines': len(lines), 'events': [], 'mods': [], 'lifecycle': {}}
    out['life_lines'] = {'first_seen': [], 'death_seen': [], 'retired': [], 'admission_changed': []}
    pids, link_pid, epoch_of = [], 0, {}
    cdi = tex = perf = perf_flag = devf_rm = devf_acc = 0
    first_post_line = shutdown_line = unloaded_line = None
    other_module_lines = 0
    for n, l in enumerate(lines, 1):
        m = LINK_RE.search(l)
        if m:
            link_pid = int(m.group(1))
            pids.append(link_pid)
        mt = TAG_RE.search(l)
        if mt and MODULE_TAG in l:
            tag = mt.group(1)
            if tag not in KNOWN_TAGS:
                raise ValueError('POST03 tag outside allowlist (line %d): %s' % (n, tag))
            first_post_line = first_post_line or n
            body = l.split(tag, 1)[1]
            if tag == 'POST03_HIT_EVENT':
                row = parse_hit(l)
                if row is None:
                    raise ValueError('POST03_HIT_EVENT line rejected by allowlist (line %d)' % n)
                row['link_pid'] = link_pid
                row['epoch_first_seen'] = epoch_of.get((row['id'], row['generation']))
                out['events'].append(row)
            elif tag == 'POST03_INSTANCE_FIRST_SEEN':
                kv = dict(FIELD_RE.findall(body))
                key = (int(kv['id']), int(kv['generation']))
                epoch_of[key] = int(kv['epoch'])
                out['life_lines']['first_seen'].append({'call': int(kv['call']), 'id': key[0], 'generation': key[1], 'epoch': int(kv['epoch']),
                                                        'adm': kv['adm'], 'reason': kv['reason']})
            elif tag == 'POST03_INSTANCE_DEATH_SEEN':
                kv = dict(FIELD_RE.findall(body))
                out['life_lines']['death_seen'].append({'call': int(kv['call']), 'id': int(kv['id']), 'generation': int(kv['generation']), 'evidence': kv['evidence']})
            elif tag == 'POST03_INSTANCE_RETIRED':
                kv = dict(FIELD_RE.findall(body))
                out['life_lines']['retired'].append({'call': int(kv['call']), 'id': int(kv['id']), 'generation': int(kv['generation']), 'reason': kv['reason'],
                                                     'delete_claim': int(kv['delete_claim']), 'context_changed': int(kv['context_changed']), 'epoch': int(kv['epoch'])})
            elif tag == 'POST03_ADMISSION_CHANGED':
                kv = dict(FIELD_RE.findall(body))
                out['life_lines']['admission_changed'].append({'call': int(kv['call']), 'id': int(kv['id']), 'generation': int(kv['generation']),
                                                               'from': kv['from'], 'to': kv['to'], 'identity': kv['identity']})
            elif tag in ('POST03_SUMMARY', 'POST03_HIT_SUMMARY', 'POST03_1_COLLIDER_DIAG', 'POST03_CONSERVATION'):
                tagm = re.search(r'\btag=(\w+)', body)
                if tagm and tagm.group(1) == 'SHUTDOWN':
                    rec = {k: int(v) for k, v in KV_NUM.findall(body) if k not in ('v',)}
                    fam = group(body, 'family', '/'.join(FAMILIES))
                    if fam:
                        rec['family_vec'] = dict(zip(FAMILIES, fam))
                    if tag == 'POST03_1_COLLIDER_DIAG':
                        for name in ('sel_class', 'raw_cc0_class', 'raw_cc1_class'):
                            mm = re.search(name + r'(?:\([a-z0-9_/]+\))?=(\d+(?:/\d+)*)', body)
                            rec[name + '_vec'] = dict(zip(SEL_CLASSES, [int(x) for x in mm.group(1).split('/')]))
                        rec['reason_vec'] = dict(zip(REASONS, group(body, 'reason', '/'.join(REASONS))))
                    if tag == 'POST03_SUMMARY':
                        adm = group(body, 'adm', 'cand/e_oc2/other/unsafe')
                        rec['adm_vec'] = dict(zip(['cand', 'e_oc2', 'other', 'unsafe'], adm))
                    out.setdefault(tag.lower(), {}).update(rec)
                else:
                    out['periodic_lines'] = out.get('periodic_lines', 0) + 1
            elif tag == 'POST03_1_INIT':
                kv = dict(FIELD_RE.findall(body))  # host_build_id y rutas NO se copian
                out['init'] = {k: kv[k] for k in ('version', 'source_commit', 'host', 'passive', 'pmf_bytes', 'capacity', 'log_cap', 'deref_gate', 'sizeof_cCcD_Obj') if k in kv}
            elif tag == 'POST03_TARGET':
                kv = {}
                for k, v in FIELD_RE.findall(body):
                    kv.setdefault(k, v)  # la 1.a aparicion es el valor real; la leyenda final no cuenta
                out['hook_target'] = {k: kv[k] for k in ('resolve', 'declared_target_resolved', 'same_address', 'inline_sites_flag') if k in kv}
            elif tag == 'POST03_HOOK_INSTALLED':
                kv = dict(FIELD_RE.findall(body))
                out['hook_installed'] = {k: kv[k] for k in ('post', 'pre', 'pre_returns') if k in kv}
            elif tag == 'POST03_SHUTDOWN':
                shutdown_line = n
                out['post03_shutdown'] = True
            continue
        if MODULE_TAG in l:
            other_module_lines += 1
        m = MOD_RE.search(l)
        if m:
            out['mods'].append({'id': m.group(1), 'name': m.group(2), 'version': m.group(3)})
        m = re.search(r'\[INFO \| dusk::mods::loader\] (\d+)/(\d+) mod\(s\) active', l)
        if m:
            out['mods_active'] = '%s/%s' % m.groups()
        if 'all mods unloaded' in l:
            out['all_mods_unloaded'] = True
            unloaded_line = n
        if l.startswith('  Backend: '):
            out['backend'] = l.split(':', 1)[1].strip()
        if 'HM203C SUMMARY(shutdown): events=' in l:
            mm = re.search(r'events=(\d+) valid=(\d+).*HP relation: match=(\d+) diff=(\d+) statusDiff=(\d+)', l)
            if mm:
                out.setdefault('hm', {}).update(dict(zip(('events', 'valid', 'hp_match', 'hp_diff', 'status_diff'), (int(x) for x in mm.groups()))))
        if 'HM203C SUMMARY(shutdown): cc_at_check pre=' in l:
            mm = re.search(r'pre=(\d+) post=(\d+) paired=(\d+) \| unmatchedPost=(\d+) orphanPre=(\d+)', l)
            if mm:
                out.setdefault('hm', {}).update(dict(zip(('pre', 'post', 'paired', 'unmatched_post', 'orphan_pre'), (int(x) for x in mm.groups()))))
        if 'HM203C SUMMARY(shutdown): modifiers seen' in l:
            mm = re.search(r'masterX2=(\d+)', l)
            if mm:
                out.setdefault('hm', {})['master_x2'] = int(mm.group(1))
        if 'HM203C SUMMARY(shutdown): damage combos' in l:
            for fam, lo, hi, cnt in re.findall(r'(?:510|496)/(\w+) (\d+)->(\d+) mods=0x[0-9a-f]+ x(\d+)', l):
                out.setdefault('hm_damage_combos', {}).setdefault(fam, 0)
                out['hm_damage_combos'][fam] += int(cnt)
        if 'BARS203 HM bridge(shutdown)' in l:
            out['bars_bridge'] = {k: int(v) for k, v in KV_NUM.findall(l.split('bridge(shutdown)', 1)[1]) if k in ('queries', 'ok', 'unavailable', 'invalid', 'rejected')}
        if 'BARS203 CP03 shutdown' in l:
            out['bars_draw'] = {k: int(v) for k, v in KV_NUM.findall(l.split('shutdown:', 1)[1]) if k in ('barsDrawn', 'packetDraws', 'refused')}
        if l.startswith('[WARNING | dusk] CalcDivideInfo'):
            cdi += 1
        if l.startswith('[WARNING | aurora::texture] texture_replacement:'):
            tex += 1
        if 'event=PERF_WINDOW' in l:
            perf += 1
            perf_flag += 'MEASUREMENT_NOT_AN_ERROR' in l
        if 'DEVF_NATIVE_API event=REMOVE_RESULT' in l:
            devf_rm += 1
        if 'DEVF_ENCOUNTER_API event=REQUEST_ACCEPTED' in l:
            devf_acc += 1
    out['link_creation_pids'] = pids
    out['other_module_lines'] = other_module_lines
    out['shutdown_precedes_unload'] = bool(shutdown_line and unloaded_line and shutdown_line < unloaded_line)
    out['incidents'] = {'CalcDivideInfo_warning_lines': cdi, 'texture_replacement_warning_lines': tex, 'PERF_WINDOW_lines': perf,
                        'PERF_WINDOW_with_MEASUREMENT_NOT_AN_ERROR': perf_flag}
    if devf_rm or devf_acc:
        out['devf'] = {'REMOVE_RESULT_lines': devf_rm, 'REQUEST_ACCEPTED_lines': devf_acc}
    return out


def cross_check(sess):
    """Compara lo RECONSTRUIDO desde los eventos y lineas de vida con los contadores declarados en SHUTDOWN. Devuelve lista de discrepancias."""
    ev = sess['events']
    conf = [e for e in ev if e['kind'] == 'HIT_CONFIRMED']
    fin = [e for e in ev if e['kind'] == 'FINISH_NATIVE_OBSERVED']
    hs, sm, dg, cs = sess.get('post03_hit_summary', {}), sess.get('post03_summary', {}), sess.get('post03_1_collider_diag', {}), sess.get('post03_conservation', {})
    ll = sess['life_lines']
    fam = {k: 0 for k in FAMILIES}
    for e in conf:
        fam[FAMILY_NAME[e['family']]] += 1
    selc = {k: 0 for k in SEL_CLASSES}
    for e in conf:
        selc[e['sel_class']] += 1
    checks = [
        ('confirmed', len(conf), hs.get('confirmed')), ('finish', len(fin), hs.get('finish')), ('events_emitted', len(ev), hs.get('events_emitted')),
        ('dual_tg', sum(e['dual'] for e in conf), hs.get('dual_tg')), ('pair_distinct', sum(e['distinct'] for e in conf), hs.get('pair_distinct')),
        ('lethal', sum(e['lethal'] for e in ev), hs.get('lethal')), ('hp_changed', sum(1 for e in ev if e['hp_pre'] != e['hp_post']), hs.get('hp_changed')),
        ('family_vec', fam, hs.get('family_vec')), ('sel_class_vec', selc, dg.get('sel_class_vec')),
        ('match_cc0', sum(e['collider_src'] == 'cc0' for e in conf), dg.get('reason_vec', {}).get('match_cc0')),
        ('match_cc1', sum(e['collider_src'] == 'cc1' for e in conf), dg.get('reason_vec', {}).get('match_cc1')),
        ('deref_ok_mod8_0', selc['mod8_0'], dg.get('deref_ok_mod8_0')), ('deref_ok_mod8_4', selc['mod8_4'], dg.get('deref_ok_mod8_4')),
        ('records_created', len(ll['first_seen']), sm.get('records_created')), ('death_seen', len(ll['death_seen']), sm.get('death_seen')),
        ('absent_verified', sum(1 for r in ll['retired'] if r['reason'] == 'LOOKUP_ABSENT_VERIFIED' and r['delete_claim'] == 1), sm.get('absent_verified')),
        ('admission_changes', len(ll['admission_changed']), sm.get('admission_changes')),
        ('conservation', (cs.get('started'), cs.get('judged'), cs.get('pending'), cs.get('ok')), (hs.get('cand_started', 0) + hs.get('finish_started', 0), len(ev), 0, 1)),
        ('collider_unmatched_and_unavailable_zero', (hs.get('collider_unmatched'), hs.get('classification_unavailable')), (0, 0)),
    ]
    return [{'name': n, 'reconstructed': r, 'declared': d} for n, r, d in checks if r != d]


def actors(sess):
    ll = sess['life_lines']
    keyed = {}
    for r in ll['first_seen']:
        keyed[(r['id'], r['generation'])] = {'id': r['id'], 'generation': r['generation'], 'first_seen_call': r['call'], 'epoch_first_seen': r['epoch'], 'adm_first': r['adm']}
    for r in ll['death_seen']:
        keyed.setdefault((r['id'], r['generation']), {'id': r['id'], 'generation': r['generation']})['death_seen_call'] = r['call']
    for r in ll['retired']:
        k = keyed.setdefault((r['id'], r['generation']), {'id': r['id'], 'generation': r['generation']})
        k.update({'retired_call': r['call'], 'retired_reason': r['reason'], 'delete_claim': r['delete_claim'], 'retired_context_changed': r['context_changed']})
    for e in sess['events']:
        k = keyed.get((e['id'], e['generation']))
        if k is not None:
            k.setdefault('events', []).append(e['event'])
    for r in ll['admission_changed']:
        k = keyed.get((r['id'], r['generation']))
        if k is not None:
            k['admission_changes'] = k.get('admission_changes', 0) + 1
    return [keyed[k] for k in sorted(keyed)]


def derive(sess):
    ev = sess['events']
    conf = [e for e in ev if e['kind'] == 'HIT_CONFIRMED']
    fam = {k: 0 for k in FAMILIES}
    for e in conf:
        fam[FAMILY_NAME[e['family']]] += 1
    sel = {k: 0 for k in SEL_CLASSES}
    for e in conf:
        sel[e['sel_class']] += 1
    return {'events': len(ev), 'hit_confirmed': len(conf), 'finish_native': sum(e['kind'] == 'FINISH_NATIVE_OBSERVED' for e in ev), 'family': fam,
            'sel_class': sel, 'collider_src': {s: sum(e['collider_src'] == s for e in conf) for s in ('cc0', 'cc1')},
            'dual_tg_events': sum(e['dual'] for e in conf), 'pair_distinct_events': sum(e['distinct'] for e in conf),
            'unavailable_family': sum(e['family'] == 'UNAVAILABLE' for e in conf), 'hp_unchanged_confirmed': sum(e['hp_pre'] == e['hp_post'] for e in conf),
            'lethal_events': sum(e['lethal'] for e in ev), 'actor_generations_hit': len({(e['id'], e['generation']) for e in conf}),
            'by_link_instance': {str(p): sum(1 for e in conf if e['link_pid'] == p) for p in sorted({e['link_pid'] for e in conf})},
            'discrepancies': cross_check(sess)}


def privacy_check(blob, allowed=(), forbidden_words=()):
    for a in sorted(allowed, key=len, reverse=True):  # hashes/commit publicos DECLARADOS: unicos hex largos permitidos
        blob = blob.replace(a, '')
    for w in forbidden_words:  # nombres de cuenta u otras palabras privadas: se pasan por parametro/entorno, NUNCA se escriben en el repo
        if w and re.search(r'\b' + re.escape(w) + r'\b', blob, re.I):
            raise SystemExit('privacy scan failed on a forbidden word')
    for rx in PRIVACY:
        m = rx.search(blob)
        if m:
            raise SystemExit('privacy scan failed on pattern %s' % rx.pattern)


def build(logs, expects):
    sessions = {s: parse_log(p, expects.get(s, {})) for s, p in logs.items()}
    rows = []
    for s in sorted(sessions):
        seen = {}
        for i, e in enumerate(sessions[s]['events'], 1):
            k = (e['id'], e['generation'])
            seen[k] = seen.get(k, 0) + 1
            e['actor_hit_ord'] = seen[k]
            e['hp_delta'] = e['hp_pre'] - e['hp_post']
            rows.append([s, i] + [e[c] for c in TSV_COLS[2:]])
    tsv = '\t'.join(TSV_COLS) + '\n' + ''.join('\t'.join('' if x is None else str(x) for x in r) + '\n' for r in rows)
    summary = {'schema_version': SCHEMA_VERSION, 'sessions': {}}
    for s in sorted(sessions):
        d = {k: v for k, v in sessions[s].items() if k not in ('events', 'life_lines')}
        d['derived'] = derive(sessions[s])
        d['actors'] = actors(sessions[s])
        d['lifecycle_counts'] = {k: len(v) for k, v in sessions[s]['life_lines'].items()}
        summary['sessions'][s] = d
    agg = {'events': len(rows)}
    for k in ('hit_confirmed', 'finish_native', 'unavailable_family'):
        agg[k] = sum(summary['sessions'][s]['derived'][k] for s in summary['sessions'])
    agg['family'] = {f: sum(summary['sessions'][s]['derived']['family'][f] for s in summary['sessions']) for f in FAMILIES}
    agg['sel_class'] = {c: sum(summary['sessions'][s]['derived']['sel_class'][c] for s in summary['sessions']) for c in SEL_CLASSES}
    agg['discrepancies'] = sum(len(summary['sessions'][s]['derived']['discrepancies']) for s in summary['sessions'])
    summary['aggregate'] = agg
    manifest = {'schema_version': SCHEMA_VERSION, 'sources': {s: {k: sessions[s][k] for k in ('file_name', 'sha256', 'bytes', 'splitlines')} for s in sorted(sessions)},
                'notes': 'los logs crudos NO se versionan; solo estos metadatos y la evidencia saneada'}
    return sessions, tsv, summary, manifest


def run(logs, outdir, expects=None, forbidden_words=()):
    expects = expects or {}
    forbidden_words = tuple(forbidden_words) + tuple(w for w in os.environ.get('POST031_PRIVACY_WORDS', '').split(',') if w)
    sessions, tsv, summary, manifest = build(logs, expects)
    blob = json.dumps(summary, sort_keys=True, indent=1) + '\n'
    mblob = json.dumps(manifest, sort_keys=True, indent=1) + '\n'
    sblob = json.dumps(SCHEMA, sort_keys=True, indent=1) + '\n'
    allowed = [sessions[s]['sha256'] for s in sessions] + [sessions[s].get('init', {}).get(k, '') for s in sessions for k in ('source_commit', 'host')]
    allowed = [a for a in allowed if a]
    for t in (tsv, blob, mblob, sblob):
        privacy_check(t, allowed, forbidden_words)
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    for name, data in (('POST031_A1_B1_EVENTS_SANITIZED.tsv', tsv), ('POST031_A1_B1_SUMMARY_SANITIZED.json', blob), ('POST031_A1_B1_SOURCE_MANIFEST.json', mblob),
                       ('POST031_A1_B1_SCHEMA.json', sblob)):
        (outdir / name).write_text(data, encoding='utf-8', newline='\n')
    return summary


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--log-a', required=True, help='A1')
    ap.add_argument('--log-b', required=True, help='B1')
    ap.add_argument('--output-dir', required=True)
    for s in ('a', 'b'):
        ap.add_argument('--expect-sha-' + s)
        ap.add_argument('--expect-bytes-' + s, type=int)
        ap.add_argument('--expect-lines-' + s, type=int)
    a = ap.parse_args()
    expects = {k: {'sha256': getattr(a, 'expect_sha_' + k.lower()), 'bytes': getattr(a, 'expect_bytes_' + k.lower()), 'splitlines': getattr(a, 'expect_lines_' + k.lower())}
               for k in ('A', 'B')}
    summary = run({'A1': a.log_a, 'B1': a.log_b}, a.output_dir, {'A1': expects['A'], 'B1': expects['B']})
    print(json.dumps(summary['aggregate'], sort_keys=True))
    return 1 if summary['aggregate']['discrepancies'] else 0


if __name__ == '__main__':
    sys.exit(main())
