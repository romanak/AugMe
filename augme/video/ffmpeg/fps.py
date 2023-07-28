from typing import List
from augme.video.ffmpeg.base_augmenter import BaseFFMPEGAugmenter


class VideoAugmenterByFPSChange(BaseFFMPEGAugmenter):
    def __init__(self, fps: int):
        assert fps > 0, "FPS must be greater than zero"
        self.fps = fps

    def get_command(self, video_path: str, output_path: str) -> List[str]:
        """
        Changes the frame rate of the video

        @param video_path: the path to the video to be augmented

        @param output_path: the path in which the resulting video will be stored.

        @returns: a list of strings containing the CLI FFMPEG command for
            the augmentation
        """
        filters = [
            "-vf", f"fps=fps={self.fps}:round=up,"
            + "pad=width=ceil(iw/2)*2:height=ceil(ih/2)*2",
            "-c:a", "copy",
        ]

        return self.standard_filter_fmt(video_path, filters, output_path)
