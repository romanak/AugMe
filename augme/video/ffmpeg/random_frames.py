from typing import List
from augme.video.ffmpeg.base_augmenter import BaseFFMPEGAugmenter


class VideoAugmenterByRandomFrames(BaseFFMPEGAugmenter):
    def __init__(self, num_frames: int):
        assert num_frames > 1, "num_frames must be greater than one"

        self.num_frames = num_frames


    def get_command(self, video_path: str, output_path: str) -> List[str]:
        """
        Flushes video frames from internal cache of frames into a random order

        @param video_path: the path to the video to be augmented

        @param output_path: the path in which the resulting video will be stored.
            If not passed in, the original video file will be overwritten

        @returns: a list of strings containing the CLI FFMPEG command for
            the augmentation
        """
        filters = [
            "-vf", f"random=frames={self.num_frames},"
            + "pad=width=ceil(iw/2)*2:height=ceil(ih/2)*2",
            "-c:a", "copy",
        ]

        return self.standard_filter_fmt(video_path, filters, output_path)
