import sys
import os

# Add the neighboring directory to sys.path
sys.path.append(os.path.abspath('../src'))
for path in sys.path:
    print(path)
