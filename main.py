import argparse
import os
import glob
from PIL import Image, ImageOps


BORDER_PADDING = 200
BORDER_COLOR = 'white'


def resize_square(image, fill_color=(255, 255, 255)):
    width, height = image.size
    side_length = max(width, height)

    resized_image = Image.new('RGB', (side_length, side_length), fill_color)
    resized_image.paste(
        image, (int((side_length - width) / 2),
                int((side_length - height) / 2)))

    return resized_image


def parse_arguments():
    parser = argparse.ArgumentParser(description='Add borders to images.')
    parser.add_argument('--src',
                        type=directory_path,
                        help='Image source directory.',
                        required=True)
    parser.add_argument('--dst',
                        type=directory_path,
                        help='Image output directory.',
                        required=True)

    return parser.parse_args()


def directory_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(
            f"Given path {path} is not a valid path")


def main():
    parsed_arguments = parse_arguments()

    source_paths = glob.glob(os.path.join(parsed_arguments.src, '*.jpg'))

    for source_path in source_paths:
        _, filename = os.path.split(source_path)

        image = Image.open(source_path)
        square_image = resize_square(image)
        padded_square_image = ImageOps.expand(
            square_image, BORDER_PADDING, BORDER_COLOR)

        padded_square_image.save(os.path.join(
            parsed_arguments.dst, filename), quality=100)


if __name__ == '__main__':
    main()
