from math import ceil, sqrt
from typing import List
from augme.video.ffmpeg.base_augmenter import BaseFFMPEGAugmenter
from augme.video.helpers import get_video_info


class VideoAugmenterByAspectRatio(BaseFFMPEGAugmenter):
    def __init__(self, ratio: float):
        assert (ratio > 0), "Aspect ratio must be positive number"
        self.aspect_ratio = ratio

    def get_command(self, video_path: str, output_path: str) -> List[str]:
        """
        Changes the sample (sar) & display (dar) aspect ratios of the video

        @param video_path: the path to the video to be augmented

        @param output_path: the path in which the resulting video will be stored.

        @returns: a list of strings containing the CLI FFMPEG command for
            the augmentation
        """
        video_info = get_video_info(video_path)
        area = int(video_info["width"]) * int(video_info["height"])

        # FFmpeg requires even dimensions
        new_w = ceil(int(sqrt(area * self.aspect_ratio)) / 2) * 2
        new_h = ceil(int(area / new_w) / 2) * 2

        filters = [
            "-vf",  f"scale=width={new_w}:height={new_h},"
            + f"setsar=ratio=1:1,"
            + f"setdar=ratio={self.aspect_ratio}",
            "-c:a", "copy",
        ]

        return self.standard_filter_fmt(video_path, filters, output_path)
