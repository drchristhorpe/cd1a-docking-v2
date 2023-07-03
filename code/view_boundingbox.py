from typing import List


def load_mhc_abd(pdb_code:str):
    abd_id = f"{pdb_code}_1_abd"
    histo_abd_url = f"https://coordinates.histo.fyi/structures/downloads/class_i/without_solvent/{abd_id}.cif"
    cmd.load(histo_abd_url)
    cmd.color('green', abd_id)


def calculate_centre_of_mass(canonical=False):
    if canonical:
        load_mhc_abd('1hhk')
    com = [round(coord, 4) for coord in cmd.centerofmass()]
    if canonical:
        cmd.delete('1hhk_1_abd')
    return com


def display_centre_of_mass(com:List, canonical=False):
    if canonical:
        pseudoatom_name = 'ccom'
    else:
        pseudoatom_name = 'com'
    cmd.pseudoatom(pseudoatom_name, pos=com)
    cmd.show('spheres',pseudoatom_name)
    if canonical:
        cmd.color('white',pseudoatom_name)
    else:
        cmd.color('gray50',pseudoatom_name)


def display_cleft_bounding_box(com:List, show_spheres=False):

    xyz = [20, 20, 10]

    #TODO automate all of this
    # combinations, this and the bonding feels automateable
    """
        ---
        -+-
        +--
        --+
        ++-
        -++
        +-+
        +++
    """

    lower_right_a1 = [(com[0] - xyz[0]), (com[1] - xyz[1]), (com[2] - xyz[2])]
    upper_right_a1 = [(com[0] - xyz[0]), (com[1] + xyz[1]), (com[2] - xyz[2])]
    lower_left_a1 = [(com[0] + xyz[0]), (com[1] - xyz[1]), (com[2] - xyz[2])]
    upper_left_a1 = [(com[0] + xyz[0]), (com[1] + xyz[1]), (com[2] - xyz[2])]


    lower_right_a2 = [(com[0] - xyz[0]), (com[1] - xyz[1]), (com[2] + xyz[2])]
    upper_right_a2 = [(com[0] - xyz[0]), (com[1] + xyz[1]), (com[2] + xyz[2])]
    lower_left_a2 = [(com[0] + xyz[0]), (com[1] - xyz[1]), (com[2] + xyz[2])]
    upper_left_a2 = [(com[0] + xyz[0]), (com[1] + xyz[1]), (com[2] + xyz[2])]

    cmd.pseudoatom('box', pos=lower_right_a1, name='LRA1')
    cmd.pseudoatom('box', pos=upper_right_a1, name='URA1')
    cmd.pseudoatom('box', pos=lower_left_a1, name='LLA1')
    cmd.pseudoatom('box', pos=upper_left_a1, name='ULA1')
    cmd.pseudoatom('box', pos=lower_right_a2, name='LRA2')
    cmd.pseudoatom('box', pos=upper_right_a2, name='URA2')
    cmd.pseudoatom('box', pos=lower_left_a2, name='LLA2')
    cmd.pseudoatom('box', pos=upper_left_a2, name='ULA2')

    if show_spheres:
        cmd.show('spheres','box')
    cmd.color('gray70','box')

    cmd.bond("box////LRA1", "box////LLA1")
    cmd.bond("box////LLA1", "box////LLA2")
    cmd.bond("box////LLA2", "box////LRA2")
    cmd.bond("box////LRA2", "box////LRA1")

    cmd.bond("box////URA1", "box////ULA1")
    cmd.bond("box////ULA1", "box////ULA2")
    cmd.bond("box////ULA2", "box////URA2")
    cmd.bond("box////URA2", "box////URA1")

    cmd.bond("box////URA1", "box////LRA1")
    cmd.bond("box////ULA1", "box////LLA1")
    cmd.bond("box////URA2", "box////LRA2")
    cmd.bond("box////ULA2", "box////LLA2")

def build_plane(plane:str, corners:List):
    plane_colours = {
        'x':'cyan',
        'y':'magenta',
        'z':'orange'
    }

    plane_name = f"{plane}_plane"

    cmd.pseudoatom(plane_name, pos=corners[0], name='1')
    cmd.pseudoatom(plane_name, pos=corners[1], name='2')
    cmd.pseudoatom(plane_name, pos=corners[2], name='3')
    cmd.pseudoatom(plane_name, pos=corners[3], name='4')

    cmd.bond(f"{plane_name}////1", f"{plane_name}////2")
    cmd.bond(f"{plane_name}////1", f"{plane_name}////3")
    cmd.bond(f"{plane_name}////2", f"{plane_name}////4")
    cmd.bond(f"{plane_name}////3", f"{plane_name}////4")
    cmd.color(plane_colours[plane], plane_name)


    
def display_reference_planes(com:List):
    xyz = [27, 30, 25]

    y_offset = 5

    x1 = [(com[0]) - xyz[0], (com[1] - y_offset), com[2] - xyz[2] ]
    x2 = [(com[0]) + xyz[0], (com[1] - y_offset), com[2] - xyz[2] ]
    x3 = [(com[0]) - xyz[0], (com[1] - y_offset), com[2] + xyz[2] ]
    x4 = [(com[0]) + xyz[0], (com[1] - y_offset), com[2] + xyz[2] ]
    
    build_plane('x', [x1,x2,x3,x4])

    y1 = [(com[0]) - xyz[0], (com[1] - y_offset), com[2]]
    y2 = [(com[0]) + xyz[0], (com[1] - y_offset), com[2]]
    y3 = [(com[0]) - xyz[0], (com[1] - y_offset + xyz[1]), com[2]]
    y4 = [(com[0]) + xyz[0], (com[1] - y_offset + xyz[1]), com[2]]
    
    build_plane('y', [y1,y2,y3,y4])

    z1 = [(com[0]), (com[1] - y_offset), (com[2] - xyz[2])]
    z2 = [(com[0]), (com[1] - y_offset), (com[2] + xyz[2])]
    z3 = [(com[0]), (com[1] - y_offset + xyz[1]), (com[2]- xyz[2])]
    z4 = [(com[0]), (com[1] - y_offset + xyz[1]), (com[2] + xyz[2])]

    build_plane('z', [z1,z2,z3,z4])

    v1 = [(com[0]), (com[1] - y_offset), com[2] ]
    v2 = [(com[0]), (com[1] - y_offset + xyz[1]), com[2] ]

    cmd.pseudoatom('vertical', pos=v1, name='1')
    cmd.pseudoatom('vertical', pos=v2, name='2')
    cmd.bond("vertical////1", "vertical////2")
    cmd.color('white','vertical')
    pass


def load_ligand(pdb_code:str):
    cmd.load(f"../inputs/ligands/{pdb_code}_ligand.pdb")


pdb_codes = [
    '1onq',
    '1xz0',
    '4x6c',
    '4x6d_1',
    '4x6d_2',
    '4x6e',
    '4x6f',
    '5j1a',
    '6nux',
    '7koz',
    '7kp0',
    '7kp1',
    '7ryn',
    '7ryo',
    '7sh4'
]


def main():

    pdb_code = '1onq'

    
    ccom = calculate_centre_of_mass(canonical=True)

    load_mhc_abd(pdb_code)

    com = calculate_centre_of_mass()

    display_centre_of_mass(ccom, canonical=True)

    display_centre_of_mass(com)

    display_cleft_bounding_box(ccom)

    display_reference_planes(ccom)

    for pdb_code in pdb_codes:

        load_ligand(pdb_code)

    #cmd.load(f"../inputs/cd1a/1onq_cd1a.pdb")
    #cmd.remove('1onq_1_abd')
    cmd.reset()

    print (com)

main()