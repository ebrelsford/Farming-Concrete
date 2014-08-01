class NoRainfallResultsException(Exception):
    """
    Indicates that there were no rainfall results for a given time and place
    when the request was passed to NOAA.
    """
    pass


class NoStationResultsException(Exception):
    """
    Indicates that there were no station results for a given time and place
    when the request was passed to NOAA.
    """
    pass
