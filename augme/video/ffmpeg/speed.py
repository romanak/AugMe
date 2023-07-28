from typing import List
from augme.video.ffmpeg.base_augmenter import BaseFFMPEGAugmenter


class VideoAugmenterBySpeed(BaseFFMPEGAugmenter):
    def __init__(self, factor: float):
        assert factor > 0, "Factor must be greater than zero"
        
        self.factor = factor

    def get_command(self, video_path: str, output_path: str) -> List[str]:
        """
        Changes the speed of the video

        @param video_path: the path to the video to be augmented

        @param output_path: the path in which the resulting video will be stored.
            If not passed in, the original video file will be overwritten

        @returns: a list of strings containing the CLI FFMPEG command for
            the augmentation
        """
        filters = [
            "-vf", f"setpts={1/self.factor}*PTS,"
            + "pad=width=ceil(iw/2)*2:height=ceil(ih/2)*2",
            "-af", f"atempo={self.factor}",
            "-c:a", "aac",
        ]

        return self.standard_filter_fmt(video_path, filters, output_path)
