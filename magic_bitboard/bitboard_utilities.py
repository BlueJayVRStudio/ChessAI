import numpy as np

def set_bit(bitboard: np.uint64, square: int) -> np.uint64:
    return bitboard | (np.uint64(1) << np.uint64(square))

def clear_bit(bitboard: np.uint64, square: int) -> np.uint64:
    return bitboard & ~(np.uint64(1) << np.uint64(square))

def is_bit_set(bitboard: np.uint64, square: int) -> bool:
    return (bitboard & (np.uint64(1) << np.uint64(square))) != 0

def print_bitboard(bitboard: np.uint64):
    for rank in range(7, -1, -1):
        row = ""
        for file in range(8):
            square = rank * 8 + file
            row += "1 " if is_bit_set(bitboard, square) else ". "
        print(row)
    print()

# algebraic to numeric index
def square_to_index(square: str) -> int:
    file = ord(square[0]) - ord('a')
    rank = int(square[1]) - 1
    return rank * 8 + file

# numeric index to algebraic
def index_to_square(index: int) -> str:
    file = index % 8
    rank = index // 8 + 1
    return f"{chr(ord('a') + file)}{rank}"

# Constants for board representation
FILE_A = np.uint64(0x0101010101010101)
FILE_H = np.uint64(0x8080808080808080)
RANK_1 = np.uint64(0x00000000000000FF)
RANK_8 = np.uint64(0xFF00000000000000)

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
    
    