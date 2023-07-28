from math import pi
from typing import List
from augme.video.ffmpeg.base_augmenter import BaseFFMPEGAugmenter


class VideoAugmenterByRotation(BaseFFMPEGAugmenter):
    def __init__(self, degrees: float):
        self.degrees = degrees

    def get_command(self, video_path: str, output_path: str) -> List[str]:
        """
        Rotates the video

        @param video_path: the path to the video to be augmented

        @param output_path: the path in which the resulting video will be stored.
            If not passed in, the original video file will be overwritten

        @returns: a list of strings containing the CLI FFMPEG command for
            the augmentation
        """
        filters = [
            "-vf",  f"rotate={self.degrees * (pi / 180)},"
            + "pad=width=ceil(iw/2)*2:height=ceil(ih/2)*2",
            "-c:a", "copy",
        ]
        
        return self.standard_filter_fmt(video_path, filters, output_path)
