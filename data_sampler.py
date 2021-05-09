""""
    read the date of the berklet segmentation to sample an image with a segmentation map
    given by a human
 """
import os,glob
dirFile = os.path.dirname(__file__)

rel_path_data = "..//Data"
path_dir_data = os.path.join(dirFile, rel_path_data)
assert os.path.exists(path_dir_data), "directory of data is not available"

path_img_database = os.path.join(path_dir_data, "BSDS300-images//BSDS300//images//train")
path_seg_img_database = os.path.join(path_dir_data, "BSDS300-human//BSDS300//human//color")

def sample_data(index):
    """

        returns id of an image given index
    """
    try:
        id_img = os.listdir(path_img_database)[index]
        whole_path = os.path.join(path_img_database,id_img)
        return whole_path,id_img
    except IndexError:
        print(f"should choose index between 0 and {len(path_img_database)}")

def get_path_seg_from_id_img(id_img):
    """
        given the id of an image (sequence of numbers) get one of the segmentation
    """

    for root, dirs, files in os.walk(path_seg_img_database, topdown=False):
        for name in files:
            if name.replace(".seg", ".jpg") == id_img:
                whole_path = os.path.join(root, name)
                return whole_path

def get_path_img_and_seg_from_id(index):
    path_img , id_img = sample_data(index)
    path_seg = get_path_seg_from_id_img(id_img)
    return path_img,path_seg

#TODO: add a generator to cycle for all the data

#TODO : add a function to get all the segmentations for one image

if __name__ == '__main__':
    path_img,path_seg = get_path_img_and_seg_from_id(index=99)