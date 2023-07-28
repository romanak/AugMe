from typing import List, Optional
from augme.video.ffmpeg.base_augmenter import BaseFFMPEGAugmenter
from augme.video.helpers import get_video_info
from math import ceil


class VideoAugmenterByResize(BaseFFMPEGAugmenter):
    def __init__(self, width: Optional[int], height: Optional[int]):
        assert width is None or width > 0, "Width must be set to None or be positive"
        assert height is None or height > 0, "Height must be set to None or be positive"
        
        self.width, self.height = width, height
        

    def get_command(self, video_path: str, output_path: str) -> List[str]:
        """
        Resizes the video

        @param video_path: the path to the video to be augmented

        @param output_path: the path in which the resulting video will be stored.
            If not passed in, the original video file will be overwritten

        @returns: a list of strings containing the CLI FFMPEG command for
            the augmentation
        """
        video_info = get_video_info(video_path)

        if self.width and self.height:
            new_width = ceil(self.width / 2) * 2
            new_height = ceil(self.height / 2) * 2
        elif self.width:
            new_width = ceil(self.width / 2) * 2
            new_height = ceil(video_info["height"] / video_info["width"] * self.width / 2) * 2
        elif self.height:
            new_width = ceil(video_info["width"] / video_info["height"] * self.height / 2) * 2
            new_height = ceil(self.height / 2) * 2
        else:
            new_width = ceil(video_info["width"] / 2) * 2
            new_height = ceil(video_info["height"] / 2) * 2

        filters = [
            "-vf",  f"scale=width={new_width}:height={new_height},"
            + "pad=width=ceil(iw/2)*2:height=ceil(ih/2)*2,"
            + "setsar=ratio=1:1,"
            + f"setdar=ratio={new_width / new_height}",
        ]

        return self.standard_filter_fmt(video_path, filters, output_path)
