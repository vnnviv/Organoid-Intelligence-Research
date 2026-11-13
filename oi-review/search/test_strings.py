import urllib.request,urllib.parse,json,re,time
E="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
def es(term,retmax=10000):
    for k in range(6):
        try: return _es(term,retmax)
        except Exception: time.sleep(3+3*k)
    return _es(term,retmax)
def _es(term,retmax=10000):
    d=urllib.parse.urlencode({"db":"pubmed","term":term,"retmax":retmax,"retmode":"json"}).encode()
    return json.loads(urllib.request.urlopen(urllib.request.Request(E+"esearch.fcgi",data=d),timeout=60).read())["esearchresult"]
recs=json.load(open('screening_ids.json'))
# map includes to PMIDs (pmid:, pmcid: via idconv, doi via esearch [doi])
inc=[r for r in recs if r['dec']=='Include']
pm=set()
pmcs=[r['id'].split(':')[1].upper() for r in inc if r['id'].startswith('pmcid:')]
j=json.loads(urllib.request.urlopen("https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?format=json&tool=oi-review&ids="+",".join(pmcs),timeout=30).read())
for x in j['records']:
    if x.get('pmid'): pm.add(str(x['pmid']))
for r in inc:
    if r['id'].startswith('pmid:'): pm.add(r['id'][5:])
    if r['id'].startswith('doi:'):
        ids=es(r['id'][4:]+"[doi]")['idlist']; pm|=set(ids); time.sleep(1.2)
print("Includes indexed in PubMed:",len(pm),sorted(pm))
json.dump(sorted(pm),open('inc_pmids.json','w'))
