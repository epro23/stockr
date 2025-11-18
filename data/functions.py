def adjust_large_metrics(value):
    """
    Adjust large numerical values in the metrics frames for better readability.
    Converts values >= 1,000,000 to millions (M) and values >= 1,000 to thousands (K).
    """
    if value >= 1e9:
        return f"{value / 1e9:.2f}B"
    elif value >= 1e6:
        return f"{value / 1e6:.2f}M"
    elif value >= 1e3:
        return f"{value / 1e3:.2f}K"
    else:
        return f"{value:.3f}" if isinstance(value, float) else str(value)
    