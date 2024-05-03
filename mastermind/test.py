import itertools

# Example input data
colours = [1, 2]
code_length = 2

# Calculate the Cartesian product using itertools.product
cartesian_product = itertools.product(colours, repeat=code_length)

# Convert the result to a list of lists
result_list = [list(item) for item in cartesian_product]

# Test code
items_and_scores = {}


# Adding items and their scores
items_and_scores[(1,0)] = 10
items_and_scores[(2,0)] = 20
items_and_scores[(2,1)] = 15

#print(items_and_scores)
#if (2,3) not in items_and_scores: print(True)
items_and_scores[(1,0)] += 1
#print(items_and_scores[(1,0)])


def sublist_with_most_variety(list_of_lists):
    max_variety_count = 0
    sublist_with_max_variety = None

    for sublist in list_of_lists:
        variety_count = len(set(sublist))
        if variety_count > max_variety_count:
            max_variety_count = variety_count
            sublist_with_max_variety = sublist

    return sublist_with_max_variety

# Example usage:
my_list = [[1, 2, 3, 4], [1, 2, 3], [1, 2, 2, 3, 3, 4], [1, 2, 4, 4, 4, 4]]
result = sublist_with_most_variety(my_list)
print("Sublist with most variety:", result)

