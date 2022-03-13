def help(name, zoom):
    # molar_mass; ε, σ
    if name in ["Ne"]:
        return 0.020, 0.0031, 274 / zoom
    if name in ["Ar"]:
        return 0.040, 0.0104, 340 / zoom
    if name in ["Kr"]:
        return 0.0837, 0.0140, 365 / zoom
    if name in ["Xe"]:
        return 0.131, 0.0020, 398 / zoom
