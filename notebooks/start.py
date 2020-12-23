
organization = "IngEurCDaaS01"
project = "IngOne"

f"GET https://dev.azure.com/{organization}/{project}/_apis/git/repositories?api-version=6.1-preview.1"


import json
import subprocess

# az boards work-item create --title "Test from tim's command line" --type "User Story" 


process = subprocess.run(["az", "repos", "list"],
                         stdin=subprocess.PIPE, 
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         universal_newlines=True,
                         shell=False)

process.stdout

['az boards work-item create',
                          '--title \"Test from tims python script\"',
                          '--type \"User Story\"',
                          '--area \"IngOne\P01908-Default\example_repo\"'
                          ]