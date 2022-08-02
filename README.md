# VISUALISATIONS OF THE DATA IN THE KATABASE PROJECT

## Presentation
A bunch of scripts / tools for the visualisation of data available at the end of 
step 4 `TaggedData`. Some of the visualisations were originally created for the 
website, others were made just to make sense of the data. Finally, a few scripts
and visualisations were made for a [master's thesis](https://github.com/paulhectork/tnah2022_memoire).

---

## Directory structure
- `in/` : input directory (`json` and `xml` files)
- `out/` : output directory (png figures and a json file)
- `utils/` : useful tools to build the scripts: data preparation and such
- all `*.py` scripts at root are used to make scripts.

---

## How to
The only `__main__` scripts (that can be run directly) are in the root.
```shell
python3 -m venv env  # create environment
source env/bin/activate  # source the proper env
pip install -r requirements.txt  # install libs
python teinametypes.py  # create 1 fig classifying different types of tei:names
python figmaker.py  # create a lot of other scripts
```

---

## Credits
All scripts developped by Paul Kervegan in april-september 2022, except for
`utils/reconciliator.py` and `utils/conversion_tables.py`, developped by A. Bartz. 
Data used was created by different members of the Katabase project. 
Available under GNU GPL v3.

have fun !
