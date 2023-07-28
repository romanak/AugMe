from math import ceil
from typing import List, Tuple
from augme.video.ffmpeg.base_augmenter import BaseFFMPEGAugmenter
from augme.video.helpers import (
    get_video_info,
    get_audio_info,
    validate_path,
    validate_rgb_color,
)


class VideoAugmenterByFStack(BaseFFMPEGAugmenter):
    def __init__(
        self,
        second_video_path: str,
        third_video_path: str,
        forth_video_path: str,
        merge_audio: bool,
        target_grid: int,
        preserve_aspect_ratio: bool,
        pad_video: bool,
        pad_color: Tuple[int, int, int],
        max_height: int,
    ):
        assert target_grid in [0,1,2,3], "Valid target_grid is one of 0,1,2,3"
        validate_rgb_color(pad_color)
        video_paths = [second_video_path, third_video_path, forth_video_path]
        [validate_path(path) for path in video_paths]

        self.video_paths = video_paths
        self.merge_audio = merge_audio
        self.target_grid = target_grid
        self.preserve_aspect_ratio = preserve_aspect_ratio
        self.pad_video = pad_video
        self.hex_color = "%02x%02x%02x" % pad_color
        self.max_height = max_height


    def get_command(self, video_path: str, output_path: str) -> List[str]:
        """
        Stacks four videos in a grid

        @param video_path: the path to the video to be augmented

        @param output_path: the path in which the resulting video will be stored.
            If not passed in, the original video file will be overwritten

        @returns: a list of strings containing the CLI FFMPEG command for
            the augmentation
        """
        video_info = get_video_info(video_path)
        audio_info = get_audio_info(video_path)

        video_infos = [get_video_info(path) for path in self.video_paths]
        audio_infos = [get_audio_info(path) for path in self.video_paths]

        duration = video_info['duration']
        n_loops = [ceil(duration / vinfo['duration']) for vinfo in video_infos]

        audio_filter = ""
        audio_codec = ["-c:a", "copy",]
        if (self.merge_audio and audio_info and audio_infos[0] and audio_infos[1] and audio_infos[2]):
            audio_filter = ";[0:a:0][1:a:0][2:a:0][3:a:0]amerge=inputs=4,pan=stereo|c0<c0+c2+c4+c6|c1<c1+c3+c5+c7[a]"
            audio_map = ["-map",  "[a]",]
            audio_codec = [
                "-c:a", "aac", # audio encoder
                "-r:a", "44100", # audio sample rate
                "-b:a", "128k", # audio bit rate
                "-ac", "2", # audio channels
            ]
        else:
            audio_map = ["-map", "0:a?",]

        if self.target_grid == 0:
            stack_order_h1 = "[0:v:0][1pad]"
            stack_order_h2 = "[2pad][3pad]"
        elif self.target_grid == 1:
            stack_order_h1 = "[1pad][0:v:0]"
            stack_order_h2 = "[2pad][3pad]"
        elif self.target_grid == 2:
            stack_order_h1 = "[1pad][2pad]"
            stack_order_h2 = "[0:v:0][3pad]"
        elif self.target_grid == 3:
            stack_order_h1 = "[1pad][2pad]"
            stack_order_h2 = "[3pad][0:v:0]"
            

        if self.preserve_aspect_ratio:
            scale_width = "-1"
        else:
            scale_width = video_info['width']

        video_filters = []
        for i in range(len(video_infos)):
            video_filter = f"[{i+1}:v:0]scale=w={scale_width}:h={video_info['height']}[{i+1}v];"
            if (self.pad_video and (video_info['width'] < video_info['height'] / video_infos[i]['height'] * video_infos[i]['width'])):
                video_filter += f"[{i+1}v]scale=w={video_info['width']}:h=-1[{i+1}scale];"\
                    + f"[{i+1}scale]pad=w={video_info['width']}:h={video_info['height']}:x=(ow-iw)/2:y=(oh-ih)/2:color={self.hex_color}[{i+1}pad];"
            elif self.pad_video:
                video_filter += f"[{i+1}v]pad=w={video_info['width']}:h={video_info['height']}:x=(ow-iw)/2:y=(oh-ih)/2:color={self.hex_color}[{i+1}pad];"
            else:
                video_filter += f"[{i+1}v]null[{i+1}pad];"
            video_filters.append(video_filter)

        filters = [
            "-stream_loop", str(n_loops[0]),
            "-i", self.video_paths[0],
            "-t", f"{video_info['duration']}",
            "-stream_loop", str(n_loops[1]),
            "-i", self.video_paths[1],
            "-t", f"{video_info['duration']}",
            "-stream_loop", str(n_loops[2]),
            "-i", self.video_paths[2],
            "-t", f"{video_info['duration']}",
            "-filter_complex",
            "".join(video_filters)
            + f"{stack_order_h1}hstack=inputs=2[1hstack];"
            + f"{stack_order_h2}hstack=inputs=2[2hstack];"
            + f"[2hstack][1hstack]scale2ref=w=oh*mdar:h=-1[2hs][1hs];"
            + f"[1hs][2hs]vstack=inputs=2[vstack];"
            + f"[vstack]scale=w=-1:h='min(ih,{self.max_height})',setsar=ratio=1:1[vscale];"
            + f"[vscale]pad=w=ceil(iw/2)*2:h=ceil(ih/2)*2[v]" # ensure divisible by 2
            + audio_filter,
            "-map", "[v]",
            *audio_map,
            "-fps_mode", "cfr", # duplicate and drop frames for constant frame rate
            "-r", str(video_info['r_frame_rate']),
            *audio_codec,
         ]

        return self.standard_filter_fmt(video_path, filters, output_path)
