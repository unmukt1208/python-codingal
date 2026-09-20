
og_list = [-2, 5, 1, -4, 3]
def find_cube(og_list):
    return og_list**3
cubed_list = list(map(find_cube, og_list))
print(cubed_list)
paired = list(zip(og_list, cubed_list))
print(paired)
for i in cubed_list:
    if i == -64:
        exit()
    print(i)