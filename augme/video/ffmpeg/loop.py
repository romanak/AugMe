from typing import List
from augme.video.ffmpeg.base_augmenter import BaseFFMPEGAugmenter


class VideoAugmenterByLoops(BaseFFMPEGAugmenter):
    def __init__(self, num_loops: int):
        assert num_loops >= 0, "Number of loops cannot be a negative number"
        
        self.num_loops = num_loops

    def get_command(self, video_path: str, output_path: str) -> List[str]:
        """
        Loops the video `num_loops` times

        @param video_path: the path to the video to be augmented

        @param output_path: the path in which the resulting video will be stored.

        @returns: a list of strings containing the CLI FFMPEG command for
            the augmentation
        """
        return [
            "-y",
            "-stream_loop",
            str(self.num_loops),
            "-i",
            video_path,
            "-vf", "pad=width=ceil(iw/2)*2:height=ceil(ih/2)*2",
            "-c:a", "copy",
            *self.output_fmt(output_path),
        ]
