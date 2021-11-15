import os
import cv2
import pickle


def compute_sift(image_path:str, output_dir:str ) ->str:
    image = cv2.imread(image_path,cv2.IMREAD_GRAYSCALE)
    sift = cv2.SIFT_create()
    keypoints, descriptors = sift.detectAndCompute(image,None)
    pickle_kp=list(map(lambda p: (p.pt[0],p.pt[0], p.size, p.angle, p.response, p.octave, p.class_id),keypoints))
    #print(pickle_kp[1], len(pickle_kp))
    features = {
        "keypoint": pickle_kp,
        "descriptor": descriptors,
    }
    base_name = get_basename(image_path)
    pickle_file_path=os.path.join(output_dir,f'{base_name}.pickle')
    with open(pickle_file_path, mode="wb") as pkl_file:
        pickle.dump(features, pkl_file)
    return pickle_file_path   