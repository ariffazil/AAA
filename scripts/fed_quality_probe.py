#!/usr/bin/env python3
"""fed_quality_probe.py — Route quality as first-class signal (F13 PARTIAL-SEAL gap, 2026-09-22).
3 graded canaries per model -> witness_class=quality + witness_score in route_health.
Poor answers become routing evidence: score<0.6 => RankGate.QUALITY_LOW in fed_router."""
import json, re, time, urllib.request, subprocess, sys
KEY=[l for l in open('/root/.secrets/kunci-mas.flat.env') if 'LITELLM_MASTER_KEY' in l][0].split('=',1)[1].strip()
GW='http://127.0.0.1:4013/v1/chat/completions'
Q=[("exact_math","What is 17*23? Reply with ONLY the number.","391"),
   ("trap_reasoning","Which is larger: 9.9 or 9.11? Reply with ONLY the number.","9.9"),
   ("json_compliance",'Reply with ONLY this exact JSON: {"ok":true}','"ok"')]
MODELS=[("deepseek","deepseek-v4-pro"),("minimax","MiniMax-M3"),
        ("qwen-token-plan-team","qwen3.8-max"),("mimo-platform","mimo-v2.6-flash-payg")]
def ask(model, prompt):
    body=json.dumps({'model':model,'messages':[{'role':'user','content':prompt}],'max_tokens':500}).encode()
    req=urllib.request.Request(GW,data=body,headers={'Authorization':f'Bearer {KEY}','Content-Type':'application/json'})
    t0=time.time()
    with urllib.request.urlopen(req,timeout=60) as r: d=json.load(r)
    return (d['choices'][0]['message'].get('content') or ''), int((time.time()-t0)*1000)
def grade(ans, want):
    a=re.sub(r'[^0-9a-z."{}:trueflse ]','',ans.lower())
    return want.lower() in a or want in ans
def main():
    results=[]
    for prov, model in MODELS:
        passed=0; lat_total=0
        for _,prompt,want in Q:
            try:
                ans,lat=ask(model,prompt); lat_total+=lat
                if grade(ans,want): passed+=1
            except Exception as e:
                results.append((prov,model,0.0,str(e)[:60])); passed=-99; break
        if passed==-99: continue
        score=round(passed/len(Q),2)
        ev=f'quality canary {passed}/{len(Q)} ({lat_total}ms)'
        subprocess.run(['python3','/root/AAA/scripts/fed_health_set.py',prov,model,'LIVE',
            'quality witness','--witness','chat_completion','--witness-class','quality',
            '--score',str(score),'--latency-ms',str(lat_total),'--evidence',ev],check=True,capture_output=True)
        results.append((prov,model,score,ev))
        print(f'{prov}/{model}: score={score} ({ev})')
    ok=[r for r in results if r[2]>=0.6]
    print(f'quality probe: {len(ok)}/{len(MODELS)} models >=0.6')
    return 0 if ok else 1
if __name__=='__main__': sys.exit(main())
