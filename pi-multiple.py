import subprocess
import sys

children = []
for _ in range(4):
    child = subprocess.Popen([sys.executable, "pi-contributor.py"])
    children.append(child)

for p in children:
    p.wait()

print("C'est fini.")
