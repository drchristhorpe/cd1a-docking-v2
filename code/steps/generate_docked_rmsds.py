import json
import toml
import os


config = toml.load('config.toml')

pdb_code = '7ryo'

pdb_pose = f"{config['INPUTS']}/ligands/{pdb_code}_ligand.pdb"


rmsds_dict = {}

for iteration in [i for i in range(0,51)]:

    docked_pose = f"{config['OUTPUTS']}/ligands/docking/{pdb_code}/{pdb_code}_{iteration}.sdf"

    output_filepath = f"{config['TMP']}/docked/{pdb_code}_{iteration}.txt"
    json_filepath = f"{config['OUTPUTS']}/ligands/docking/rmsds/{pdb_code}.json"

    obrms_command = f"obrms --firstonly {pdb_pose} {docked_pose} > {output_filepath}"

    os.system(obrms_command)

    with open(output_filepath, 'r') as rmsds_txt_file:
        raw_rmsds = rmsds_txt_file.read()

    rmsds_dict[iteration] = []

    i = 0
    for line in raw_rmsds.splitlines():
        rmsd = float(line.split(' ')[2])
        rmsds_dict[iteration].append(rmsd)
        i += 1

with open(json_filepath, 'w') as rmsds_json_file:
    json.dump(rmsds_dict, rmsds_json_file)

