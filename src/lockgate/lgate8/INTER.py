def inter(n, x, y, x1):
    """
    Interpolates linearly between the points in the table.
    
    Parameters:
    - n: number of values in the table
    - x: array with x-values
    - y: array with y-values
    - x1: x for which the function value is sought
    
    Returns:
    - y1: y(x1)
    """

    j = 0
    for i in range(1, n + 1):
        if x1 > x[i - 1]:
            j = i

    if j <= 0:
        y1 = y[0]
    elif j >= n:
        y1 = y[n - 1]
    else:
        y1 = (y[j - 1] * (x[j] - x1) + y[j] * (x1 - x[j - 1])) / (x[j] - x[j - 1])

    return y1

if __name__ == "__main__":
    # Example usage:
    n_values = 5
    x_values = [1.0, 2.0, 3.0, 4.0, 5.0]
    y_values = [10.0, 20.0, 15.0, 25.0, 30.0]
    x_example = 2.5

    result = interpolate(n_values, x_values, y_values, x_example)
    print(f"The interpolated value at x = {x_example} is y = {result}")
