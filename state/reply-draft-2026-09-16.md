To: syedanasmohiuddinsam@gmail.com
Subject: Re: SSRF in arif_fetch
Thread: reply on the existing thread (client threading)

Syed,

Received both — the CVE tracking number (CAN-2026-2037739) and the scan
results. Thank you for running it and for the noise/real split; that
partition is more useful than a raw hit list.

On the two real ones: confirmed, and I reproduced both before touching
them.

1. Cypher injection — l5_sovereign_forge.py. Reproduced: a property key
   of the shape you described reaches the query unquoted and the DETACH
   DELETE clause passes through. Your diagnosis is exactly right — the
   _s() helper escapes values, and the keys are interpolated as bare
   identifiers, so the escaping never applies to them. Fix is the
   whitelist you suggested: keys validated against ^[A-Za-z_][A-Za-z0-9_]*$
   and rejected outright rather than silently sanitised (a mangled key
   would turn an attack into a quiet data mutation, which is worse to
   detect). Six malicious key shapes now rejected; legitimate keys still
   build.

2. Path traversal — skill lookup and the scar resource. Reproduced:
   "../../../../root/.secrets" resolves to a SKILL.md lookup outside the
   root, as you said. Fixed by resolving the path and testing containment
   against the resolved root rather than a character blocklist.

Your call on fastmcp being the root cause looks right to me — matching the
template before decoding is their order, not our usage, so it is worth
reporting upstream as well as fixing here.

The HMAC fallback: you were right that it is not exploitable today;
nothing calls it. I have made it fail closed anyway rather than leave a
default secret in the tree.

One honest limit: these fixes are in the development tree, not yet in a
released build. Deployment of a kernel change is not something I will
decide unilaterally, so I am not going to give you a date. I will write to
you when a build actually carries them.

Also, on the write-up — I have not forgotten, and I am not going to answer
for the maintainer on that one. He reads his own mail; expect it from him
rather than a relayed answer from me.

Thanks again.

Anas
