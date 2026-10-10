#!/usr/bin/env python3
"""jobplane CLI — create / claim / heartbeat / release / transition / show / list.

Thin wrapper over jobplane.core.JobPlane. Prints JSON to stdout; errors to
stderr with exit code 2. Ledger path comes from --ledger or $JOBPLANE_LEDGER
(default /root/AAA/jobplane/ledger/jobs.jsonl).

Usage examples:
    python3 -m jobplane.cli create --repo /root/x --base-commit abc123 \
        --requested-by arif --proposed-by 555-ASI \
        --allowed /root/x/src --acceptance "pytest -q" --authorization-receipt REC1
    python3 -m jobplane.cli transition <job_id> AUTHORIZED --actor arif --role HUMAN
    python3 -m jobplane.cli transition <job_id> QUEUED --actor 555-ASI
    python3 -m jobplane.cli claim <job_id> --holder 555-ASI --ttl 900
    python3 -m jobplane.cli heartbeat <job_id> --holder 555-ASI
    python3 -m jobplane.cli release <job_id> --holder 555-ASI --to VERIFYING
    python3 -m jobplane.cli show <job_id>
    python3 -m jobplane.cli list --state LEASED
"""

from __future__ import annotations

import argparse
import json
import sys

from .core import DEFAULT_LEDGER, JobPlane, JobPlaneError


def _emit(obj) -> None:
    print(json.dumps(obj, indent=2, sort_keys=True))


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="jobplane", description="Minimal durable job envelope control-plane")
    p.add_argument("--ledger", default=DEFAULT_LEDGER, help="path to append-only JSONL ledger")
    sub = p.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("create", help="create a job (PROPOSED)")
    c.add_argument("--repo", default="", help="repository root")
    c.add_argument("--base-commit", default="", dest="base_commit")
    c.add_argument("--mutation-class", default="code_edit", dest="mutation_class")
    c.add_argument("--allowed", nargs="*", default=[], help="allowed paths")
    c.add_argument("--forbidden", nargs="*", default=[], help="forbidden paths")
    c.add_argument("--acceptance", nargs="*", default=[], help="acceptance test commands")
    c.add_argument("--precondition", nargs="*", default=[])
    c.add_argument("--requested-by", default="", dest="requested_by")
    c.add_argument("--proposed-by", default="", dest="proposed_by")
    c.add_argument("--parent-session-id", default="", dest="parent_session_id")
    c.add_argument("--authorization-receipt", default="", dest="authorization_receipt")

    t = sub.add_parser("transition", help="apply a state transition")
    t.add_argument("job_id")
    t.add_argument("to_state")
    t.add_argument("--actor", required=True)
    t.add_argument("--role", default="AGENT")
    t.add_argument("--reason", default="")

    cl = sub.add_parser("claim", help="claim the lease (locks path scope)")
    cl.add_argument("job_id")
    cl.add_argument("--holder", required=True)
    cl.add_argument("--ttl", type=int, default=900, dest="ttl_seconds")
    cl.add_argument("--role", default="AGENT")

    hb = sub.add_parser("heartbeat", help="extend the lease")
    hb.add_argument("job_id")
    hb.add_argument("--holder", required=True)
    hb.add_argument("--ttl", type=int, default=900, dest="ttl_seconds")

    rl = sub.add_parser("release", help="release the lease")
    rl.add_argument("job_id")
    rl.add_argument("--holder", required=True)
    rl.add_argument("--to", default="QUEUED", dest="to_state")
    rl.add_argument("--reason", default="")

    sh = sub.add_parser("show", help="show one job")
    sh.add_argument("job_id")

    ls = sub.add_parser("list", help="list jobs")
    ls.add_argument("--state", default=None)
    ls.add_argument("--active", action="store_true", help="only active (unexpired leases)")

    sub.add_parser("expire", help="sweep and expire lapsed leases")
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    jp = JobPlane(args.ledger)
    try:
        if args.cmd == "create":
            env = jp.create(
                scope={
                    "repository": args.repo,
                    "base_commit": args.base_commit,
                    "allowed_paths": args.allowed,
                    "forbidden_paths": args.forbidden,
                    "mutation_class": args.mutation_class,
                },
                acceptance_tests=args.acceptance,
                preconditions=args.precondition,
                requested_by=args.requested_by,
                proposed_by=args.proposed_by,
                parent_session_id=args.parent_session_id,
                authorization_receipt=args.authorization_receipt,
            )
            _emit(env)
        elif args.cmd == "transition":
            _emit(jp.transition(args.job_id, args.to_state, actor=args.actor,
                                role=args.role, reason=args.reason))
        elif args.cmd == "claim":
            _emit(jp.claim(args.job_id, holder=args.holder,
                           ttl_seconds=args.ttl_seconds, actor_role=args.role))
        elif args.cmd == "heartbeat":
            _emit(jp.heartbeat(args.job_id, holder=args.holder,
                               ttl_seconds=args.ttl_seconds))
        elif args.cmd == "release":
            _emit(jp.release(args.job_id, holder=args.holder,
                             to_state=args.to_state, reason=args.reason))
        elif args.cmd == "show":
            _emit(jp.get(args.job_id))
        elif args.cmd == "list":
            _emit(jp.list(state=args.state, active_only=args.active))
        elif args.cmd == "expire":
            _emit({"expired": jp.expire_due()})
    except JobPlaneError as e:
        print(f"ERROR [{type(e).__name__}]: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
