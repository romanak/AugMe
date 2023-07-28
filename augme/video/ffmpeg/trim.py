from typing import List, Optional
from augme.video.ffmpeg.base_augmenter import BaseFFMPEGAugmenter
from augme.video.helpers import get_video_info


class VideoAugmenterByTrim(BaseFFMPEGAugmenter):
    def __init__(self, start: Optional[float] = None, end: Optional[float] = None):
        assert start is None or start >= 0, "Start cannot be a negative number"
        assert (
            end is None or (start is not None and end > start) or end > 0
        ), "End must be a non-negative value greater than start"

        self.start = start
        self.end = end


    def get_command(self, video_path: str, output_path: str) -> List[str]:
        """
        Trims the video

        @param video_path: the path to the video to be augmented

        @param output_path: the path in which the resulting video will be stored.

        @returns: a list of strings containing the CLI FFMPEG command for
            the augmentation
        """
        video_info = get_video_info(video_path)

        if self.start is None:
            self.start = 0
        if self.end is None:
            self.end = video_info["duration"]

        duration = self.end - self.start

        return [
            "-y", # overwrite existing
            "-ss", str(self.start), # start timestamp of the cut, put before input for better performance
            "-i", video_path, # input video
            "-t", str(duration), # duration of the cut counting from start timestamp
            "-vf", "pad=width=ceil(iw/2)*2:height=ceil(ih/2)*2",
            "-c:a", "copy",
            *self.output_fmt(output_path),
        ]
