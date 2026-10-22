from numpy import inf, isfinite, nan, ndarray, sqrt, sum


def _cen_and_std(
    val: ndarray,
    unc: ndarray,
) -> tuple[float, float]:
    """
    Calculate the central value and standard deviation from a value and 
    uncertainty array.

    The central value is always taken as the first element of the `val` array. 
    If any subsequent elements are finite, the standard deviation is calculated 
    from these. Otherwise, the uncertainty associated with the central value is 
    used. 
    """
    cen = val[0]
    arr = val[1:]
    std = _std(arr, cen=cen) if isfinite(arr).any() else unc[0]

    return cen, std


def _std(arr: ndarray, cen: float | None = None) -> float:
    """
    Calculate the standard deviation of an array. 

    Non-finite values are ignored. If not `cen` value is given, the mean of the 
    finite values is used as the center and `ddof` is increased to 1 from 0. If 
    the number o finite values is equal to `ddof`, inf is returned. Otherwise, 
    the standard deviation is calculated normally:

    ```
    std = sqrt(sum((x - cen) ** 2) / n)
    ```
    """
    mask = isfinite(arr)
    if not mask.any():
        return nan

    arr = arr[mask]
    n = arr.size
    if cen is None:
        cen = arr.mean()
        n -= 1

    if n == 0:
        return inf

    return sqrt(sum((arr - cen) ** 2) / n)
