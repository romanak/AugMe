from typing import List
from augme.video.ffmpeg.base_augmenter import BaseFFMPEGAugmenter


class VideoAugmenterByQuality(BaseFFMPEGAugmenter):
    def __init__(self, quality: int):
        assert 0 <= quality <= 51, "Quality must be a value in the range [0, 51]"
        
        self.quality = quality

    def get_command(self, video_path: str, output_path: str) -> List[str]:
        """
        Alters the quality level of the video

        @param video_path: the path to the video to be augmented

        @param output_path: the path in which the resulting video will be stored.
            If not passed in, the original video file will be overwritten

        @returns: a list of strings containing the CLI FFMPEG command for
            the augmentation
        """
        return [
            *self.input_fmt(video_path),
            "-vf", "pad=width=ceil(iw/2)*2:height=ceil(ih/2)*2",
            "-c:v", "libx264",
            "-crf", f"{self.quality}",
            "-preset", "slow",
            "-c:a", "copy",
            output_path
        ]
