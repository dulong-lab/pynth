def normalize(a):
    if a.size == 0:
        return a

    return a / max(abs(a.max()), abs(a.min()))


__all__ = ['normalize']
