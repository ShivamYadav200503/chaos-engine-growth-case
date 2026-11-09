import re
from pathlib import Path

with open('src/06_compile_pdfs_and_package.py', 'r', encoding='utf-8') as f:
    text = f.read()

matches = re.findall(r'FIGS_DIR\s*/\s*[\'"]([^\'"]+)[\'"]', text)
print('Figures referenced in 06_compile_pdfs_and_package.py:', set(matches))

with open('submission/appendix.md', 'r', encoding='utf-8') as f:
    app_text = f.read()
matches_app = re.findall(r'figures/([a-zA-Z0-9_\.]+\.png)', app_text)
print('Figures referenced in submission/appendix.md:', set(matches_app))

