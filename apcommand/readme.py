
# python standard library
import subprocess

print(subprocess.check_output('atheros -h'.split()))

print(subprocess.check_output('broadcom -h'.split()))