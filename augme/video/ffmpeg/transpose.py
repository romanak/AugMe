from typing import List
from augme.video.ffmpeg.base_augmenter import BaseFFMPEGAugmenter


class VideoAugmenterByTransposition(BaseFFMPEGAugmenter):
    def __init__(self, direction: float):
        assert direction in [0,1,2,3], "Valid direction is one of 0,1,2,3"
        
        self.direction = direction

    def get_command(self, video_path: str, output_path: str) -> List[str]:
        """
        Transpose rows with columns in the input video and optionally flip it. 

        @param video_path: the path to the video to be augmented

        @param output_path: the path in which the resulting video will be stored.
            If not passed in, the original video file will be overwritten

        @returns: a list of strings containing the CLI FFMPEG command for
            the augmentation
        """
        filters = [
            "-vf",  f"transpose={self.direction},"
            + "pad=width=ceil(iw/2)*2:height=ceil(ih/2)*2",
            "-c:a", "copy",
        ]
        
        return self.standard_filter_fmt(video_path, filters, output_path)
