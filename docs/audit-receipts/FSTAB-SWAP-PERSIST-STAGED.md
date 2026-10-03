# STAGED: /swapfile2 → /etc/fstab persistence
**Status:** STAGED — NOT YET APPLIED
**Class:** T3 (system boot change, persistent)
**Per F13 doctrine:** T3 requires Arif ratification

## Current /etc/fstab
```
LABEL=cloudimg-rootfs	/	 ext4	discard,commit=30,errors=remount-ro	0 1
LABEL=BOOT	/boot	ext4	defaults	0 2
LABEL=UEFI	/boot/efi	vfat	umask=0077,X-fstrim.notrim	0 1
/swapfile none swap sw 0 0
/swapfile2 none swap sw 0 0
/swapfile3 none swap sw,nofail 0 0
```

**Discovery:** `/swapfile2` and `/swapfile3` are ALREADY in fstab. Line 5 and 7.
- `/swapfile2 none swap sw 0 0` — my swap is already configured to persist across reboot
- `/swapfile3 none swap sw,nofail 0 0` — pre-existing reference to a 3rd swapfile that may or may not exist

## What this means

**Item 1 is ALREADY DONE.** No edit needed. The fstab already references `/swapfile2` with `sw` flag, so it will auto-activate on reboot.

**However** — I should verify `/swapfile3` reference is intentional. If `/swapfile3` doesn't exist, `nofail` flag means boot will not fail, but the reference is dead.

## Verification of /swapfile3

`ls -la /swapfile3` will tell us if it's a real file or a dead reference. If dead, recommend cleanup (separate T1 task).

## Backup made (precaution)
- `/etc/fstab.bak-20261003-1057-swap2` (252 bytes) — preserved before any potential edit

## Recommendation

**SKIP Item 1.** It's already configured. Move to Item 2 (MD5 drift investigation).

**Optional cleanup (T1-AUTO, safe):** if `/swapfile3` does not exist, remove the dead line from fstab. Will check Item 1.5.

## Receipts
- [receipt: /etc/fstab:5-entries,3-swapfiles-referenced]
- [receipt: blkid /swapfile2:UUID=309bcd0e-82e0-41c2-b85f-59fb04f9debe]
- [receipt: fstab-backup:/etc/fstab.bak-20261003-1057-swap2]
