rm -rf ./fackel-mas* && rm -rf downloaded_data && rm -rf ./data && rm -rf ./tmp
wget -O downloaded_data --header "PRIVATE-TOKEN: ${GITLAB_TOKEN}" https://gitlab.oeaw.ac.at/api/v4/projects/33/repository/archive?path=fackel/fk_texts/FK
tar -xf downloaded_data && rm downloaded_data
mv fackel-master-* ./tmp
mv tmp/fackel/fk_texts/FK data && rm -rf ./tmp
