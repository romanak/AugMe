from typing import List
from augme.video.ffmpeg.base_augmenter import BaseFFMPEGAugmenter


class VideoAugmenterByResolution(BaseFFMPEGAugmenter):
    def __init__(self, factor: float):
        assert factor > 0.0, "Scale factor must be positive"

        self.factor = factor

    def get_command(self, video_path: str, output_path: str) -> List[str]:
        """
        Alters the resolution of the video

        @param video_path: the path to the video to be augmented

        @param output_path: the path in which the resulting video will be stored.
            If not passed in, the original video file will be overwritten

        @returns: a list of strings containing the CLI FFMPEG command for
            the augmentation
        """
        filters = [
            "-vf", f"scale=height:ih*{self.factor}:width=iw*{self.factor},"
            + "pad=width=ceil(iw/2)*2:height=ceil(ih/2)*2"
        ]

        return self.standard_filter_fmt(video_path, filters, output_path)
