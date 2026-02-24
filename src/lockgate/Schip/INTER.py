def inter(n, x, y, x1):
    """
    Interpoleert linear tussen de punten in de tabel.
    Als x1 < x[0] dan y1 = x[1]; als x1 > x[n] dan y1=x[n] linear interpolation between the points in the table.
    De tabel moet stijgend zijn
    n: aantal waardes in de tabel
    x[n]: lijst van x-waardes (tijd)
    y[n]: lijst van y-waardes (golfhoogte)
    x1: x waarvoor de functie waarde gezocht wordt
    y1: bevat de return y[x1] uit

    Args:
    - n: number of values in the table (int)
    - x: list of x-values (list of floats)
    - y: list of y-values (list of floats)
    - x1: x-value for which y-value is to be interpolated (float)

    Returns:
    - y1: interpolated y-value (float)
    """

    # Initialize j
    j = 0
    
    for i in range(0,n):
        if x1 > x[i]:
            j = i
    
    if j <= 0:
        y1 = y[0]

    elif j >= n - 1:
        y1 = y[n - 1]

    else:
        y1 = (y[j] * (x[j+1] - x1) + y[j+1] * (x1 - x[j])) / (x[j+1] - x[j])

    return y1