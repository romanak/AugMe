import os
import shutil
from abc import ABC, abstractmethod
from typing import List, Optional
from augme.video.helpers import (
    validate_input_and_output_paths,
    CustomNamedTemporaryFile,
    execute_ffmpeg_cmd
)

# use appropriate GPU encoder for acceleration
# however, some encoding options may not be available
encoders = {'cpu': 'libx264', 'amd': 'h264_amf', 'nvidia': 'h264_nvenc'}
# -init_hw_device cuda:0,primary_ctx=1

class BaseFFMPEGAugmenter(ABC):
    def add_augmenter(self, video_path: str, output_path: Optional[str] = None, **kwargs
    ) -> None:
        """
        Applies the specific augmentation to the video

        @param video_path: the path to the video to be augmented

        @param output_path: the path in which the resulting video will be stored.
            If not passed in, the original video file will be overwritten

        @param kwargs: parameters for specific augmenters
        """
        video_path, output_path = validate_input_and_output_paths(
            video_path, output_path
        )
        with CustomNamedTemporaryFile(
            suffix=os.path.splitext(video_path)[1]
        ) as tmpfile:
            if video_path == output_path:
                shutil.copyfile(video_path, tmpfile.name)
                video_path = tmpfile.name

            execute_ffmpeg_cmd(self.get_command(video_path, output_path))

    @abstractmethod
    def get_command(self, video_path: str, output_path: str) -> List[str]:
        """
        Constructs the FFMPEG command for VidGear

        @param video_path: the path to the video to be augmented

        @param output_path: the path in which the resulting video will be stored.

        @returns: a list of strings containing the CLI FFMPEG command for
            the augmentation
        """
        raise NotImplementedError("Implement get_command method")

    @staticmethod
    def input_fmt(video_path: str) -> List[str]:
        return [
            "-y", # overwrite existing
            "-i", video_path, # input video
        ]

    @staticmethod
    def output_fmt(output_path: str) -> List[str]:
        return [
            "-c:v", "libx264", # video encoder
            "-preset", "slow", # encoding speed to compression ratio
            "-crf", "23", # constant rate factor for constant quality encoding
            "-pix_fmt", "yuv420p", # pixel format YUV 4:2:0
            output_path, # output video
        ]

    @staticmethod
    def standard_filter_fmt(
        video_path: str, filters: List[str], output_path: str
    ) -> List[str]:
        return [
            *BaseFFMPEGAugmenter.input_fmt(video_path),
            *filters,
            *BaseFFMPEGAugmenter.output_fmt(output_path),
        ]
