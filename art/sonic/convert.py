# Notes to anyone who wants to use this:

# This converter tool takes INDEXED COLOR IMAGES ONLY.
# Colors 0-15 are assigned to the corresponding colors in the palette.
# The actual colors in the image's palette are ignored.

# The tool reads tiles top to bottom first, then left to right, 
# and dumps them into an uncompressed file.

from PIL import Image
from numpy import asarray

def read_tiles(filename: str):
    img = asarray(Image.open(filename + '.png'))
    return [img[x:x+8,y:y+8] for y in range(0,img.shape[1],8) for x in range(0,img.shape[0],8)]

def get_bit(num: int, n: int) -> bool:
    return (bool) (num & (1 << n))

def set_bit(num: int, n: int, val: bool) -> int:
    if (val):
        return num | (1 << n)
    else:
        return num & ~(1 << n)

def row_to_planar(row) -> bytearray:
    bytes = bytearray([0] * 4)
    for byte_number in range(4):
        for color_number in range(8):
            bytes[byte_number] = set_bit(bytes[byte_number], 7 - color_number, get_bit(row[color_number], byte_number))
    return bytes

def tile_to_planar(tile) -> bytearray:
    bytes = bytearray()
    for row in tile:
        bytes += row_to_planar(row)
    return bytes

def image_to_planar(img) -> bytearray:
    bytes = bytearray()
    for tile in img:
        bytes += tile_to_planar(tile)
    return bytes

def write_binary(bin: bytearray, filename: str) -> None:
    with open(filename + '.bin', 'wb') as file:
        file.write(bin)

def convert_art(file: str) -> None:
    write_binary(image_to_planar(read_tiles(file)), file)

convert_art('art_ucmp_sonic')
convert_art('art_ucmp_sonic_mirrored')
