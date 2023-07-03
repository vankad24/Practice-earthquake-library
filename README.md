# Practice-earthquake-library
# Usage

This notebook is distributed using MIT licence

    MIT License

    Copyright (c) [2023] [Artem Vesnin]

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.

# Data availabilty

Data of global GNSS network are available at https://simurg.space, ionosonde data availabel through https://giro.uml.edu. The data paper uses along with notebook (with outputs preserved) are available here https://cloud.iszf.irk.ru/index.php/s/3RcnGdohf38kmAO .  Email artem_vesnin@iszf.irk.ru if you have any questions about data format or behaviour of particular piece of code.

# Prepare environment

Load anaconda to make sure we are on the same page.

https://docs.conda.io/en/latest/

In anaconda propmt (or in linux bash):

```bash
conda deactivate
conda create -n turkey_eq python=3.10
conda activate turkey_eq
conda install jupyterlab
conda install cartopy
jupyter-notebook
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