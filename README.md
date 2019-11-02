# ImageTools

## About
sort images and videos in directories

_version:_ 0.3.1  
_author:_ suppetia

## Getting started

```sh
C:\path\where\script\is\stored>python ImageSorter.py --help
usage: ImageSorter.py [-h] [--file_operation FILE_OPERATION]
                      [--filename_extensions [FILENAME_EXTENSIONS [FILENAME_EXTENSIONS ...]]]
                      [--dir_structure DIR_STRUCTURE] [--read_recursive]
                      [--dst_dir DST_DIR]
                      src_dir

sort images by date taken or last modification date (if there is no exif data)

positional arguments:
  src_dir

optional arguments:
  -h, --help            show this help message and exit
  --file_operation FILE_OPERATION
  --filename_extensions [FILENAME_EXTENSIONS [FILENAME_EXTENSIONS ...]], -ext [FILENAME_EXTENSIONS [FILENAME_EXTENSIONS ...]]
  --dir_structure DIR_STRUCTURE, -struc DIR_STRUCTURE
  --read_recursive, -rr
  --dst_dir DST_DIR
```

#### parameters

- `file_operation`: _str_  
    _default_: `'cp'`  
    _description_: determine whether files are moved or copied  
    _values_:  
    - `'copy'`, `'cp'`: copies the files into the new directory structure
    - `'move'`, `'mv'`: moves the files into the new directory structure
- `filename extensions`: _[str]_  
    _default_: `['jpg']`  
    _description_: list of filename extensions to query for  
    _values_: theoretically all types of files but just accurate for image/video files (as the program uses `os.path.getmtime` when the files got no exif data)
- `dir_structure`: _str_  
    _default_: `'ymd'`  
    _description_: determine the sorting directory levels (example: `'ymd'`- `yyyy/yyyy_mm/yyyy_mm_dd`) 
    _values_:
    - contains `'y'` - directory level year (`'yyyy'`)
    - contains `'m'` - directory level month (`'yyyy_mm'`)
    - contains `'d'` - directory level day (`'yyyy_mm_dd'`)
- `read_recursive`: _boolean_  
    _default_: `False`  
    _description_: determine whether also subdirectories should be queried  
    _value_: set to `True` via `-rr` or `--read_recursive`
- `src_dir`: _path_like_/_str_  
    _description_: the directory of the files to be sorted
- `dst_dir`: _path_like_/_str_  
    _default_: `src_dst`  
    _description_: the super directory of the sorted file structure  
    
## Example use

```sh
# copy all jpg, mov, mp4 files into sorted file structure of format 'yyyy/yyyy_mm_dd'
C:\path\where\script\is\stored>python ImageSorter.py test_images -ext jpg mov mp4 -struc yd

# move all jpg files 'test_images' this and all subdirectories to 'test_sorted' 
# into sorted file structure of format 'yyyy/yyyy_mm/yyyy_mm_dd'
C:\path\where\script\is\stored>python ImageSorter.py test_images --dst_dir test_sorted -rr
```
