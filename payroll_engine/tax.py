def calculate_tax(gross):
    brackets = [
        (0, 2000, 0.0),
        (2001, 4000, 0.15),
        (4001, 7000, 0.20),
        (7001, 10000, 0.25),
        (10001, 14000, 0.30),
        (14001, float('inf'), 0.35)
    ]
    tax = 0.0
    for lower, upper, rate in brackets:
        if gross > lower:
            taxable = min(gross, upper) - lower
            if taxable > 0:
                tax += taxable * rate
        else:
            break
    return tax