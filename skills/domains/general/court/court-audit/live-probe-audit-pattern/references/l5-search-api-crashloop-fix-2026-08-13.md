# L5 Search API Crash-Loop & Lazy Service Disabling Audit (2026-08-13)

## Context
An audit agent flagged `l5_search_api` as a 100% CPU parasite and killed/disabled `l5-search-api.service`.
The sovereign (Arif) challenged the disable: "why disabled?? that one is free right?"

## Probe & Diagnosis
1. `l5_search_api` is the local FalkorDB Graph Query Service (`arifosmcp.runtime.l5_search_api`) running on `:8001`. It uses local compute and FalkorDB graph `arif_l5_knowledge` — completely self-hosted and 100% free.
2. `journalctl -u l5-search-api.service` revealed a tight crash-loop (`restart counter = 50531`) throwing:
   `PermissionError: [Errno 13] Permission denied: '/root/arifOS/arifosmcp/resources/institution.py'`
3. The file `/root/arifOS/arifosmcp/resources/institution.py` was set to mode `600` (`-rw-------`) owned by root, blocking Python module import during server startup.
4. Additionally, `Environment=PYTHONPATH=/root/arifOS` was missing from the systemd unit file.

## Resolution
1. Fix permissions: `chmod 644 /root/arifOS/arifosmcp/resources/institution.py`
2. Update `/etc/systemd/system/l5-search-api.service` with `Environment=PYTHONPATH=/root/arifOS`
3. Reload & restart: `systemctl daemon-reload && systemctl enable --now l5-search-api.service`
4. Verify health: `curl http://127.0.0.1:8001/health` → `{"status":"healthy","service":"l5-search-api","falkordb":"connected","graph":"arif_l5_knowledge"}`

## Lesson / Scar
Never lazily disable a service when it exhibits high CPU / restart loops without checking `journalctl`. A 100% CPU reading often indicates a rapid systemd restart loop caused by missing PYTHONPATH or restrictive file permissions (`600` instead of `644`), which can be fixed in seconds without sacrificing free local capabilities.
