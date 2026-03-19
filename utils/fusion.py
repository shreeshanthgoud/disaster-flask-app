import numpy as np

def fuse_risk(weather, cnn, nlp):

    scores = np.array([weather, cnn, nlp])

    total = np.sum(scores)

    if total == 0:
        return 0.33, 0.33, 0.33, 0.33

    w = scores / total

    final = np.sum(scores * w)

    return final, w[0], w[1], w[2]


def risk_level(score):

    if score < 0.33:
        return "Low"
    elif score < 0.66:
        return "Medium"
    else:
        return "High"