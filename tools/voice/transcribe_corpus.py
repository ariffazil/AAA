#!/usr/bin/env python3
"""Transcribe pending corpus files via Groq whisper-large-v3-turbo.
Fills transcript + transcript_status in the manifest. Only processes files
where speaker consent = F13-sovereign-self or explicit.
"""
import os, json, sys
from datetime import datetime, timezone

VAULT = '/root/AAA/corpus/voice'
GROQ_URL = 'https://api.groq.com/openai/v1/audio/transcriptions'
POST_URL = GROQ_URL  # alias used by curl call

def main():
    month = datetime.now(timezone.utc).strftime('%Y-%m')
    meta_dir = os.path.join(VAULT, 'meta', month)
    raw_dir = os.path.join(VAULT, 'raw', month)
    mpath = os.path.join(meta_dir, 'manifest.json')
    manifest = json.load(open(mpath))

    import urllib.request, uuid
    key = os.environ.get('GROQ_API_KEY')
    if not key:
        print('NO GROQ KEY'); sys.exit(1)

    import subprocess, tempfile
    done = 0
    for m in manifest:
        if m.get('transcript_status') not in ('pending',) and not str(m.get('transcript_status', '')).startswith('error'):
            if m.get('transcript_status') != 'pending':
                continue
        if m.get('transcript_status') != 'pending' and not str(m.get('transcript_status', '')).startswith('error'):
            continue
        src = os.path.join(raw_dir, m['sha16'] + os.path.splitext(m['source_path'])[1])
        if not os.path.exists(src):
            m['transcript_status'] = 'missing_file'; continue
        mime = {'ogg': 'audio/ogg', 'oga': 'audio/ogg', 'mp3': 'audio/mpeg', 'wav': 'audio/wav',
                'm4a': 'audio/mp4', 'opus': 'audio/ogg', 'webm': 'audio/webm'}[os.path.splitext(src)[1].lstrip('.')]
        try:
            r = subprocess.run([
                'curl', '-s', '-m', '120', '-X', 'POST', POST_URL,
                '-H', f'Authorization: Bearer {key}',
                '-F', f'file=@{src};type={mime}',
                '-F', 'model=whisper-large-v3-turbo',
                '-F', 'language=ms',
                '-F', 'prompt=Bahasa Melayu loghat utara, campur English. Contoh: hang, depa, kambus, gila babas, macam ni, tak payah pening.',
            ], capture_output=True, text=True, timeout=150)
            out = json.loads(r.stdout)
            if 'text' in out:
                m['transcript'] = out['text'].strip()
                m['transcript_status'] = 'done' if m['transcript'] else 'empty'
                m['transcribed_at'] = datetime.now(timezone.utc).isoformat(timespec='seconds')
                m['stt_engine'] = 'groq-whisper-large-v3-turbo'
                done += 1
                print(f"[OK] {m['sha16']}: {m['transcript'][:110]}")
            else:
                m['transcript_status'] = f"error: {str(out)[:80]}"
                print(f"[ERR] {m['sha16']}: {str(out)[:100]}")
        except Exception as e:
            m['transcript_status'] = f'error: {str(e)[:80]}'
            print(f"[ERR] {m['sha16']}: {str(e)[:100]}")

    json.dump(manifest, open(mpath, 'w'), indent=1, ensure_ascii=False)
    total = sum(m.get('duration_s') or 0 for m in manifest)
    triad = sum(1 for m in manifest if m.get('transcript_status') == 'done')
    print(f"TRIAD: {triad}/{len(manifest)} transcribed | corpus {round(total/60,1)} min")

if __name__ == '__main__':
    main()
