# Branch Archive Plan — AAA

| Branch | Status | Recommendation | Reason |
|--------|--------|----------------|--------|
| `main` | active | keep | primary |
| `master` | archive | archive only | 15 ahead, 202 behind |
| `aaa/routing-v2026-05-02` | active | keep | 5 ahead |
| `feat/repo-routing-constitution-2026-05-02` | active | keep | 4 ahead |
| `imgbot` | delete_candidate | archive only | 71 behind |
| `workspace-sync` | delete_candidate | archive only | 74 behind |
| `workspace-sync-publish` | delete_candidate | archive only | 3 ahead, 73 behind |

## Cleanup Commands
```bash
# To archive a branch locally before deletion:
git checkout <branch>
git tag archive/<branch>
git checkout main
git branch -D <branch>

# To delete remote (888_HOLD):
# git push origin --delete <branch>
```
