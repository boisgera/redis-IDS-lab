import os
import platform

pid = os.getpid()
name = platform.node()

print(pid)
print(name)

print(f"{name}-{pid}")