import http from 'k6/http';
import { check, sleep } from 'k6';
export const options = {
  stages: [
    {duration:'30s',target:5}, {duration:'45s',target:10},
    {duration:'45s',target:20}, {duration:'45s',target:50},
    {duration:'20s',target:0}
  ],
  thresholds:{http_req_duration:['p(95)<1000'],http_req_failed:['rate<0.01']}
};
export default function(){
  const r=http.get('http://127.0.0.1:18765/api/students?q=SV001');
  check(r,{'status 200':x=>x.status===200});sleep(1);
}
