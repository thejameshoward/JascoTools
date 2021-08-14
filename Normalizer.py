import pandas as pd


def Normalizer(JascoScanFile, normalization_value, wavelength_to_normalize):
    '''

    Parameters
    ----------
    JascoScanFile : JascoScanFile
        DESCRIPTION.
    normalization_value : float
        DESCRIPTION.
    wavelength_to_normalize : float
        DESCRIPTION.

    Returns
    -------
    norm_CD : dictionary
        wavelength:CD (mDeg) dictionary for plotting with Plot

    '''
    f = JascoScanFile
    wavelength_to_normalize = float(wavelength_to_normalize)

    wl = f.get_wavelengths()
    cd = f.get_CD().values()
    absorbance = f.get_abs().values()

    df = pd.DataFrame()
    df["WL"] = wl
    df["CD"] = cd
    df["ABS"] = absorbance

    df = df.set_index("WL")

    norm_result = float(normalization_value) / df["ABS"][wavelength_to_normalize]

    df_norm = df * norm_result

    normalized_cd = pd.Series(df_norm.CD.values, index=df_norm.index).to_dict()
    normalized_absorbance = pd.Series(df_norm.ABS.values, index=df_norm.index).to_dict()

    return normalized_cd, normalized_absorbance
