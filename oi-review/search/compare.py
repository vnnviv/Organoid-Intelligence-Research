import json,time
exec(open('test_strings.py').read().split("recs=json.load")[0])
inc=set(json.load(open('inc_pmids.json')))
D=' AND 2020/01/01:3000/12/31[dp]'
OI='("organoid intelligence"[tiab] OR "synthetic biological intelligence"[tiab] OR wetware[tiab] OR "biological computing"[tiab] OR "biocomputer*"[tiab])'
OLD=open('run_searches.py').read().split("S1=(")[1].split("')")[0].strip("'")
N='("brain organoid*"[tiab] OR "cerebral organoid*"[tiab] OR "cortical organoid*"[tiab] OR "neural organoid*"[tiab] OR "forebrain organoid*"[tiab] OR assembloid*[tiab] OR "neural culture*"[tiab] OR "neuronal culture*"[tiab] OR "cortical culture*"[tiab] OR "cultured neuron*"[tiab] OR "cultured cortical"[tiab] OR "neuronal network*"[tiab] OR "biological neural network*"[tiab] OR "biological neuronal network*"[tiab] OR "in vitro neur*"[tiab] OR "dissociated"[tiab])'
I='("multielectrode*"[tiab] OR "multi-electrode*"[tiab] OR "microelectrode*"[tiab] OR MEA[tiab] OR MEAs[tiab] OR electrophysiolog*[tiab] OR "electrical stimulation"[tiab] OR optogenet*[tiab] OR "calcium imaging"[tiab])'
C='("reservoir comput*"[tiab] OR "reinforcement learning"[tiab] OR "closed-loop"[tiab] OR "closed loop"[tiab] OR "goal-directed"[tiab] OR "sample efficien*"[tiab] OR "energy efficien*"[tiab] OR "machine learning"[tiab] OR "information processing"[tiab] OR comput*[tiab] OR learning[tiab] OR memory[tiab] OR classif*[tiab] OR "pattern recognition"[tiab] OR "logic gate*"[tiab] OR boolean[tiab] OR "artificial intelligence"[tiab])'
cands={"S1 as planned":OLD,
 "Rev A: OI terms OR (neural AND interface AND claim)":'('+OI+' OR ('+N+' AND '+I+' AND '+C+'))'+D,
 "Rev B: OI terms OR (neural AND claim)":'('+OI+' OR ('+N+' AND '+C+'))'+D}
out={}
for k,q in cands.items():
    r=es(q); ids=set(r['idlist']); hit=inc&ids
    out[k]={"count":int(r['count']),"recall":f"{len(hit)}/{len(inc)}","missed":sorted(inc-ids),"query":q}
    print(f"{k:55s} records {r['count']:>6}  PubMed-indexed includes found {len(hit)}/{len(inc)}  missed {sorted(inc-ids)}")
    time.sleep(1.5)
json.dump(out,open('string_test.json','w'),indent=1)

STRONG='("reservoir comput*"[tiab] OR "reinforcement learning"[tiab] OR "closed-loop"[tiab] OR "closed loop"[tiab] OR "machine learning"[tiab] OR "artificial intelligence"[tiab] OR "learning algorithm*"[tiab] OR "sample efficien*"[tiab] OR "energy efficien*"[tiab] OR "decision-making"[tiab] OR "learning and memory"[tiab])'
I2=I[:-1]+' OR stimulat*[tiab])'
more={"Rev C: OI OR (N AND I AND C) OR (N AND strong claim)":'('+OI+' OR ('+N+' AND '+I+' AND '+C+') OR ('+N+' AND '+STRONG+'))'+D,
      "Rev D: as C, interface includes stimulat*":'('+OI+' OR ('+N+' AND '+I2+' AND '+C+') OR ('+N+' AND '+STRONG+'))'+D}
for k,q in more.items():
    r=es(q); ids=set(r['idlist']); hit=inc&ids
    out[k]={"count":int(r['count']),"recall":f"{len(hit)}/{len(inc)}","missed":sorted(inc-ids),"query":q}
    print(f"{k:55s} records {r['count']:>6}  includes {len(hit)}/{len(inc)}  missed {sorted(inc-ids)}"); time.sleep(1.5)
json.dump(out,open('string_test.json','w'),indent=1)
