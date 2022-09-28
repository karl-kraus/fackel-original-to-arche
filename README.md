# fackel-original-to-arche
working repo to ingest the data of https://fackel.oeaw.ac.at/ into ARCHE


## install & run

* clone the repo
* create a virtual environment and install needed dependencies `pip install -r requirements`

* set an environment variable `$GITLAB_TOKEN` to run `./fetch_data.sh` to download the Fackel files from private gitlab repo 
* run `python extract_md.py` to write some basice Metadata into a csv
* run `python create_arche_md.py` to generate ARCHE-Metadata


(or just let GitHub Actions do all the work)