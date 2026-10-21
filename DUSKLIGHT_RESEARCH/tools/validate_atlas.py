#!/usr/bin/env python3
"""Validate atlas references read-only against source and recorded remote metadata."""
import argparse,json,pathlib,re,urllib.parse

PIN='40457c6adb381928e4b5fef6ed459ed291edd5e2'
LEVELS={'DOC_CONTRACT','SOURCE_OBSERVED','STATIC_INFERRED','STATIC_CROSSCHECKED','CI_OBSERVED','WINDOWS_RUNTIME_OBSERVED','HUMAN_RUNTIME_OBSERVED','NOT_VERIFIED','BLOCKED'}
INTEGRATION={'OFFICIAL_SERVICE','TYPED_HOOK','SYMBOL_HOOK','ASSET_OVERLAY','SCRIPT_API','POTENTIAL_REQUIRES_VERIFICATION','NOT_SUPPORTED_BY_CURRENT_EVIDENCE'}
def parse_json(p):
    def pairs(items):
        d={}
        for k,v in items:
            if k in d:raise ValueError('Duplicate JSON key: '+k)
            d[k]=v
        return d
    return json.loads(p.read_text(),object_pairs_hook=pairs)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('source',type=pathlib.Path);ap.add_argument('--files',type=pathlib.Path);args=ap.parse_args()
    atlas=pathlib.Path(__file__).resolve().parents[1];source=args.source.resolve()
    if source==atlas or source in atlas.parents:raise ValueError('Atlas must be outside analyzed source')
    ledger=parse_json(atlas/'EVIDENCE_LEDGER.json');symbols=parse_json(atlas/'SYMBOL_INDEX.json');systems=parse_json(atlas/'SYSTEM_INDEX.json')
    evidence=ledger['evidence'];ids={x['id'] for x in evidence};sids={x['system_id'] for x in systems}
    assert len(ids)==len(evidence),'Duplicate evidence ID'
    assert len(sids)==len(systems),'Duplicate system ID'
    for x in systems:
        assert set(x.get('dependencies',[]))<=sids,('Missing dependency',x['system_id'])
        assert set(x.get('evidence_ids',[]))<=ids,('Missing system evidence',x['system_id'])
    remote={(x['repo'],x['commit'],x['path']):x['line_count'] for x in ledger.get('remote_source_metadata',[])}
    for x in ledger.get('historical_ci_observed',[]):remote[(x['repo'],x['head_sha'],x['path'])]=x['workflow_line_count']
    counts={};refs=0;unique_ranges=set();unknown=set()
    def check(q):
        nonlocal refs
        key=(q['repo'],q['commit'],q['path'])
        if q['repo']=='TwilitRealm/dusklight':
            assert q['commit']==PIN,key
            p=source/q['path'];assert p.is_file(),key
            if p not in counts:counts[p]=len(p.read_text(errors='replace').splitlines())
            n=counts[p]
        elif key in remote:n=remote[key]
        else:unknown.add(key);return
        assert 1<=q['line_start']<=q['line_end']<=n,(q,n)
        refs+=1;unique_ranges.add((*key,q['line_start'],q['line_end']))
    for x in evidence:
        assert x['level'] in LEVELS,x['id']
        for q in x['sources']:check(q)
    seen=set()
    for x in symbols:
        for k in ['symbol','kind','system_id','source','purpose','dependencies','integration','conditions','risks','evidence_level','evidence_ids']:assert k in x,(x.get('symbol'),k)
        assert x['kind'] in {'function','method','struct','enum','global','service'},x['symbol']
        assert x['evidence_level'] in LEVELS and x['integration'] in INTEGRATION,x['symbol']
        assert x['system_id'] in sids and set(x['evidence_ids'])<=ids,x['symbol']
        assert x.get('signature'),x['symbol']
        for k in ['dependencies','conditions','risks','evidence_ids']:assert isinstance(x[k],list),(x['symbol'],k)
        q=x['source'];check(q);key=(x['symbol'],x['kind'],q['repo'],q['commit'],q['path'],q['line_start'])
        assert key not in seen,('Duplicate symbol record',key);seen.add(key)
    paths=parse_json(args.files) if args.files else [p.relative_to(atlas).as_posix() for p in atlas.rglob('*') if p.is_file() and p.suffix in {'.md','.json'}]
    for name in paths:
        p=atlas/name
        if p.suffix=='.json':parse_json(p)
        if p.suffix!='.md':continue
        text=p.read_text()
        for evidence_id in re.findall(r'\b(?:SDK|HOOK|WORLD|PLAYER|PRES|ROOT|HIST|CALLBACK|ARCH|PORT)-\d{3}\b',text):
            assert evidence_id in ids,('Unknown evidence ID in Markdown',name,evidence_id)
        for target in re.findall(r'\]\(([^)]+)\)',text):
            if '://' in target or target.startswith('#'):continue
            dest=(p.parent/urllib.parse.unquote(target.split('#')[0])).resolve()
            assert atlas==dest or atlas in dest.parents,('Outside atlas',name,target)
            assert dest.is_file(),('Missing relative link',name,target)
        for repo,commit,path,a,b in re.findall(r'https://github.com/([^/]+/[^/]+)/blob/([0-9a-f]{40})/([^#)]+)#L(\d+)(?:-L(\d+))?',text):
            check(dict(repo=repo,commit=commit,path=urllib.parse.unquote(path),line_start=int(a),line_end=int(b or a)))
    assert not unknown,('Remote source metadata missing; fetch exact cited file',sorted(unknown))
    result=dict(checkpoint=ledger['checkpoint'],evidence=len(evidence),symbol_records=len(symbols),systems=len(systems),validated_code_range_occurrences=refs,unique_code_ranges=len(unique_ranges),cited_upstream_files=len(counts),checked_atlas_files=len(paths),runtime_tested=False,scope='Editorial/reference validation only; duplicate citations count as occurrences. Does not certify semantic correctness, exports, build or game runtime.')
    (atlas/'VALIDATION_REPORT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False))
if __name__=='__main__':main()
