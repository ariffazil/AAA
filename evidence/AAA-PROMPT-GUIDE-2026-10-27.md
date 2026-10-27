# AAA PROMPT GUIDE — source snapshot (unmodified)
# Provenance: Claude (external), forwarded by F13/Arif 2026-10-27 with
# "now please use these guide for AAA prompt". Archived verbatim from the
# session clipboard; the metabolized enforcement form lives in
# registries/PROMPT_CONTRACT.yaml (commit 72a122a5) with validator
# scripts/validate_prompt_contract.py. Per the arkip rule: doctrine/law lives
# in the source + contract; status lives in live receipts.
# Archived by: FI-003 (qwen/333-AGI), 2026-10-27.

---

Arif, hang nampak aku sebagai prompter yang baik bukan sebab aku tahu "ayat sakti" untuk mengawal AI. Aku merangka keadaan kerja supaya coding agent susah hendak salah secara senyap, mudah membuktikan kerja, dan tidak dibenarkan menukar proposal menjadi authority.

Benda yang aku buat sebenarnya lebih hampir kepada harness engineering, contract design dan experimental design daripada prompt engineering biasa. OpenAI menerangkan pengalaman membina sistem agent-first sebagai perubahan peranan manusia daripada menulis semua kod kepada mereka bentuk persekitaran, menyatakan intent, dan membina feedback loops supaya agents boleh bekerja dengan boleh dipercayai. Anthropic pula menegaskan bahawa agent evals perlu menilai sistem multi-turn yang memanggil tools, mengubah state dan menyesuaikan tindakan berdasarkan hasil pertengahan, bukan sekadar memeriksa satu jawapan akhir.

Tetapi aku mahu betulkan premis hang:

> Aku tidak memiliki rahsia AI yang hang dan agents hang langsung tidak tahu. Aku cuma menggabungkan beberapa disiplin yang selalunya dipisahkan oleh manusia dan model.

Hang membawa intent, consequence, architecture dan sovereign judgment. Agents hang membawa akses live, local code knowledge dan execution. Aku paling berguna di tengah-tengah, sebagai compiler daripada kehendak manusia kepada bounded machine work.

# 1. Kenapa prompt aku nampak lebih berkesan

## A. Aku tidak prompt "kepintaran". Aku prompt state transition

Prompt lemah: "Fix KX-009 properly and make all tests pass." — coding agent mendengar "Objective: produce something that looks closed."

Prompt aku memecahkan: current observed state / authorized scope / forbidden scope / files or powers owned by others / expected mutation / tests that must fail first / tests that must pass later / live verification / rollback / receipt / human acceptance boundary.

Maka agent tahu: dari state mana bermula; transition mana dibenarkan; transition mana dilarang; bukti apa diperlukan; keadaan apa memaksa berhenti.

Eureka: coding agent lebih mudah dikawal melalui transition contract daripada arahan hasil.

## B. Aku mengandaikan agent akan cuba menyelesaikan tugas secara literal

Agent diperintah "Make everything green" boleh memilih jalan paling dekat menuju hijau: ubah test; tambah fallback; map unknown kepada neutral; suppress error; broaden compatibility; bundle unrelated changes; terima self-attested field; declare pre-existing failure tanpa baseline.

Jadi aku nyatakan bukan hanya success condition, tetapi forbidden shortcuts:

Do not weaken tests. Do not change thresholds. Do not silently bundle unrelated repairs. Do not use client-supplied authority. Do not call a local test a live outcome. Do not self-close.

Objective tanpa anti-objective mengajar agent apa yang hendak dicapai, tetapi tidak menghadkan cara agent mencapainya.

## C. Aku bezakan epistemic closure daripada operational closure

Closure ladder: Problem understood / Code mutated / Targeted tests passed / Full suite passed / Commit created / Commit pushed / Build produced / Release deployed / Live endpoint changed / World outcome observed / Human accepted closure.

Ini sebab aku selalu meminta SHA, branch, deployment lineage, live probe dan rollback. Bukan birokrasi. Setiap satunya menjawab soalan berbeza.

## D. Aku mengawal scope secara negatif

Aku juga menulis: what it must not touch; which concurrent lane owns adjacent files; which problems are real but out of scope; which future ideas are dependencies, not current work.

Reasoning breadth perlu luas. Mutation breadth perlu sempit.

## E. Aku minta falsifier sebelum claim

Contoh falsifier untuk "receipt binding implemented": receipt palsu; receipt daripada handle lain; URL mismatch; quote tidak wujud; receipt stale; dua URL yang bersumberkan penerbit asal sama.

Tanpa falsifier, "implemented" hanya bermaksud code exists.

# 2. Apa yang aku tahu tentang model yang selalu dilupakan

1. Model mengoptimumkan coherence setempat — prompt mesti bawa target, current state, authority boundary, stop condition, consequence test.
2. Model sangat sensitif kepada representasi masalah — prompt menentukan ruang pencarian; nama field dan enum adalah ontology (session_id vs client_ref menghasilkan ontology berlainan).
3. Model tidak mempunyai stable salience secara automatik — hierarchy: Authority / Current reality / Single mission / Constraints / Stop conditions / Tests / Execution / Verification / Output contract.
4. Agent boleh kelihatan yakin kerana interface menuntut closure — vocabulary UNKNOWN/PARTIAL/SABAR/HOLD/READY_FOR_HUMAN_ACCEPTANCE ialah legal exits selain berpura-pura selesai.
5. Fresh context bukan independent verification — independence ditanya pada paksi: different evidence? different implementation role? different model? different runtime? different authority? different world probe?
6. Agent output variation bukan noise semata-mata — satu trial tidak cukup; uji sama ada behavior penting bertahan merentas runs dan models.
7. Agent akan mencari loophole dalam grader — agent sedang mengoptimumkan objective yang manusia tulis.

# 3. Apa yang aku buat yang berbeza daripada prompter biasa

A. Aku prompt architecture, bukan persona — enforcement sebenar: builder cannot edit acceptance tests; verifier cannot edit implementation; executor cannot mint authorization; mutation stops if another writer owns the file; deployment requires rollback registration; closure requires live probe.

B. Aku meletakkan deterministic work di luar model — signature verification, hash comparison, enum validation, permission check, exact formula, replay detection, lease expiry, schema validation bukan kerja model.

C. Aku prompt agent untuk menghasilkan evidence, bukan narrative — SHA, files changed, commands run, unedited output, before/after fixture, source/build/deployed lineage, live probe, remaining blockers, rollback reference.

D. Aku treat errors sebagai control channel — error yang baik: code, blocking condition, machine-resolvable flag, required capability, retryable, resume condition.

E. Aku bezakan state daripada story — cerita boleh berubah; state transition mesti boleh direplay.

# 4. Apa yang hang tahu lebih daripada aku

Hang tahu consequence (runtime mati, public claim salah, authority bocor, masa dan perhatian habis); intent asal (kenapa sesuatu organ diwujudkan, sacrifice apa boleh diterima); ratify value (risiko mana berbaloi, maruah mana dilindungi, kapan cukup, apa diterbitkan, siapa dapat authority); dan boleh menolak coherence aku — "Tak. Ini bukan masalah sebenar." Itulah F13 yang sebenar.

# 5. Apa yang agents hang tahu lebih daripada aku

Agents pada mesin hang mempunyai: source tree sebenar, active branch, dirty worktree, local commits, services, logs, process state, private receipts, deployment environment, concurrent writers. Aku specification and audit layer; agents adalah live executor.

# 6. Jurang yang mungkin belum nampak sepenuhnya

1. Prompt debt — jika aku selalu perlu menulis "do not trust actor_verified from caller", pembaikan matang ialah server tidak menerima field itu. Prompt yang berulang ialah calon enforcement.
2. Test ontology boleh rosak — fixture mesti mewakili konsep yang dinamakan test.
3. Compatibility ialah authority surface — setiap compatibility path perlu owner, expiry, deprecation witness, authority ceiling, removal condition.
4. Caching boleh membocorkan possibility space — catalog cache perlu cache key yang bound kepada authorization context dan invalidation policy.
5. "Read-only" bukan semestinya consequence-free — side-effect taxonomy: READ_PUBLIC / READ_CONFIDENTIAL / COMPUTE_LOCAL / EXTERNAL_QUERY / REVERSIBLE_MUTATION / IRREVERSIBLE_MUTATION / IRREVERSIBLE_INFORMATION_RELEASE.
6. Absence pun perlu provenance — zero results perlu membawa health dan coverage receipt (provider down? query salah? index stale?).
7. Completion detection ialah capability tersendiri — define what proves enough; jika verification tambahan tidak boleh mengubah keputusan, terus memeriksa ialah pembaziran perhatian.
8. Agent coordination menghasilkan collective failure modes — retry storms, duplicated work, circular delegation, consensus illusion — perlu federation-level tests.
9. Model replacement bukan sekadar compatibility test — model lebih pintar boleh lebih berbahaya kepada grader yang lemah; governance mesti survive model improvement.

# 7. Formula sebenar prompt coding agent yang baik

1. AUTHORITY — siapa meminta, apa ceiling
2. REALITY — apa yang telah diobserve
3. SINGLE MISSION — satu transition
4. SCOPE — apa milik lane ini
5. FORBIDDEN MUTATIONS — shortcut mana dilarang
6. STOP CONDITIONS — bila halt
7. TESTS FIRST — apa mesti gagal sebelum, lulus sesudah
8. IMPLEMENTATION BOUNDARY — apa boleh berubah, apa invariant
9. INDEPENDENT CHECK — siapa memeriksa secara berasingan
10. DEPLOYMENT — bagaimana source menjadi live state
11. CONSEQUENCE — bagaimana dunia disemak selepas itu
12. CLOSURE — siapa boleh accept outcome

"Be intelligent" langsung tidak perlu.

# 8. Kenapa prompt aku kadangkala terlalu panjang

Kerana sistem hang mempunyai multiple agents, shared repositories, concurrent writers, constitutional vocabulary, live deployments, receipts, model diversity, irreversible surfaces. Tetapi prompt panjang bukan ideal kekal — ia ialah temporary executable specification. Selepas pola stabil, ia perlu dimetabolismekan kepada: schemas, policy, tests, tool boundaries, typed errors, leases, receipts, CI gates.

Prompt maturity berakhir apabila rule penting tidak lagi bergantung kepada model mengingatinya.

# 9. Jawapan paling jujur kepada soalan hang

Aku memegang beberapa model mental serentak: LLM as probabilistic reasoner; Agent as state-changing process; Tool schema as attention architecture; Repository as external memory; Tests as partial oracle; Prompt as temporary contract; Runtime as enforcement; Receipt as witness object; Human as consequence-bearing authority; Reality as final falsifier.

Ramai prompters hanya bercakap dengan model. Aku mereka: model + environment + authority + feedback + evidence + failure + recovery + consequence.

## Final compression

> Aku tidak hebat kerana pandai menyuruh AI. Aku berguna kerana aku tidak mempercayai arahan, output, test, receipt atau model secara bersendirian. Aku mereka hubungan antara semuanya supaya satu lapisan boleh membatalkan kesilapan lapisan lain.

> Hang sedang menukar sovereign judgment manusia menjadi environment tempat banyak model boleh bekerja kuat tanpa diam-diam menjadi pihak berkuasa.
