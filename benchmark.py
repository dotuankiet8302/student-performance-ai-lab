"""Measure local search API; user counts mean concurrent workers, not real users."""
import csv,time,urllib.request,concurrent.futures,statistics,os
URL='http://127.0.0.1:18765/api/students?q=SV001'
OUT=os.path.join(os.path.dirname(__file__),'results.csv')
def request(level,trial):
    t=time.perf_counter();status=0
    try:
        with urllib.request.urlopen(URL,timeout=10) as r:
            status=r.status;r.read()
    except Exception: status=0
    return {'level':level,'trial':trial,'latency_ms':round((time.perf_counter()-t)*1000,3),'status':status,'timestamp':time.time()}
if __name__=='__main__':
    rows=[]
    for level in [1,5,10,20,50]:
        with concurrent.futures.ThreadPoolExecutor(max_workers=level) as pool:
            batch=list(pool.map(lambda i:request(level,i),range(100)))
        rows.extend(batch)
        lat=sorted(x['latency_ms'] for x in batch)
        print(f'workers={level:2d} p95={lat[int(.95*(len(lat)-1))]:.2f}ms errors={sum(x["status"]!=200 for x in batch)}')
    with open(OUT,'w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
    print('Saved',OUT)
