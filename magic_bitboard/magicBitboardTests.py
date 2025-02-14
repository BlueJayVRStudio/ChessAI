import numpy as np
from bitboard_utilities import *

def example():
    bitboard = np.uint64(0)
    # bitboard = set_bit(bitboard, 0)  # Set A1
    bitboard = set_bit(bitboard, 63) # Set H8
    print_bitboard(bitboard)
    print(type(bitboard))

    print(bitboard & FILE_A != 0)
    print(bitboard & FILE_H != 0)
    print(bitboard & RANK_1 != 0)
    print(bitboard & RANK_8 != 0)

if __name__ == "__main__":
    # print_bitboard(FILE_A)
    # print_bitboard(FILE_H)
    # print_bitboard(RANK_1)
    # print_bitboard(RANK_8)
    # example()

    cyclic_correctness = True
    for i in range(ord('a'), ord('h') + 1):
        for j in range(8):
            algebraic = chr(i) + str(j+1)
            if algebraic != index_to_square(square_to_index(algebraic)):
                cyclic_correctness = False
    
    print(f"symbolic conversion correctness: {cyclic_correctness}")
    
    