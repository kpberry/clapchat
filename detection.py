import numpy as np


def has_clap(data: np.ndarray, window_size: int, threshold: float):
    sums = np.cumsum(np.abs(data))
    moving_averages = (sums[window_size:] - sums[:-window_size]) / window_size
    return np.any(moving_averages > threshold)
