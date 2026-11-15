# %% [markdown]
# # Setup check
#
# Run this once before Day 1. It imports every library the labs use, reads each data file of Sahil Water and fits one small model. Nothing calls or downloads a model; a laptop processor or a Colab CPU runtime is enough.

# %%
import os, sys, subprocess
from pathlib import Path

IN_COLAB = "google.colab" in sys.modules
if IN_COLAB:
    REPO_URL = "https://github.com/SDAIAAcademy/ds-301.git"
    if not Path("/content/ds-301").exists():
        subprocess.run(["git", "clone", "-q", REPO_URL, "/content/ds-301"], check=True)
    os.chdir("/content/ds-301/labs")
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-r", "requirements-colab.txt"], check=True)
else:
    while not Path("sahil.py").exists() and Path.cwd() != Path.cwd().parent:
        os.chdir("..")  # solutions/ notebooks run from labs/
sys.path.insert(0, os.getcwd())

# %%
import importlib
missing = []
for name in ["numpy", "pandas", "scipy", "statsmodels", "sklearn", "matplotlib", "patsy", "marginaleffects"]:
    try:
        m = importlib.import_module(name)
        print(f"✅ {name} {getattr(m, '__version__', '')}")
    except ImportError:
        missing.append(name)
        print(f"❌ {name} is missing")
print("Python", sys.version.split()[0])

# %%
import sahil as U
import statsmodels.formula.api as smf
files = {"bills": U.bills, "districts": U.districts, "segments": U.segments, "weekly leak reports": U.leaks,
         "district leak summary": U.district_leaks, "candidate predictors": U.candidates}
for label, load in files.items():
    print(f"✅ {label}: {len(load())} rows")
fit = smf.ols("log_m3 ~ household_size", data=U.bills()).fit()
print(f"✅ a first fit: {fit.params['household_size']:.3f} on the log scale per person")
U.check(not missing, "every library is installed" if not missing else f"install: {', '.join(missing)}")
