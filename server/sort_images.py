import os, glob, shutil, time, logging
from sys import platform as _platform
from PIL import Image

logger = logging.getLogger('sort-images')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('sort-images.log')
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)

def create_folders(paths):
    for path in paths:
        logger.info('Attempting to create folder - {}'.format(path))
        if not os.path.exists(path):
            os.makedirs(path)
            logger.info('Folder -- {} -- created'.format(path))
        else:
            logger.info('Folder -- {} -- already exists'.format(path))
def retrieve_resolutions(file_path):
    return open(file_path).read().split('\n')

def detect_os():
    if _platform == "linux" or _platform == "linux2" or _platform == "darwin":
        logger.info('Using Unix based filepath slashes')
        return '/'
    else:
        logger.info('Using Windows based filepath slashes')
        return '\\'
    logger.warn('Cannot detect platform. Defaulting to Windows based file system')
    return '\\'

def move_images(image_list):
    for info in image_list:
        if not os.path.isfile(info['destination']):
            logger.info('Attempting to move {} to {}'.format(info['file_name'], info['destination']))
            shutil.copy(info['source'], info['destination'])
            logger.info('Moved {} to {}'.format(info['file_name'], info['destination']))

def main():
    slash = detect_os()
    source_folder = os.path.abspath('.{}images{}'.format(slash, slash))
    logger.info('Creating source folder variable: {}'.format(source_folder))
    favorite = os.path.abspath('.{}sorted{}favorites'.format(slash, slash)) + '{}'.format(slash)
    print(favorite)
    logger.info('Creating favorite folder variable: {}'.format(favorite))
    others = os.path.abspath('.{}sorted{}others{}'.format(slash, slash, slash))
    logger.info('Creating others folder variable: {}'.format(others))
    all_image_paths = os.path.abspath('.{}images{}*.*'.format( slash, slash))
    paths = [favorite, others]
    logger.info('Creating all image paths variable: {}'.format(paths))

    favs = retrieve_resolutions(os.path.abspath('.{}fav_resolutions.txt'.format(slash)))
    fav_resolutions = list(map(lambda add_string: favorite + add_string, favs))
    other_resolutions_list = []
    paths = paths + fav_resolutions
    for x in paths:
        print(x)
    images = []
    create_folders(paths)
    sorted_folder = os.path.abspath('.{}sorted{}'.format(slash, slash))

    for found_file in glob.glob(all_image_paths):
        image = {}
        file_name = found_file.replace(source_folder, '')
        width, height = Image.open(found_file).size
        resolution = '{}x{}'.format(str(width), str(height))
        image['file_name'] = file_name
        image['source'] =  found_file
        image['resolution'] = resolution
        if resolution in favs:
            dest = '{}{}{}{}{}'.format(os.path.abspath(favorite),slash,resolution,slash,file_name)
            image['destination'] = dest.replace('//','/')
        else:
            oth = '{}{}{}{}{}'.format(os.path.abspath(others),slash,resolution,slash,file_name)
            image['destination'] = oth.replace('//','/')
            other_resolutions_list.append('{}{}{}{}'.format(os.path.abspath(others),slash,resolution,slash))
        images.append(image)

    create_folders(other_resolutions_list)
    move_images(images)
    shutil.make_archive('sorted', 'zip', sorted_folder)
    remove_images = glob.glob(source_folder+"{}*".format(slash))
    for f in remove_images:
        os.remove(f)
    shutil.rmtree(sorted_folder)
if __name__ == "__main__":
    main()