# This program receives a spritesheet and some data about it and creates another spritesheet
# where all the frames are the same size.
#
# Usage: spritesheet_standardizer <original image> <data file> <output image name>
#
# Data file format:
# <first chunk frame width> <first chunk frame height> <first chunk width> <first chunk height>
# <second chunk frame width> <second chunk frame height> <second chunk width> <second chunk height>
# ...
# <last chunk frame width> <last chunk frame height> <last chunk width> <last chunk height>
# <output frame width> <output frame height>
#
# If chunk width is zero the chunk is skipped and is not counted on the final sheet.
#
# A chunk is defined by a rectangular set of equally spaced frames with the same width and height.
# Chunks are obtained from top to bottom and currently this program cannot handle offsets
# and repositionings of any kind.

from PIL import Image
import sys

class Chunk:
    def __init__(self, frame_width, frame_height, width=0, height=0):
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.width = width
        self.height = height

def parse_input(file_name):
    chunks = []
    with open(file_name, "r") as f:
        chunks = [Chunk(*[int(number) for number in line.split()]) for line in f]
    return chunks

def main():
    original_sheet = Image.open(sys.argv[1])
    parsed_input = parse_input(sys.argv[2])
    final_sheet_name = sys.argv[3]

    chunks, final_frame_size = parsed_input[:-1], parsed_input[-1]
    final_frame_width, final_frame_height = final_frame_size.frame_width, final_frame_size.frame_height

    sheet_width = final_frame_width * max([chunk.width for chunk in chunks])
    sheet_height = final_frame_height * sum([chunk.height for chunk in chunks if chunk.width > 0])
    final_sheet = Image.new("RGBA", (sheet_width, sheet_height), color=(0, 0, 0, 0))

    acc_height = 0
    acc_lines = 0
    for chunk in chunks:
        for i in range(chunk.height):
            for j in range(chunk.width):
                v_border = chunk.frame_height - final_frame_height
                h_border = chunk.frame_width - final_frame_width

                left = j * chunk.frame_width + max(0, h_border // 2)
                upper = acc_height + i * chunk.frame_height + max(0, v_border // 2)
                right = left + min(chunk.frame_width, final_frame_width)
                lower = upper + min(chunk.frame_height, final_frame_height)
                frame = original_sheet.crop((left, upper, right, lower))

                final_sheet.paste(frame, (j * final_frame_width + max(0, -h_border // 2),
                                         (acc_lines + i) * final_frame_height + max(0, -v_border // 2)))

        acc_height += chunk.height * chunk.frame_height
        if chunk.width != 0:
            acc_lines += chunk.height

    # final_sheet.show()
    final_sheet.save(final_sheet_name, format="png")

if __name__ == '__main__':
    main()
