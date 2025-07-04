def get_classic_coordinates() -> dict[str, tuple[float, float]]:
    """Return classic periodic table coordinates for each element.

    The returned dictionary maps each element symbol (e.g., "H", "Fe", "U")
    to a tuple of (x, y) coordinates, where:
        - x is the column position on the periodic table.
        - y is the row position on the periodic table.
    """
    element_coords = {
        "H": (1, 9),
        "He": (18, 9),
        "Li": (1, 8),
        "Be": (2, 8),
        "B": (13, 8),
        "C": (14, 8),
        "N": (15, 8),
        "O": (16, 8),
        "F": (17, 8),
        "Ne": (18, 8),
        "Na": (1, 7),
        "Mg": (2, 7),
        "Al": (13, 7),
        "Si": (14, 7),
        "P": (15, 7),
        "S": (16, 7),
        "Cl": (17, 7),
        "Ar": (18, 7),
        "K": (1, 6),
        "Ca": (2, 6),
        "Sc": (3, 6),
        "Ti": (4, 6),
        "V": (5, 6),
        "Cr": (6, 6),
        "Mn": (7, 6),
        "Fe": (8, 6),
        "Co": (9, 6),
        "Ni": (10, 6),
        "Cu": (11, 6),
        "Zn": (12, 6),
        "Ga": (13, 6),
        "Ge": (14, 6),
        "As": (15, 6),
        "Se": (16, 6),
        "Br": (17, 6),
        "Kr": (18, 6),
        "Rb": (1, 5),
        "Sr": (2, 5),
        "Y": (3, 5),
        "Zr": (4, 5),
        "Nb": (5, 5),
        "Mo": (6, 5),
        "Tc": (7, 5),
        "Ru": (8, 5),
        "Rh": (9, 5),
        "Pd": (10, 5),
        "Ag": (11, 5),
        "Cd": (12, 5),
        "In": (13, 5),
        "Sn": (14, 5),
        "Sb": (15, 5),
        "Te": (16, 5),
        "I": (17, 5),
        "Xe": (18, 5),
        "Cs": (1, 4),
        "Ba": (2, 4),
        "La": (3, 2.5),
        "Ce": (4, 2.5),
        "Pr": (5, 2.5),
        "Nd": (6, 2.5),
        "Pm": (7, 2.5),
        "Sm": (8, 2.5),
        "Eu": (9, 2.5),
        "Gd": (10, 2.5),
        "Tb": (11, 2.5),
        "Dy": (12, 2.5),
        "Ho": (13, 2.5),
        "Er": (14, 2.5),
        "Tm": (15, 2.5),
        "Yb": (16, 2.5),
        "Lu": (17, 2.5),
        "Hf": (4, 4),
        "Ta": (5, 4),
        "W": (6, 4),
        "Re": (7, 4),
        "Os": (8, 4),
        "Ir": (9, 4),
        "Pt": (10, 4),
        "Au": (11, 4),
        "Hg": (12, 4),
        "Tl": (13, 4),
        "Pb": (14, 4),
        "Bi": (15, 4),
        "Po": (16, 4),
        "At": (17, 4),
        "Rn": (18, 4),
        "Ac": (3, 1.5),
        "Th": (4, 1.5),
        "Pa": (5, 1.5),
        "U": (6, 1.5),
        "Np": (7, 1.5),
        "Pu": (8, 1.5),
        "Am": (9, 1.5),
        "Cm": (10, 1.5),
        "Bk": (11, 1.5),
        "Cf": (12, 1.5),
        "Es": (13, 1.5),
        "Fm": (14, 1.5),
        "Md": (15, 1.5),
        "No": (16, 1.5),
        "Lr": (17, 1.5),
    }
    return element_coords


def get_special_coordinates() -> dict[str, tuple[float, float]]:
    """Return special coordinates for lanthanide and actinide
    placeholders.

    Symbols with a tuple (x, y), that marks their positions

    These are not real elements but symbols ("*", "**", etc.) used in
    periodic table plots to indicate where the lanthanide and actinide
    series are referenced from the main table.
    """
    special_coords = {
        " * ": (3, 4.1),
        " ** ": (3, 3.7),
        "*": (2, 2.4),
        "**": (2, 1.4),
    }
    return special_coords
