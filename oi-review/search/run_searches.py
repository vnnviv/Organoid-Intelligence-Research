"""Run Search_Log S1 (PubMed, as planned) and S5 (arXiv). Writes CSVs + a run log."""
import json, csv, time, urllib.request, urllib.parse, datetime, xml.etree.ElementTree as ET
E="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
S1=('("organoid intelligence"[tiab] OR "synthetic biological intelligence"[tiab] OR wetware[tiab] OR biocomput*[tiab] OR ((organoid*[tiab] OR "neural culture*"[tiab] OR "neuronal culture*"[tiab] OR "cortical culture*"[tiab] OR "biological neural network*"[tiab] OR "multielectrode array*"[tiab] OR "microelectrode array*"[tiab]) AND ("reservoir comput*"[tiab] OR "reinforcement learning"[tiab] OR "closed-loop"[tiab] OR "goal-directed"[tiab] OR "sample efficien*"[tiab] OR "energy efficien*"[tiab] OR "machine learning"[tiab] OR classif*[tiab] OR "information processing"[tiab]))) AND 2020/01/01:3000/12/31[dp]')
def post(url,data):
    req=urllib.request.Request(url,data=urllib.parse.urlencode(data).encode())
    for i in range(5):
        try: return urllib.request.urlopen(req,timeout=60).read()
        except Exception as e: time.sleep(2+i*2); err=e
    raise err
r=json.loads(post(E+"esearch.fcgi",{"db":"pubmed","term":S1,"retmax":10000,"retmode":"json","tool":"oi-review"}))["esearchresult"]
ids=r["idlist"]; print("S1 count",r["count"],len(ids))
rows=[]
for i in range(0,len(ids),200):
    x=post(E+"efetch.fcgi",{"db":"pubmed","id":",".join(ids[i:i+200]),"retmode":"xml","tool":"oi-review"})
    root=ET.fromstring(x)
    for art in root.findall(".//PubmedArticle"):
        pmid=art.findtext(".//PMID"); title="".join(art.find(".//ArticleTitle").itertext()) if art.find(".//ArticleTitle") is not None else ""
        ab=" ".join("".join(t.itertext()) for t in art.findall(".//Abstract/AbstractText"))
        yr=art.findtext(".//PubDate/Year") or (art.findtext(".//PubDate/MedlineDate") or "")[:4]
        doi=""; pmc=""
        for aid in art.findall("./PubmedData/ArticleIdList/ArticleId"):
            if aid.get("IdType")=="doi": doi=(aid.text or "").lower()
            if aid.get("IdType")=="pmc": pmc=aid.text or ""
        jr=art.findtext(".//Journal/Title") or ""
        pt=";".join(p.text for p in art.findall(".//PublicationType") if p.text)
        rows.append({"pmid":pmid,"doi":doi,"pmcid":pmc,"year":yr,"journal":jr,"title":title,"pubtypes":pt,"abstract":ab})
    time.sleep(0.4)
with open("S1_pubmed.csv","w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
log={"S1":{"date":datetime.date.today().isoformat(),"string":S1,"count":int(r["count"]),"fetched":len(rows),"translation":r.get("querytranslation","")}}
json.dump(log,open("run_log.json","w"),indent=1)
print("fetched",len(rows))
