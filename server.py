"""Local student-search demo for authorized performance experiments."""
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import sqlite3, json, os, time, html
ROOT=os.path.dirname(__file__)
DB=os.path.join(ROOT,'students.db')

def init_db():
    with sqlite3.connect(DB) as c:
        c.execute('CREATE TABLE IF NOT EXISTS students(id INTEGER PRIMARY KEY, code TEXT, name TEXT, class_name TEXT)')
        if c.execute('SELECT count(*) FROM students').fetchone()[0]==0:
            c.executemany('INSERT INTO students(code,name,class_name) VALUES(?,?,?)',[(f'SV{i:05}',f'Sinh viên {i}',f'CNTT{(i%8)+1:02}') for i in range(1,5001)])
        c.execute('CREATE INDEX IF NOT EXISTS idx_code ON students(code)')

PAGE='''<!doctype html><html lang="vi"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Tra cứu sinh viên — Performance Lab</title><style>body{font:16px system-ui;background:#f1f5f9;color:#0f172a;margin:0}.wrap{max-width:900px;margin:60px auto;background:white;padding:36px;border-radius:18px;box-shadow:0 10px 30px #cbd5e155}h1{margin:0 0 12px}input,button{font:inherit;padding:12px;border-radius:8px;border:1px solid #cbd5e1}input{width:60%}button{background:#155e75;color:white;cursor:pointer}table{width:100%;border-collapse:collapse;margin-top:24px}td,th{padding:10px;text-align:left;border-bottom:1px solid #e2e8f0}.hint{color:#64748b}</style><main class="wrap"><h1>Tra cứu sinh viên</h1><p class="hint">Website thực hành chạy trên localhost · 5.000 hồ sơ mẫu</p><input id="q" placeholder="Nhập mã SV, tên hoặc lớp" value="SV001"><button onclick="search()">Tìm kiếm</button><p id="status"></p><table><thead><tr><th>Mã SV</th><th>Họ tên</th><th>Lớp</th></tr></thead><tbody id="rows"></tbody></table></main><script>async function search(){const t=performance.now();const r=await fetch('/api/students?q='+encodeURIComponent(document.querySelector('#q').value));const d=await r.json();document.querySelector('#status').textContent=d.count+' kết quả · '+Math.round(performance.now()-t)+' ms (đo từ trình duyệt)';document.querySelector('#rows').innerHTML=d.students.map(x=>'<tr><td>'+x.code+'</td><td>'+x.name+'</td><td>'+x.class_name+'</td></tr>').join('')}search()</script></html>'''
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        u=urlparse(self.path)
        if u.path=='/':
            payload=PAGE.encode(); typ='text/html; charset=utf-8'
        elif u.path=='/api/students':
            q=parse_qs(u.query).get('q',[''])[0][:40]
            # Demo deliberately supports controlled latency injection via environment variable.
            delay=float(os.environ.get('LAB_DELAY_MS','0'))/1000
            if delay>0: time.sleep(min(delay,0.5))
            with sqlite3.connect(DB,timeout=10) as c:
                rows=c.execute('SELECT code,name,class_name FROM students WHERE code LIKE ? OR name LIKE ? OR class_name LIKE ? LIMIT 25',tuple(['%'+q+'%']*3)).fetchall()
            payload=json.dumps({'count':len(rows),'students':[dict(zip(('code','name','class_name'),r)) for r in rows]},ensure_ascii=False).encode();typ='application/json; charset=utf-8'
        else:
            self.send_error(404);return
        self.send_response(200);self.send_header('Content-Type',typ);self.send_header('Content-Length',str(len(payload)));self.end_headers();self.wfile.write(payload)
    def log_message(self,*args): pass
if __name__=='__main__':
    init_db();print('Open http://127.0.0.1:18765',flush=True);ThreadingHTTPServer(('127.0.0.1',18765),Handler).serve_forever()
