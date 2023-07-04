import json


pdb_code = ''
pdb_pose = f""


rmsds_dict = {}
rmsds = []


cross_docked_pose = f""
output_filepath = f""


obrms_command = f'obrms --firstonly {pdb_pose} {cross_docked_pose} > {output_filepath}'

with open(output_filepath, 'r') as rmsds_txt_file:
    raw_rmsds = rmsds_txt_file.read()

for line in raw_rmsds.splitlines():
    rmsd = float(line.split(': ')[1])
    rmsds_dict['rmsds'][str(i)] = rmsd
    rmsds.append(rmsd)
    i += 1

json_output_filepath = f'{this_filepath}/{pdb_code}_rmsds.json'
with open(json_output_filepath, 'w') as rmsds_json_file:
    json.dump(rmsds_dict, rmsds_json_file)