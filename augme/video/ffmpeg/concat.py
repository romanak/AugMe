from math import ceil
from typing import List, Tuple
from augme.video.ffmpeg.base_augmenter import BaseFFMPEGAugmenter
from augme.video.helpers import get_video_info, validate_path, validate_rgb_color


class VideoAugmenterByConcat(BaseFFMPEGAugmenter):
    def __init__(
        self,
        video_paths: List[str],
        src_video_path_index: int,
        pad_color: Tuple[int, int, int],
    ):
        assert len(video_paths) > 0, "Please provide at least one input video"
        assert len(video_paths) > src_video_path_index, "Please provide a valid src_video_path_index"
        validate_rgb_color(pad_color)
        [validate_path(video_path) for video_path in video_paths]

        self.video_paths = video_paths
        self.src_video_path_index = src_video_path_index
        self.video_infos = [get_video_info(path) for path in video_paths]
        self.hex_color = "%02x%02x%02x" % pad_color
        

    def get_command(self, video_path: str, output_path: str) -> List[str]:
        """
        Concatenates multiple videos together

        @param video_path: the path to the video to be augmented

        @param output_path: the path in which the resulting video will be stored.

        @returns: a list of strings containing the CLI FFMPEG command for
            the augmentation
        """
        video_info = self.video_infos[self.src_video_path_index]
        height = ceil(video_info["height"] / 2) * 2
        width = ceil(video_info["width"] / 2) * 2
        frame_rate = video_info["r_frame_rate"]

        inputs = [["-i", video] for video in self.video_paths]
        flat_inputs = [element for sublist in inputs for element in sublist]
        scale_filter, maps = "", ""
        for i in range(len(self.video_paths)):
            if (self.video_infos[i]['width'] / self.video_infos[i]['height']) < (width / height):
                scale_filter += f"[{i}:v:0]scale=w=-1:h={height}[{i}scale];"
            else:
                scale_filter += f"[{i}:v:0]scale=w={width}:h=-1[{i}scale];"
            scale_filter += (
                f"[{i}scale]pad=w={width}:h={height}:x=(ow-iw)/2:y=(oh-ih)/2:color={self.hex_color}[{i}pad];"
                f"[{i}pad]setsar=ratio=1:1[{i}sar],"
                f"[{i}sar]setdar=ratio={width / height}[{i}v];"
            )
            maps += f"[{i}v][{i}:a]"

        return [
            "-y",
            *flat_inputs,
            "-filter_complex", scale_filter + maps + f"concat=n={len(self.video_paths)}:v=1:a=1[v][a]",
            "-map", "[v]",
            "-map", "[a]",
            "-fps_mode", "cfr", # duplicate and drop frames for constant frame rate
            "-r", str(frame_rate),
            "-c:a", "aac",
            *self.output_fmt(output_path),
        ]
