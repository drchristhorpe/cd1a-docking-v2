from typing import Dict
from pathlib import Path

import os

split_token = '$$$$'

def generate_conformers(pdb_code:str, config:Dict):
    output_directory = f"{config['OUTPUTS']}/ligands/conformers/{pdb_code}"

    Path(output_directory).mkdir(parents=True, exist_ok=True)
    conformers_filename = f"{output_directory}/{pdb_code}_{config['CONFORMER_COUNT']}_conformers.sdf"

    obabel_command = f"obabel {config['INPUTS']}/ligands/{pdb_code}_ligand.pdb -O {conformers_filename} --conformer --nconf {config['CONFORMER_COUNT']} --score rmsd --writeconformers"
    print (pdb_code)
    print (config)
    print (obabel_command)    

    os.system(obabel_command)

    with open(conformers_filename, 'r') as file:
        sdf_file = file.read()

    conformers = sdf_file.split(f'{split_token}\n')

    i = 0
    for conformer in conformers:
        conformer = conformer + split_token

        conformer_filename = f"{config['OUTPUTS']}/ligands/conformers/{pdb_code}/{pdb_code}_{i}.sdf"
        with open(conformer_filename, 'w') as file:
            file.write(conformer)

        i += 1

