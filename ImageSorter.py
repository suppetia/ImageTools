"""
move or copy images in directories named by the dates the pictures were taken

Christopher Mertens
2019-10-20
version: 0.2.2
"""

import glob
import os
import shutil
import sys
import argparse
from PIL import Image


def sort_by_date_taken(src_dir, dst_dir=None, file_operation='cp', filename_extensions=['jpg'], **kwargs):
    """
    copy images into directories named by the date when the picture was taken
    :param src_dir: directory to copy the files from
    :param dst_dir: target directory to copy the files to
    :param file_operation: file operation to perform on the files
    :param filename_extensions: filter the files by extension
    """

    def _get_date_taken(path):
        """
        get date when picture was taken from exif metadata
        :param path: path of the picture
        :return: DateTimeOriginal (exif id 36867)
        """
        return Image.open(path)._getexif()[36867]

    def _create_dir_name(date, dir_structure='ymd'):
        """
        create the directory path
        :param date: exif data of the picture
        :param dir_structure: structure of dir (example: 'ymd' - 'YYYY\YYYY_MM\YYYY_MM_DD; 'yd' - YYYY\YYYY_MM_DD)
        :return: relative path/name of the directory
        """
        date_splitted = date.split(' ')[0].split(':')
        dir_name = '\\'
        if 'y' in dir_structure:
            dir_name += date_splitted[0] + '\\'
        if 'm' in dir_structure:
            dir_name += '_'.join(d for d in date_splitted[:2]) + '\\'
        if 'd' in dir_structure:
            dir_name += '_'.join(d for d in date_splitted[:3]) + '\\'
        return dir_name

    # set dst_dir to src_dir if not specified
    if dst_dir is None:
        dst_dir = src_dir
    # find all files with specified file name extension
    files = []
    for filename_extension in filename_extensions:
        if 'read_recursive' in kwargs.keys() and kwargs['read_recursive']:
            files += glob.glob(src_dir + "\\**\\*." + filename_extension, recursive=True)
        else:
            files += glob.glob(src_dir + "\\*." + filename_extension)
    print("copying " + str(len(files)) + " files from " + src_dir + " to " + dst_dir + '\n')
    for num, file in enumerate(files):
        # create the name of directory structure
        if 'dir_structure' in kwargs.keys():
            dir_name = _create_dir_name(_get_date_taken(file), dir_structure=kwargs['dir_structure'])
        else:
            dir_name = _create_dir_name(_get_date_taken(file))
        date_dir = dst_dir + "\\" + dir_name + "\\"
        # create new date directory if it doesn't exists
        os.makedirs(date_dir, exist_ok=True)
        if file_operation in ['copy', 'cp']:
            # copy file to new dir
            shutil.copy(file, date_dir + file.split("\\")[-1])
        elif file_operation in ['move', 'mv']:
            # move file to new dir
            shutil.move(file, date_dir + file.split("\\")[-1])

        # print the number of files left
        sys.stdout.write("\r" + str(len(files)-num) + " files left")
        sys.stdout.flush()

    sys.stdout.write('\r')
    sys.stdout.flush()
    print(str(len(files)) + " files sorted")


if __name__ == '__main__':

    # parse command prompt arguments
    parser = argparse.ArgumentParser(description="sort images by date taken")

    parser.add_argument('--file_operation', action='store', default='cp')
    parser.add_argument('--filename_extensions', '-ext', action='store', nargs='*', default=['jpg'])
    parser.add_argument('--dir_structure', '-struc', action='store', default='ymd')
    parser.add_argument('--read_recursive', '-rr', action='store_true')
    parser.add_argument('src_dir', action='store')
    parser.add_argument('--dst_dir', action='store', default=None)

    args = parser.parse_args()

    # check arguments validity
    if args.file_operation not in ['cp', 'mv', 'copy', 'move']:
        parser.error('invalid file_operation:' + args.file_operation)
    if not any(char in args.dir_structure for char in ['y', 'm', 'd']):
        parser.error('invalid option for dir_structure: ' + args.dir_structure)

    # get absolute path
    src_dir = os.path.abspath(args.src_dir)
    if not os.path.exists(src_dir):
        parser.error("source directory doesn't exist")
    dst_dir = os.path.abspath(args.dst_dir) if args.dst_dir is not None else None

    sort_by_date_taken(src_dir=src_dir, dst_dir=dst_dir, file_operation=args.file_operation,
                       filename_extensions=args.filename_extensions,
                       dir_structure=args.dir_structure, read_recursive=args.read_recursive)

    """ uncomment for executing without command prompt
    # enter the src dir to sort
    src_dir = os.path.abspath("test_images\\test_sorted")
    sort_by_date_taken(src_dir, file_operation='mv', dir_structure='ymd', read_recursive=True)
    """
