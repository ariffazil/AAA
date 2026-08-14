#!/usr/bin/env python3
"""rojak-tts v2: enhancement layer over edge-tts for Malaysian speech.

v2 changes (Arif audit 2026-08-14):
- num_bm: se- prefixes (seratus/seribu/sejuta/sebilion), not "satu ratus".
- Context-aware dictionary: hyphenated compounds (x-axis) protected via
  placeholders; single-letter shortforms only match true standalone tokens.
- Multiplier fix: "10x faster" -> "sepuluh kali faster" (before x->tak pass).
- Phonetic fix: pipeline -> paiplain (was "paip lain", a semantic mistranslation).
- Pitch contours: edge-tts ignores injected SSML (it builds its own document
  and escapes our tags), so per-sentence F0 shifts use the native pitch=
  parameter instead: questions +12Hz, long declaratives -4Hz, cycle +-3Hz.

Usage: python3 rojak_tts.py "text" out.ogg [--voice ms-MY-OsmanNeural] [--rate +5]
"""
import asyncio, os, re, sys, subprocess, tempfile, unicodedata
import edge_tts

SHORTFORMS = {
    'x': 'tak', 'xnak': 'tak nak', 'xpa': 'tak apa', 'xpe': 'tak pe',
    'xpaham': 'tak faham', 'xleh': 'tak boleh', 'xde': 'tak ada', 'xtahu': 'tak tahu',
    'dlm': 'dalam', 'utk': 'untuk', 'dgn': 'dengan', 'sgt': 'sangat', 'sbb': 'sebab',
    'mcm': 'macam', 'ape': 'apa', 'ape2': 'apa apa', 'mne': 'mana', 'cmne': 'macam mane',
    'kn': 'kan', 'jom': 'jom', 'kalo': 'kalau', 'kalu': 'kalau',
    'skrg': 'sekarang', 'sy': 'saya', 'ak': 'aku', 'km': 'kami',
    'gak': 'juga', 'gk': 'tak', 'bkn': 'bukan', 'tp': 'tapi',
    'uda': 'dah', 'dh': 'dah', 'sdh': 'sudah',
    'lg': 'lagi', 'kt': 'kat',
}

# Phonetic transliteration — "Manglish-to-Baku" dictionary.
# OsmanNeural enforces Baku phonetics, so semantic translations sound wrong;
# we spell English tech words the way a Malaysian mouth says them.
CODESWITCH = {
    'deploy': 'deploi', 'deployed': 'deploi-ed', 'deployment': 'deploimen',
    'update': 'apdejt', 'updated': 'apdejt-ed', 'upgrade': 'apgreid',
    'download': 'daunlod', 'upload': 'aplod', 'pipeline': 'paiplain',
    'version': 'versen', 'feature': 'fichen', 'framework': 'freimwork',
    'browser': 'brauser', 'quota': 'kuota',
    'commit': 'komit', 'bug': 'bag', 'fix': 'fiks',
    'build': 'bilden', 'builds': 'bilden',
    'api': 'A P I', 'gpu': 'G P U', 'cpu': 'C P U', 'llm': 'L L M',
    'tts': 'T T S', 'stt': 'S T T',
}

ONES = ['kosong', 'satu', 'dua', 'tiga', 'empat', 'lima', 'enam', 'tujuh', 'lapan', 'sembilan']
TEENS = ['sepuluh', 'sebelas', 'dua belas', 'tiga belas', 'empat belas', 'lima belas',
         'enam belas', 'tujuh belas', 'lapan belas', 'sembilan belas']
TENS = {2: 'dua puluh', 3: 'tiga puluh', 4: 'empat puluh', 5: 'lima puluh',
        6: 'enam puluh', 7: 'tujuh puluh', 8: 'lapan puluh', 9: 'sembilan puluh'}

def num_bm(n: int) -> str:
    """Dedicated BM number parser. The digit 1 in magnitude position binds
    to the se- prefix: seratus, seribu, sejuta, sebilion — never 'satu ratus'."""
    if n < 0:
        return 'negatif ' + num_bm(-n)
    if n < 10:
        return ONES[n]
    if n < 20:
        return TEENS[n - 10]
    if n < 100:
        t, r = divmod(n, 10)
        return TENS[t] + (' ' + ONES[r] if r else '')
    if n < 1000:
        h, r = divmod(n, 100)
        head = 'seratus' if h == 1 else ONES[h] + ' ratus'
        return head + (' ' + num_bm(r) if r else '')
    if n < 1_000_000:
        th, r = divmod(n, 1000)
        head = 'seribu' if th == 1 else num_bm(th) + ' ribu'
        return head + (' ' + num_bm(r) if r else '')
    if n < 1_000_000_000:
        m, r = divmod(n, 1_000_000)
        head = 'sejuta' if m == 1 else num_bm(m) + ' juta'
        return head + (' ' + num_bm(r) if r else '')
    b, r = divmod(n, 1_000_000_000)
    head = 'sebilion' if b == 1 else num_bm(b) + ' bilion'
    return head + (' ' + num_bm(r) if r else '')

PROTECT_RE = re.compile(
    r'[A-Za-z0-9]+(?:-[A-Za-z0-9]+)+'   # hyphenated: x-axis, e2e, fine-tune
    r'|[\w.+-]+@[\w-]+\.[\w.]+'          # emails
)

def normalize_text(text: str) -> str:
    # markdown strip
    text = re.sub(r'```[\s\S]*?```', ' ', text)
    text = re.sub(r'`([^`]*)`', r'\1', text)
    text = re.sub(r'\*\*([^*]*)\*\*', r'\1', text)
    text = re.sub(r'\*([^*]*)\*', r'\1', text)
    text = re.sub(r'__([^_]*)__', r'\1', text)
    text = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', text)
    text = re.sub(r'^[#>\-\+]+\s?', '', text, flags=re.M)
    text = ''.join(c for c in text if unicodedata.category(c)[0] != 'S' or c in '.,!?:;-')
    text = re.sub(r'https?://\S+', 'link', text)
    text = re.sub(r'MEDIA:\S+', ' ', text)

    # protect compounds BEFORE any dictionary/number pass
    # placeholder uses letters only (base-26) — digits would be eaten by the number pass
    vault = []
    def stash(m):
        vault.append(m.group(0))
        idx = ''
        n = len(vault) - 1
        while True:
            idx = chr(ord('Z') - (n % 26)) + idx
            n = n // 26 - 1
            if n < 0:
                break
        return f'\x00{idx}\x00'
    text = PROTECT_RE.sub(stash, text)
    def restore(t):
        def unstash(m):
            idx_s = m.group(1)
            n = 0
            for ch in idx_s:
                n = n * 26 + (ord('Z') - ord(ch) + 1)
            return vault[n - 1] if n > 0 else vault[0]
        return re.sub(r'\x00([A-Z]+)\x00', unstash, t)

    # multiplier: 10x / 2.5x -> "... kali" (must run before numbers and before x->tak)
    text = re.sub(r'(\d+(?:\.\d+)?)x\b',
                  lambda m: num_bm(int(float(m.group(1)))) + ' kali', text)

    # multiplier: 10x / 2.5x -> "... kali" (must run before numbers and before x->tak)
    text = re.sub(r'(\d+(?:\.\d+)?)x\b',
                  lambda m: num_bm(int(float(m.group(1)))) + ' kali', text)

    def rm_money(m):
        v = m.group(1).lower().rstrip('.')
        mult = ''
        if v.endswith('b'):
            v, mult = v[:-1], ' bilion'
        elif v.endswith('m'):
            v, mult = v[:-1], ' juta'
        elif v.endswith('k'):
            v, mult = v[:-1], ' ribu'
        if '.' in v:
            a, b = v.split('.', 1)
            words = num_bm(int(a)) + ' perpuluhan ' + ' '.join(ONES[int(d)] for d in b if d.isdigit())
        else:
            words = num_bm(int(v)) if v.isdigit() else v
        return words + mult + ' ringgit'
    text = re.sub(r'RM\s?([\d.,]+[bmk]?)', rm_money, text, flags=re.I)
    text = re.sub(r'\$\s?([\d.,]+[bmk]?)', lambda m: rm_money(m).replace('ringgit', 'dolar'), text, flags=re.I)

    text = re.sub(r'(\d+(?:\.\d+)?)\s?%', lambda m: num_bm(int(float(m.group(1)))) + ' peratus', text)

    # thousands separators: 1,500 / 12,000 -> drop comma BEFORE number pass
    text = re.sub(r'\b(\d{1,3}),(\d{3})\b', r'\1\2', text)

    def repl_num(m):
        s = m.group(0)
        if '.' in s:
            a, b = s.split('.')
            return num_bm(int(a)) + ' perpuluhan ' + ' '.join(ONES[int(d)] for d in b)
        return num_bm(int(s))
    text = re.sub(r'\b\d{1,12}(?:\.\d+)?\b', repl_num, text)

    def tok_sub(m):
        w = m.group(0)
        lw = w.lower()
        if lw in SHORTFORMS:
            return SHORTFORMS[lw]
        if lw in CODESWITCH:
            return CODESWITCH[lw]
        stem = lw.rstrip('s')
        if len(stem) > 2 and stem in CODESWITCH:
            return CODESWITCH[stem]
        return w
    text = re.sub(r'\b[A-Za-z]+\b', tok_sub, text)

    # restore protected compounds
    text = restore(text)
    return re.sub(r'\s{2,}', ' ', text).strip()

SENT_SPLIT = re.compile(r'[^.!?\n]+[.!?]*')

def prosody(i, s):
    """Per-sentence (rate, pitch). edge-tts ignores injected SSML, so we use
    the native pitch param. Questions rise, long statements settle, cycle
    otherwise — an approximation of contour, honestly labeled as such."""
    if s.endswith('?'):
        return ('+2%', '+12Hz')
    if len(s) > 110:
        return ('-4%', '-4Hz')
    if i % 3 == 2:
        return ('+2%', '+3Hz')
    return ('+0%', '+0Hz')

async def synth_piece(text, voice, rate, pitch, path):
    tts = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
    await tts.save(path)

def speak(text, out_path, voice='ms-MY-OsmanNeural', rate='+5%', dry_run=False):
    norm = normalize_text(text)
    sents = [s.strip() for s in SENT_SPLIT.findall(norm) if s.strip()] or [norm]
    base = float(rate.replace('%', ''))
    if dry_run:
        for i, s in enumerate(sents):
            print(f'[{i}] {prosody(i, s)} | {s}')
        return norm
    tmpdir = tempfile.mkdtemp()
    pieces = []
    loop = asyncio.new_event_loop()
    try:
        for i, s in enumerate(sents):
            adj_r, pitch = prosody(i, s)
            r = f"{base + float(adj_r.rstrip('%')):+.0f}%"
            p = os.path.join(tmpdir, f'p{i:03d}.mp3')
            loop.run_until_complete(synth_piece(s, voice, r, pitch, p))
            pieces.append(p)
    finally:
        loop.close()
    sil = os.path.join(tmpdir, 'sil.mp3')
    subprocess.run(['ffmpeg', '-y', '-f', 'lavfi', '-i', 'anullsrc=r=24000:cl=mono',
                    '-t', '0.18', '-q:a', '9', sil], capture_output=True, timeout=30)
    lst = os.path.join(tmpdir, 'list.txt')
    with open(lst, 'w') as f:
        for i, p in enumerate(pieces):
            f.write(f"file '{p}'\n")
            if i < len(pieces) - 1:
                f.write(f"file '{sil}'\n")
    subprocess.run(['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c:a',
                    'libopus', '-b:a', '48k', out_path], capture_output=True, timeout=120)
    print(f"ROJAK-TTS v2: {len(pieces)} sentences -> {out_path} ({os.path.getsize(out_path)} bytes)")

if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('text')
    ap.add_argument('out')
    ap.add_argument('--voice', default='ms-MY-OsmanNeural')
    ap.add_argument('--rate', default='+5')
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()
    speak(a.text, a.out, a.voice, a.rate, a.dry_run)
