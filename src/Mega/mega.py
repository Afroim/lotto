import random
import math

# Probability table for numbers 1 to 70
probability_table = {
    1: 0.014005602240896359, 2: 0.013725490196078431, 3: 0.01876750700280112, 4: 0.01484593837535014,
    5: 0.012324929971988795, 6: 0.014565826330532213, 7: 0.015406162464985995, 8: 0.017086834733893556,
    9: 0.012605042016806723, 10: 0.018487394957983194, 11: 0.015406162464985995, 12: 0.01288515406162465,
    13: 0.013725490196078431, 14: 0.017366946778711485, 15: 0.017086834733893556, 16: 0.014285714285714285,
    17: 0.017927170868347338, 18: 0.01568627450980392, 19: 0.015126050420168067, 20: 0.015966386554621848,
    21: 0.012324929971988795, 22: 0.015126050420168067, 23: 0.012324929971988795, 24: 0.01484593837535014,
    25: 0.01484593837535014, 26: 0.015126050420168067, 27: 0.013725490196078431, 28: 0.014005602240896359,
    29: 0.015966386554621848, 30: 0.014565826330532213, 31: 0.017927170868347338, 32: 0.013445378151260505,
    33: 0.015406162464985995, 34: 0.013445378151260505, 35: 0.011484593837535015, 36: 0.012044817927170869,
    37: 0.013725490196078431, 38: 0.016246498599439777, 39: 0.012605042016806723, 40: 0.014565826330532213,
    41: 0.012324929971988795, 42: 0.015406162464985995, 43: 0.015406162464985995, 44: 0.01568627450980392,
    45: 0.012605042016806723, 46: 0.017086834733893556, 47: 0.012605042016806723, 48: 0.014005602240896359,
    49: 0.010084033613445379, 50: 0.011764705882352941, 51: 0.010364145658263305, 52: 0.013165266106442577,
    53: 0.015126050420168067, 54: 0.01288515406162465, 55: 0.011484593837535015, 56: 0.013165266106442577,
    57: 0.013725490196078431, 58: 0.015406162464985995, 59: 0.01484593837535014, 60: 0.012324929971988795,
    61: 0.015406162464985995, 62: 0.015126050420168067, 63: 0.012605042016806723, 64: 0.017086834733893556,
    65: 0.010924369747899159, 66: 0.01568627450980392, 67: 0.012605042016806723, 68: 0.01288515406162465,
    69: 0.012605042016806723, 70: 0.014285714285714285
}

# Extract numbers and corresponding probabilities
numbers = list(range(1,71))
probabilities = list(probability_table.values())

# Initialize variables to hold combinations and a set of seen numbers
combinations = []
seen_numbers = set()

# Function to calculate the information measure of a combination
def info_meas(comb):
    return -sum(math.log2(probability_table[num]) for num in comb)

weighted_numbers = []
for num, prob in probability_table.items():
    weighted_numbers.extend([num] * int(prob * 10000))
# Generate and store combinations until the union of all combinations contains all numbers from 1 to 70
pot_size = 2000
sz = 600
while len(seen_numbers) < 70:
    # Generate a list of potential combinatio
		potential_combos = [random.sample(weighted_numbers, k=5) for _ in range(pot_size)]
		un_combos = [combo for combo in potential_combos  if len(combo) == len(set(combo))]
		un_combos.sort(key=info_meas)
		un_combos = un_combos[0:sz]
		cret = lambda com: (len(set(com) - seen_numbers))
		un_combos.sort(key=cret, reverse=True )

    # Select the combination that adds the most new numbers with the minimum information measure
		best_combo = un_combos[0]
		combinations.append(best_combo)
		seen_numbers.update(best_combo)

# Print the generated combinations with their information measures
#combinations.sort(key=info_meas)
#print(combinations)
for i, combo in enumerate(combinations, 1):
    combo_str = ', '.join(map(str, sorted(combo)))
    info_measure = info_meas(combo)
    print(f"{i}, {combo_str} , {info_measure:.4f}")

print(f"\nMinimal number of combinations generated: {len(combinations)}")