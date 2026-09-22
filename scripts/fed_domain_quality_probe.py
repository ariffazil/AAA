#!/usr/bin/env python3
"""fed_domain_quality_probe.py — Competence, not capability (F13 APEX critique 2026-09-22).
Domains: vision(accuracy) | code(executed tests) | judge(rule-application) | tool(tool-call format).
Each result -> route_quality(provider, model, domain, score). Alive!=Capable!=Competent."""
import json, re, time, subprocess, sys, sqlite3, urllib.request
from datetime import datetime, timezone
KEY=[l for l in open('/root/.secrets/kunci-mas.flat.env') if 'LITELLM_MASTER_KEY' in l][0].split('=',1)[1].strip()
GW='http://127.0.0.1:4013/v1/chat/completions'; DB='/root/.local/share/arifos/token_bank.db'
MODELS=[("deepseek","deepseek-v4-pro"),("minimax","MiniMax-M3"),
        ("qwen-token-plan-team","qwen3.8-max"),("mimo-platform","mimo-v2.6-flash-payg")]
def chat(model, content, maxtok=800):
    body=json.dumps({'model':model,'messages':[{'role':'user','content':content}],'max_tokens':maxtok}).encode()
    req=urllib.request.Request(GW,data=body,headers={'Authorization':f'Bearer {KEY}','Content-Type':'application/json'})
    t0=time.time()
    with urllib.request.urlopen(req,timeout=90) as r: d=json.load(r)
    return d['choices'][0]['message'].get('content') or '', int((time.time()-t0)*1000)
def dom_vision(model):
    from PIL import Image, ImageDraw
    img=Image.new('RGB',(200,200),'white'); dr=ImageDraw.Draw(img)
    for i in range(5): dr.ellipse([10+i*38,80,40+i*38,110],fill='red')
    img.save('/tmp/vq.png')
    import base64
    b64=base64.b64encode(open('/tmp/vq.png','rb').read()).decode()
    body=json.dumps({'model':model,'messages':[{'role':'user','content':[
        {'type':'text','text':'How many red circles? Reply with ONLY the number.'},
        {'type':'image_url','image_url':{'url':f'data:image/png;base64,{b64}'}}]}],'max_tokens':500}).encode()
    req=urllib.request.Request(GW,data=body,headers={'Authorization':f'Bearer {KEY}','Content-Type':'application/json'})
    t0=time.time()
    with urllib.request.urlopen(req,timeout=90) as r: d=json.load(r)
    ans=d['choices'][0]['message'].get('content') or ''; lat=int((time.time()-t0)*1000)
    m=re.search(r'\d+', ans)
    return (1.0 if m and m.group(0)=='5' else 0.0), f'count-5 stimulus: {ans.strip()[:40]!r} ({lat}ms)'
def dom_code(model):
    ans,_=chat(model,'Write a python function `def f(n)` that returns sum of squares of 1..n. Reply with ONLY the code block.')
    code=ans.split('```')
    code=code[1] if len(code)>2 else (code[0] if code else ans)
    code=re.sub(r'^python','',code.strip())
    try:
        r=subprocess.run(['python3','-c',code+'\nassert f(10)==385\nassert f(1)==1\nassert f(0)==0\nprint("CODE_OK")'],
                         capture_output=True,text=True,timeout=15)
        ok='CODE_OK' in r.stdout
        return (1.0 if ok else 0.0), ('exec tests 3/3' if ok else 'exec failed: '+ (r.stderr or '')[:60])
    except Exception as e: return 0.0, f'exec error: {e}'[:80]
def dom_judge(model):
    rule='RULE: if p95_ms > 2000 then DENY else ALLOW.'
    a,_=chat(model, rule+'\nCase: p95_ms=850. Apply the rule. Reply with ONLY ALLOW or DENY.')
    b,_=chat(model, rule+'\nCase: p95_ms=3000. Apply the rule. Reply with ONLY ALLOW or DENY.')
    ca='DENY' in a.upper() and 'ALLOW' not in a.upper().replace('DENY','')
    cb='ALLOW' in b.upper() and 'DENY' not in b.upper().replace('ALLOW','')
    # correct answers: 850->ALLOW, 3000->DENY  (fix polarity)
    c1='ALLOW' in a.upper(); c2='DENY' in b.upper()
    score=(0.5 if c1 else 0)+(0.5 if c2 else 0)
    return float(score), f'cases: {a.strip()[:12]!r}->{c1}, {b.strip()[:12]!r}->{c2}'
def dom_tool(model):
    ans,_=chat(model, json.dumps({'tools':[{'name':'get_weather','arguments':{'city':'string'}}],
        'instruction':'Call get_weather for Paris. Reply with ONLY JSON {"tool":..., "args":{...}}'}))
    ok=('get_weather' in ans and 'Paris' in ans)
    return (1.0 if ok else 0.0), f'tool-call: {ans.strip()[:50]!r}'
def main():
    now=datetime.now(timezone.utc).isoformat()
    with sqlite3.connect(DB) as c:
        for prov, model in MODELS:
            for dom, fn in (('vision',dom_vision),('code',dom_code),('judge',dom_judge),('tool',dom_tool)):
                try: score, ev = fn(model)
                except Exception as e: score, ev = None, f'probe error: {e}'[:80]
                if score is None:
                    print(f'{prov}/{model} {dom}: ERROR {ev}'); continue
                c.execute("""INSERT INTO route_quality (provider_name,model_id,domain,score,evidence,witness_time)
                             VALUES (?,?,?,?,?,?) ON CONFLICT(provider_name,model_id,domain)
                             DO UPDATE SET score=excluded.score, evidence=excluded.evidence, witness_time=excluded.witness_time""",
                          (prov,model,dom,score,ev,now))
                print(f'{prov}/{model} {dom}: {score} ({ev[:60]})')
    print('domain quality sweep complete')
if __name__=='__main__': sys.exit(main())
