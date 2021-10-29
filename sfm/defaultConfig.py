from typing import Dict

config: Dict = {
    "extension": ['jpg', 'JPEG', 'png', 'PNG'],
    'feature_type': 'SIFT',
    'feature_root': 1,
    'sift_peak_threshold': 0.1,
    'sift_edge_threshold': 10,
    'surf_hessian_threshold': 3000,
    'surf_n_octaves': 4,
    'surf_n_octavelayers': 2,
    'surf_upright': 0,
    'akaze_omax': 4,
    'akaze_dthreshold': 0.001,
    'akaze_descriptor': 'MSURF',
    'akaze_descriptor_size': 0,
    'akaze_descriptor_channels': 3,
    'akaze_kcontrast_percentile': 0.7,
    'akaze_use_isotropic_diffusion': 'no',
    'lowes_ratio': 0.8,
    'matcher_type': 'FLANN',
    'symmetric_matching': 'yes',
    'flann_algorithm': 'KMEANS',
    'flann_branching': 8,
    'flann_iterations': 10,
    'flann_tree': 8,
    'flann_checks': 20
 }