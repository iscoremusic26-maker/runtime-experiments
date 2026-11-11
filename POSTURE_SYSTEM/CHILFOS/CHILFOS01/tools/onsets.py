"""Onset analysis of the decoded combo recordings (pure Python, reproducible). Usage: onsets.py <wav> [verbose]"""
import wave, sys, math, array
w = wave.open(sys.argv[1]); sr = w.getframerate(); ch = w.getnchannels(); n = w.getnframes()
raw = array.array('h', w.readframes(n))
x = [ (raw[i] + raw[i+1]) / 65536.0 for i in range(0, len(raw), 2)] if ch == 2 else [v/32768.0 for v in raw]
hop = int(sr * 0.005); win = int(sr * 0.010)
E = []; H = []; Z = []
for s in range(0, len(x) - win, hop):
    seg = x[s:s+win]
    e = sum(v*v for v in seg) / win
    d = sum((seg[k]-seg[k-1])**2 for k in range(1, win)) / win   # high-frequency energy (first difference)
    zc = sum(1 for k in range(1, win) if (seg[k] >= 0) != (seg[k-1] >= 0)) / win
    E.append(e); H.append(d); Z.append(zc)
L = [10*math.log10(e + 1e-12) for e in E]; LH = [10*math.log10(h + 1e-12) for h in H]
floor = sorted(L)[len(L)//5]
# onset strength: positive rise of high-frequency log energy against the previous 30 ms minimum
flux = [0.0]*len(LH)
for i in range(len(LH)):
    prev = min(LH[max(0, i-6):i]) if i else LH[0]
    flux[i] = max(0.0, LH[i] - prev)
mx = max(flux)
cands = []
for i in range(1, len(flux)-1):
    if flux[i] >= flux[i-1] and flux[i] > flux[i+1] and flux[i] > 0.35*mx and L[i] > floor + 12:
        cands.append(i)
# merge peaks closer than 70 ms (the strongest wins)
ons = []
for i in cands:
    if ons and (i - ons[-1]) * 0.005 < 0.070:
        if flux[i] > flux[ons[-1]]: ons[-1] = i
    else:
        ons.append(i)
out = []
for i in ons:
    # precise onset: first 1 ms sample block before the peak where |x| exceeds 30% of the 40 ms peak amplitude
    s0 = max(0, i*hop - int(0.030*sr)); s1 = min(len(x), i*hop + int(0.040*sr))
    pk = max(abs(v) for v in x[s0:s1]); t = None
    for s in range(s0, s1):
        if abs(x[s]) >= 0.3*pk: t = s / sr; break
    j = max(range(i, min(len(L), i+12)), key=lambda k: L[k])
    dec = next((k for k in range(j, min(len(L), j+200)) if L[k] < L[j]-20), j+200)
    out.append(dict(t=round(t, 4), peak_db=round(L[j], 1), rise_db=round(flux[i], 1), bright=round(LH[j]-L[j], 1), zcr=round(Z[j], 3), decay20_ms=(dec-j)*5))
print('file=%s sr=%d dur=%.4f floor_db=%.1f max_flux=%.1f' % (sys.argv[1].split('/')[-1], sr, len(x)/sr, floor, mx))
prev = None
for o in out:
    o['dt'] = None if prev is None else round(o['t'] - prev, 4); prev = o['t']
    print(o)
