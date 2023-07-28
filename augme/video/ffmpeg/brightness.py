from typing import List
from augme.video.ffmpeg.base_augmenter import BaseFFMPEGAugmenter


class VideoAugmenterByBrightness(BaseFFMPEGAugmenter):
    def __init__(self, level: float):
        assert -1.0 <= level <= 1.0, "Level must be a value in the range [-1.0, 1.0]"
        
        self.level = level

    def get_command(self, video_path: str, output_path: str) -> List[str]:
        """
        Changes the brightness level of the video

        @param video_path: the path to the video to be augmented

        @param output_path: the path in which the resulting video will be stored.

        @returns: a list of strings containing the CLI FFMPEG command for
            the augmentation
        """
        filters = [
            "-vf", f"eq=brightness={self.level},"
            + "pad=width=ceil(iw/2)*2:height=ceil(ih/2)*2",
            "-c:a", "copy",
        ]

        return self.standard_filter_fmt(video_path, filters, output_path)
