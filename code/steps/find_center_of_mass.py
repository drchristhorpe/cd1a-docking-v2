from pymol import cmd


def find_center_of_mass(pdb_code:str):
    histo_abd_url = f"https://coordinates.histo.fyi/structures/downloads/class_i/without_solvent/{pdb_code}_1_abd.cif"


    cmd.load(histo_abd_url)
    
    
    labels = ['x','y','z']

    center_of_mass = {k:v for k,v in zip(labels,com)}
    print (center_of_mass)


find_center_of_mass('1onq')