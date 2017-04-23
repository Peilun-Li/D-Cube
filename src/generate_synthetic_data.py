# generate 3D synthetic data
import random

def add_block(syn_data, start_coords, block_size, density):
    for i in range(start_coords[0], start_coords[0]+block_size[0]):
        for j in range(start_coords[1], start_coords[1]+block_size[1]):
            for k in range(start_coords[2], start_coords[2]+block_size[2]):
                if random.random() <= density:
                    syn_data.append([i, j, k])


def write_to_file(syn_data, path):
    with open(path, "w") as f:
        for line in syn_data:
            f.write(",".join(map(str, line)) + "\n")


if __name__ == "__main__":
    syn_data = []
    add_block(syn_data, [0, 0, 0], [50, 50, 50], 0.0001)
    add_block(syn_data, [10, 10, 10], [3, 6, 10], 0.99)
    add_block(syn_data, [30, 30, 30], [7, 4, 11], 0.45)
    write_to_file(syn_data, "syn.csv")
