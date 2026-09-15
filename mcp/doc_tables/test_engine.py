import sys
sys.path.insert(0, "/root/AAA/mcp/doc_tables")
import server as S

def brief(tag, res):
    print(f"{tag}: table_count={res['table_count']}", end="")
    if res["tables"]:
        t = res["tables"][0]
        print(f" | best {t['shape']} strategy={t['strategy']} score={t['score']}")
    else:
        print(" | (no tables — honest empty)")

print("### A. cafib p397 slotting, must be 2x5 with 70/90/115/250/400")
r = S.extract_any("/tmp/cafib.pdf", page=397, min_rows=2, min_cols=2)
brief("A", r); print(r["tables"][0]["markdown"])

print("\n### B. cafib p425 reconcile")
r = S.extract_any("/tmp/cafib.pdf", page=425, min_rows=2, min_cols=2)
brief("B", r)
for i, t in enumerate(r["tables"]):
    print(f"   t{i} -> {S.reconcile_table(t['cells'])['verdict']}")

print("\n### C. sa2024 p36 musyarakah/mudarabah ruled table")
r = S.extract_any("/tmp/sa2024.pdf", page=36, min_rows=2, min_cols=2)
brief("C", r)

print("\n### D. sa2024 p1 TOC (borderless fallback must still work)")
r = S.extract_any("/tmp/sa2024.pdf", page=1, min_rows=2, min_cols=2)
brief("D", r)

print("\n### E. sa2024 p3/p4 narrative pages (must NOT return prose as tables)")
r = S.extract_any("/tmp/sa2024.pdf", page_range=(3, 4), min_rows=2, min_cols=2)
brief("E", r)

print("\n### F. HTML")
r = S.extract_any("/tmp/t.html")
brief("F", r)
print("   ", S.reconcile_table(r["tables"][0]["cells"])["verdict"])
