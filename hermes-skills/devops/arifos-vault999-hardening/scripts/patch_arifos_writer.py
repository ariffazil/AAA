#!/usr/bin/env python3
"""Hot-patch arifOS tools_internal.py with X-Writer-Token header.
Run inside container: docker cp patch_arifos_writer.py arifosmcp:/tmp/p.py && docker exec arifosmcp python3 /tmp/p.py
"""
target = '/app/arifosmcp/runtime/tools_internal.py'
with open(target) as f:
    c = f.read()

# 1. Add writer_token env read after writer_url
old_url = 'writer_url = os.environ.get("VAULT999_WRITER_URL", "http://vault999-writer:5001")'
new_url = '''writer_url = os.environ.get("VAULT999_WRITER_URL", "http://vault999-writer:5001")
        writer_token = os.environ.get("VAULT_WRITER_TOKEN", "")
        headers = {"Content-Type": "application/json"}
        if writer_token:
            headers["X-Writer-Token"] = writer_token'''

if old_url in c and 'writer_token = os.environ' not in c:
    c = c.replace(old_url, new_url, 1)
    print("Added writer_token + headers")
else:
    print("Already patched or pattern not found")

# 2. Add headers= to the client.post call
old_post = '''response = await client.post(
                    f"{writer_url}/seal",
                    json=payload,
                )'''
new_post = '''response = await client.post(
                    f"{writer_url}/seal",
                    json=payload,
                    headers=headers,
                )'''

if old_post in c and 'headers=headers' not in c:
    c = c.replace(old_post, new_post, 1)
    print("Added headers to client.post")
elif 'headers=headers' in c:
    print("headers already in client.post")

with open(target, 'w') as f:
    f.write(c)

print("Patched OK")
