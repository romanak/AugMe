import shutil
import subprocess
from typing import Any, Dict, List, Optional, Tuple, Union
import json
import re
import os
from pathlib import Path


FFMPEG_PATH = ffmpeg = shutil.which('ffmpeg')
FFPROBE_PATH = shutil.which('ffprobe')


def execute_ffmpeg_cmd(cmd, timeout=3600):
    cmd.insert(0, FFMPEG_PATH)
    print(*cmd)

    process = subprocess.Popen(
        cmd,
        bufsize=1,
        text=True,
        encoding='utf-8'
    )
    try:
        (stdout, stderr) = process.communicate(input=None, timeout=timeout)
    except subprocess.TimeoutExpired:
        process.kill()


def execute_ffprobe_cmd(cmd, timeout=30):
    cmd.insert(0, FFPROBE_PATH)
    print(*cmd)

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=timeout
        )
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while executing {command}")
        print(e.output)
    except subprocess.TimeoutExpired:
        print(f"Timeout error occurred while executing {command}")

    return result


def execute_ffmpeg_capture_cmd(cmd, timeout=3600):
    cmd.insert(0, FFMPEG_PATH)
    print(*cmd)

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=timeout
        )
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while executing {command}")
        print(e.output)
    except subprocess.TimeoutExpired:
        print(f"Timeout error occurred while executing {command}")

    return result


def get_video_fps(frame_rate: str) -> Optional[float]:
    try:
        # ffmpeg often returns fractional framerates, e.g. 225480/7523
        if "/" in frame_rate:
            num, denom = (float(f) for f in frame_rate.split("/"))
            return num / denom
        else:
            return float(frame_rate)
    except Exception:
        return 0


def get_precise_duration(input_file: str) -> Optional[float]:
    cmd = [
        # '-v', 'quiet', # produce only minimal output
        '-i', input_file,
        '-f', "null",
        '-',
    ]
    result = execute_ffmpeg_capture_cmd(cmd)

    # Match the regular expression pattern
    pattern = r"time=(\d{2}):(\d{2}):(\d{2})\.(\d{2})"
    # pattern = "hello world"
    match = re.findall(pattern, result.stderr)

    if match:
        # Extract the matched groups
        hours = int(match[-1][0])
        minutes = int(match[-1][1])
        seconds = int(match[-1][2])
        milliseconds = int(match[-1][3])
        total_seconds = (hours * 3600) + (minutes * 60) + seconds + (milliseconds / 100)
        return total_seconds
    else:
        return 0


def get_media_info(
        input_file: str
    ) -> Tuple[
        List[Optional[Dict[str, Any]]],
        List[Optional[Dict[str, Any]]],
        List[Optional[Dict[str, Any]]],
    ]:
    video_metadata = []
    audio_metadata = []
    subtitle_metadata = []

    cmd = [
        '-v', 'quiet', # produce only minimal output
        '-print_format', 'json',  # print output in JSON format
        '-show_streams', #  display detailed information about the selected streams
        input_file
    ]
    result = execute_ffprobe_cmd(cmd)

    # Parse the output as JSON
    if result:
        output_json = json.loads(result.stdout)

        if ('streams' in output_json) and (len(output_json['streams']) > 0):

            # Extract video and audio stream metadata
            video_metadata = [
                s for s in output_json['streams'] if s['codec_type'] == 'video'
            ]
            audio_metadata = [
                s for s in output_json['streams'] if s['codec_type'] == 'audio'
            ]
            subtitle_metadata = [
                s for s in output_json['streams'] if s['codec_type'] == 'subtitle'
            ]

            # Convert fraction to decimal point representation of frame rates
            for stream in video_metadata:
                avg_frame_rate = stream.get('avg_frame_rate', 0)
                stream['avg_frame_rate'] = get_video_fps(avg_frame_rate)
                r_frame_rate = stream.get('r_frame_rate', 0)
                stream['r_frame_rate'] = get_video_fps(r_frame_rate)
                stream['duration'] = float(stream.get('duration', 0)) or get_precise_duration(input_file)

    return (video_metadata, audio_metadata, subtitle_metadata)

def get_video_info(input_file: str) -> Optional[Dict[str, Any]]:
    (video_metadata, audio_metadata, subtitle_metadata) = get_media_info(input_file)
    if len(video_metadata) > 0:
        return video_metadata[0]

def get_audio_info(input_file: str) -> Optional[Dict[str, Any]]:
    (video_metadata, audio_metadata, subtitle_metadata) = get_media_info(input_file)
    if len(audio_metadata) > 0:
        return audio_metadata[0]

def extract_frames(
    video_path: str,
    output_dir: str,
    fps: Union[int, float],
    quality: Union[int, float] = 5,
) -> Optional[Any]:
    """
    Extract frames from the video at fps rate and save them as JPEG images
    to the specified directory.

    @param video_path: the path to the video that will be stacked on top

    @param output_dir: the path to the directory to extract the frames

    @param fps: frames per second rate, i.e. fps=0.5 means 1 frame every 2 seconds

    @param quality: the quality of the output jpeg image, 2 is best, 31 is worst

    @returns: None
    """
    fps = float(fps)
    quality = int(quality)
    assert 2 <= quality <= 31, "Quality must be a number in the range [2, 31]"
    assert fps > 0, "FPS must be greater than zero"
    os.makedirs(output_dir, exist_ok=True)
    filename = Path(video_path).stem

    cmd = [
        "-y",
        "-i", video_path,
        "-vf", f"fps={fps}",
        "-qscale:v", str(quality),
        f"{output_dir}/{filename}_%06d.jpg",
    ]

    execute_ffmpeg_cmd(cmd)
