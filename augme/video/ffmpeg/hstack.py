from math import ceil
from typing import List, Tuple
from augme.video.ffmpeg.base_augmenter import BaseFFMPEGAugmenter
from augme.video.helpers import (
    get_video_info,
    get_audio_info,
    validate_path,
    validate_rgb_color,
)


class VideoAugmenterByHStack(BaseFFMPEGAugmenter):
    def __init__(
        self,
        second_video_path: str,
        merge_audio: bool,
        target_grid: int,
        preserve_aspect_ratio: bool,
        pad_second_video: bool,
        pad_color: Tuple[int, int, int],
        max_width: int,
    ):
        assert target_grid in [0,1], "Valid target_grid is one of 0,1"
        validate_rgb_color(pad_color)
        validate_path(second_video_path)

        self.second_video_path = second_video_path
        self.merge_audio = merge_audio
        self.target_grid = target_grid
        self.preserve_aspect_ratio = preserve_aspect_ratio
        self.pad_second_video = pad_second_video
        self.hex_color = "%02x%02x%02x" % pad_color
        self.max_width = max_width


    def get_command(self, video_path: str, output_path: str) -> List[str]:
        """
        Stacks two videos together

        @param video_path: the path to the video to be augmented

        @param output_path: the path in which the resulting video will be stored.
            If not passed in, the original video file will be overwritten

        @returns: a list of strings containing the CLI FFMPEG command for
            the augmentation
        """
        video_info = get_video_info(video_path)
        audio_info = get_audio_info(video_path)
        second_video_info = get_video_info(self.second_video_path)
        second_audio_info = get_audio_info(self.second_video_path)

        duration = video_info['duration']
        n_loops = ceil(duration / second_video_info['duration'])

        audio_filter = ""
        audio_codec = ["-c:a", "copy",]
        if (self.merge_audio and audio_info and second_audio_info):
            audio_filter = ";[0:a:0][1:a:0]amerge=inputs=2,pan=stereo|c0<c0+c2|c1<c1+c3[a]"
            audio_map = ["-map",  "[a]",]
            audio_codec = [
                "-c:a", "aac", # audio encoder
                "-r:a", "44100", # audio sample rate
                "-b:a", "128k", # audio bit rate
                "-ac", "2", # audio channels
            ]
        elif (self.merge_audio and second_audio_info):
            audio_map = ["-map", "1:a",]
        else:
            audio_map = ["-map", "0:a?",]

        if self.target_grid:
            stack_order = "[vpad][0:v:0]"
        else:
            stack_order = "[0:v:0][vpad]"

        if self.preserve_aspect_ratio:
            scale_width = "-1"
        else:
            scale_width = video_info['width']

        if (self.pad_second_video and (video_info['width'] < video_info['height'] / second_video_info['height'] * second_video_info['width'])):
            pad_filter = f"[1v]scale=w={video_info['width']}:h=-1[1scale];"\
                + f"[1scale]pad=w={video_info['width']}:h={video_info['height']}:x=(ow-iw)/2:y=(oh-ih)/2:color={self.hex_color}[vpad];"
        elif self.pad_second_video:
            pad_filter = f"[1v]pad=w={video_info['width']}:h={video_info['height']}:x=(ow-iw)/2:y=(oh-ih)/2:color={self.hex_color}[vpad];"
        else:
            pad_filter = f"[1v]null[vpad];"

        filters = [
            "-stream_loop", str(n_loops),
            "-i", self.second_video_path,
            "-t", str(video_info["duration"]),
            "-filter_complex",
            f"[1:v:0]scale=w={scale_width}:h={video_info['height']}[1v];"
            + pad_filter
            + f"{stack_order}hstack=inputs=2[hstack];"
            + f"[hstack]scale=w='min(iw,{self.max_width})':h=-1,setsar=ratio=1:1[vscale];"
            + f"[vscale]pad=w=ceil(iw/2)*2:h=ceil(ih/2)*2[v]" # ensure divisible by 2
            + audio_filter,
            "-map", "[v]",
            *audio_map,
            "-fps_mode", "cfr", # duplicate and drop frames for constant frame rate
            "-r", str(video_info['r_frame_rate']),
            *audio_codec,
        ]
        
        return self.standard_filter_fmt(video_path, filters, output_path)
