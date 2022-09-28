
#!/bin/bash

echo "install and update php things"
composer require "acdh-oeaw/arche-ingest:^1"

echo "build ARCHE-MD RDFs"
python create_arche_md.py

echo "ingest ARCHE-CONSTANTS"
vendor/bin/arche-import-metadata out/arche.ttl http://127.0.0.1/api username password --retriesOnConflict 25


# echo "ingest facs-res"
# vendor/bin/arche-import-metadata html/arche-facs.rdf http://127.0.0.1/api username password --retriesOnConflict 25