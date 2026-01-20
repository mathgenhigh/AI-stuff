import numpy as np 

# Membershio function

def triangular(x, a, b, c):
    if x <= a or x >= c:
        return 0.0
    elif a < x <= b:
        return (x - a) / (b - a)
    elif b < x < c:
        return (c - x) / (c - b)


# Fuzzification

def fuzzify_temperature(temp):
    return {
        "low": triangular(temp, 0, 0, 20),
        "medium": triangular(temp, 15, 25, 30),
        "high": triangular(temp, 25, 40, 40)
    }

def fuzzify_humidity(hum):
    return {
        "low": triangular(hum, 0, 0, 40),
        "medium": triangular(hum, 30, 50, 70),
        "high": triangular(hum, 60, 100, 100)
    }


# Rule base

def apply_rules(temp_fuzzy: dict, hum_fuzzy: dict) -> list:
    rules = []

    # Rule 1: IF temp low AND humidity low -> fan = slow
    rules.append(("slow", min(temp_fuzzy["low"], hum_fuzzy["low"])))

    # Rule 2: IF temp low AND humidity high -> fan = medium
    rules.append(("medium", min(temp_fuzzy["low"], hum_fuzzy["high"])))

    # Rule 3: IF temp medium AND humidity low -> fan = medium
    rules.append(("medium", min(temp_fuzzy["medium"], hum_fuzzy["low"])))

    # Rule 4: IF temp medium AND humidity medium -> fan = medium
    rules.append(("medium", min(temp_fuzzy["medium"], hum_fuzzy["medium"])))

    # Rule 5: IF temp high AND humidity medium -> fan = fast
    rules.append(("fast", min(temp_fuzzy["high"], hum_fuzzy["medium"])))

    # Rule 6: IF temp high AND humidity high -> fan = fast
    rules.append(("fast", min(temp_fuzzy["high"], hum_fuzzy["high"])))

    return rules


# Defuzzification (centroid)

def defuzzify(rules: list) -> float:
    fan_values = {
        "slow": 20,
        "medium": 50,
        "fast": 80
    }

    numerator = 0.0
    denominator = 0.0

    for label, strength in rules:
        numerator += fan_values[label] * strength
        denominator += strength

    if denominator == 0:
        return 0.0
    
    return numerator / denominator


# Full fuzzy controler

def fuzzy_controler(tempeature, humidity):
    temp_fuzzy = fuzzify_temperature(tempeature)
    hum_fuzzy = fuzzify_humidity(humidity)

    rules = apply_rules(temp_fuzzy, hum_fuzzy)
    output = defuzzify(rules)

    return output


# Test cases

if __name__ == "__main__":
    test_cases = [
        (18, 30),    # cold & dry
        (32, 75),     # hot & humid
    ]

    for temp, hum in test_cases:
        fan_speed = fuzzy_controler(temp, hum)
        print(f"Temperature: {temp}C, Humidity: {hum}% -> Fan Speed: {fan_speed:.2f}%")