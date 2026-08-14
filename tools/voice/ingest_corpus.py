#!/usr/bin/env python3
"""arifOS voice corpus ingester — ingests audio files into the dialect corpus vault.

Usage: python3 ingest_corpus.py [--src DIR] [--speaker NAME] [--dialect TAG]
Copies (never moves — F1 reversible) audio into /root/AAA/corpus/voice/raw/YYYY-MM/
with a sha-keyed manifest in meta/YYYY-MM/manifest.json.
"""
import os, json, shutil, hashlib, subprocess, argparse
from datetime import datetime

VAULT = '/root/AAA/corpus/voice'

def probe_duration(p):
    try:
        out = subprocess.run(['ffprobe', '-v', 'quiet', '-show_entries', 'format=duration',
                              '-of', 'csv=p=0', p], capture_output=True, text=True, timeout=15)
        return round(float(out.stdout.strip()), 1)
    except Exception:
        return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--src', default='/root/.hermes/cache/audio')
    ap.add_argument('--speaker', default='ARIF')
    ap.add_argument('--dialect', default='penang-malay')
    ap.add_argument('--consent', default='F13-sovereign-self')
    args = ap.parse_args()

    month = datetime.utcnow().strftime('%Y-%m')
    raw = os.path.join(VAULT, 'raw', month)
    meta = os.path.join(VAULT, 'meta', month)
    os.makedirs(raw, exist_ok=True)
    os.makedirs(meta, exist_ok=True)

    src_files = []
    for root, dirs, files in os.walk(args.src):
        for f in files:
            if f.lower().endswith(('.ogg', '.oga', '.mp3', '.wav', '.m4a', '.opus', '.webm')):
                src_files.append(os.path.join(root, f))

    manifest_path = os.path.join(meta, 'manifest.json')
    manifest = json.load(open(manifest_path)) if os.path.exists(manifest_path) else []
    known = {m['sha16'] for m in manifest}

    added = 0
    for p in sorted(src_files):
        data = open(p, 'rb').read()
        h = hashlib.sha256(data).hexdigest()[:16]
        if h in known:
            continue
        ext = os.path.splitext(p)[1]
        dst = os.path.join(raw, h + ext)
        shutil.copy2(p, dst)
        m = {
            'sha16': h, 'source_path': p, 'bytes': len(data),
            'duration_s': probe_duration(dst),
            'mtime': datetime.fromtimestamp(os.stat(p).st_mtime).isoformat(timespec='seconds'),
            'ingested_at': datetime.utcnow().isoformat(timespec='seconds') + 'Z',
            'speaker': args.speaker, 'dialect': args.dialect, 'consent': args.consent,
            'transcript_status': 'pending', 'transcript': None, 'intent': None,
        }
        manifest.append(m)
        added += 1

    json.dump(manifest, open(manifest_path, 'w'), indent=1)
    total = sum(m.get('duration_s') or 0 for m in manifest)
    print(f"CORPUS manifest: {len(manifest)} files | {round(total/60, 1)} min | added this run: {added}")

if __name__ == '__main__':
    main()
