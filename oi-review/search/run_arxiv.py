import urllib.request, urllib.parse, time, csv, json, datetime, xml.etree.ElementTree as ET
Q='abs:"organoid intelligence" OR abs:"synthetic biological intelligence" OR abs:wetware OR (abs:organoid AND (abs:"reservoir computing" OR abs:"reinforcement learning")) OR (abs:"neuronal culture" AND abs:learning)'
ns={"a":"http://www.w3.org/2005/Atom","x":"http://arxiv.org/schemas/atom"}
rows=[];start=0;total=None
while True:
    url="https://export.arxiv.org/api/query?"+urllib.parse.urlencode({"search_query":Q,"start":start,"max_results":200,"sortBy":"submittedDate","sortOrder":"descending"})
    root=ET.fromstring(urllib.request.urlopen(url,timeout=60).read())
    total=int(root.findtext("{http://a9.com/-/spec/opensearch/1.1/}totalResults"))
    es=root.findall("a:entry",ns)
    for e in es:
        pub=e.findtext("a:published",namespaces=ns)[:10]
        aid=e.findtext("a:id",namespaces=ns).rsplit("/abs/",1)[-1]
        rows.append({"arxiv":aid.split("v")[0] if "v" in aid else aid,"published":pub,"title":" ".join(e.findtext("a:title",namespaces=ns).split()),
                     "doi":(e.findtext("x:doi",namespaces=ns) or "").lower(),"abstract":" ".join(e.findtext("a:summary",namespaces=ns).split())})
    start+=len(es)
    if not es or start>=total: break
    time.sleep(3)
inrange=[r for r in rows if r["published"]>="2020-01-01"]
with open("S5_arxiv.csv","w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(inrange)
log=json.load(open("run_log.json")); log["S5"]={"date":datetime.date.today().isoformat(),"string":Q+" ; submitted 2020-01-01 onward (filtered after retrieval)","count_all_dates":total,"count_2020_on":len(inrange)}
json.dump(log,open("run_log.json","w"),indent=1); print(total,len(rows),len(inrange))
