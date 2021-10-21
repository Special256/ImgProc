import shutil
import subprocess
import glob
from tqdm import tqdm
import numpy as np
import os
import argparse



def extract_frames(video, dst):
    with open(os.devnull, "w") as ffmpeg_log:
        if os.path.exists(dst):
            print(" cleanup: " + dst + "/")
            shutil.rmtree(dst)
        os.makedirs(dst)
        video_to_frames_command = ["ffmpeg",
                                   # (optional) overwrite output file if it exists
                                   '-y',
                                   '-i', video,  # input file
                                   # '-vf', "scale=322:230",  # input file
                                   '-vf', 'fps=1',

                                   '-qscale:v', "2",  # quality for JPEG
                                   '{0}/%06d.jpg'.format(dst)]
        subprocess.call(video_to_frames_command,
                        stdout=ffmpeg_log, stderr=ffmpeg_log)
def ext_video(ext):
    video_list = glob.glob(os.path.join(ext['video_path'], '*.avi'))
    for video in tqdm(video_list):
        video_id = video.split("/")[-1].split(".")[0]
        dst = video_id
        extract_frames(video, dst)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--gpu", dest='gpu', type=str, default='0',
                        help='Set CUDA_VISIBLE_DEVICES environment variable, optional')
    
    parser.add_argument("--n_frame_steps", dest='n_frame_steps', type=int, default=40,
                        help='how many frames to sampler per video')

    parser.add_argument("--video_path", dest='video_path', type=str,
                        default='', help='path to video dataset')
    
    args = parser.parse_args()
    os.environ['CUDA_VISIBLE_DEVICES'] = args.gpu
    ext = vars(args)
    

    ext_video(ext)