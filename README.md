# Practice-earthquake-library

# Data availabilty

Data of global GNSS network are available at https://simurg.space, ionosonde data availabel through https://giro.uml.edu. The data paper uses along with notebook (with outputs preserved) are available here https://cloud.iszf.irk.ru/index.php/s/3RcnGdohf38kmAO.

# Prepare environment

Load anaconda to make sure we are on the same page.

https://docs.conda.io/en/latest/

In anaconda propmt (or in linux bash):

```bash
conda deactivate
conda create -n turkey_eq python=3.10
conda activate turkey_eq
```

# Install requirements
```
pip install poetry
poetry install
```

Or using pip:
```
pip install requests
pip install h5py
pip install numpy
pip install matplotlib
pip install scipy
pip install cartopy
```
