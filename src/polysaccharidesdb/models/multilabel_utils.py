"""Helpers for robust multilabel prediction decoding."""

from __future__ import annotations

import numpy as np


def ensure_2d_binary_predictions(y_pred_bin, num_labels: int | None = None):
    array = np.asarray(y_pred_bin)
    if array.ndim == 1:
        if num_labels is not None and num_labels > 0 and array.size % num_labels == 0:
            array = array.reshape(-1, num_labels)
        else:
            array = array.reshape(1, -1)
    return array
