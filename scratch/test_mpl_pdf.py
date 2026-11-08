import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import re

test_pdf = "test_mpl.pdf"
with PdfPages(test_pdf) as pdf:
    # Page 1
    fig, ax = plt.subplots(figsize=(8.5, 11))
    ax.text(0.5, 0.5, "Page 1: Executive Briefing", ha="center", va="center", fontsize=20)
    ax.axis("off")
    pdf.savefig(fig)
    plt.close()

    # Page 2
    fig, ax = plt.subplots(figsize=(8.5, 11))
    ax.text(0.5, 0.5, "Page 2: Media Plan Details", ha="center", va="center", fontsize=20)
    ax.axis("off")
    pdf.savefig(fig)
    plt.close()

with open(test_pdf, "rb") as f:
    data = f.read()

pages = len(re.findall(rb"/Type\s*/Page\b", data))
print(f"Generated {test_pdf} successfully! Size: {os.path.getsize(test_pdf)} bytes, Page count: {pages}")

