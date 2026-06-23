def calculate_tax(gross):
    brackets = [
        (0, 2000, 0.0),       # 0% for income 0-2000
        (2000, 4000, 0.15),   # 15% for income 2000-4000
        (4000, 7000, 0.20),   # 20% for income 4000-7000
        (7000, 10000, 0.25),  # 25% for income 7000-10000
        (10000, 14000, 0.30), # 30% for income 10000-14000
        (14000, float('inf'), 0.35) # 35% for income above 14000
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
