import os
import toml


config = toml.load('config.toml')

cross_pdb_code = '1onq'
pdb_code = '7sh4'


centre_of_mass = [-41.0528, 56.426, 63.1335]
bounding_box_xyz = [20, 20, 10]

exhaustiveness = 25

mobile_sidechains = [14,70,77,78,98,144]

for iteration in [i for i in range(0,51)]:

    receptor_filepath = f"{config['INPUTS']}/cd1a/{cross_pdb_code}_cd1a.pdb"
    ligand_filepath = f"{config['OUTPUTS']}/ligands/conformers/{pdb_code}/{pdb_code}_{iteration}.sdf"
    output_filepath = f"{config['OUTPUTS']}/ligands/cross_docking/{pdb_code}/{pdb_code}_{cross_pdb_code}_{iteration}.sdf"


    gnina_command = f"{config['GNINA_PATH']}/gnina"
    gnina_command += f" --receptor {receptor_filepath}"
    gnina_command += f" --ligand {ligand_filepath}"
    gnina_command += f" --exhaustiveness {exhaustiveness}"
    gnina_command += f" --out {output_filepath}"

    gnina_command += f" --center_x {centre_of_mass[0]}"
    gnina_command += f" --center_y {centre_of_mass[1]}"
    gnina_command += f" --center_z {centre_of_mass[2]}"
    gnina_command += f" --size_x {bounding_box_xyz[0]}"
    gnina_command += f" --size_y {bounding_box_xyz[1]}"
    gnina_command += f" --size_z {bounding_box_xyz[2]}"

    os.system(gnina_command)