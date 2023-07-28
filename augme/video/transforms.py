import os
import random
from typing import Any, Callable, Dict, List, Optional, Tuple
from augme.video import functional as F
from augme.video import helpers


class VidAugBaseClass(object):
    def __init__(self, p: float = 1.0):
        """
        @param p: the probability of the transform being applied; default value is 1.0
        """
        assert 0 <= p <= 1.0, "p must be a value in the range [0, 1]"
        self.p = p

    def __call__(self, *args, **kwargs) -> Any:
        """
        This function is to be implemented in the child classes.
        From this function, call the transform to be applied
        """
        raise NotImplementedError()


class BaseTransform(VidAugBaseClass):
    def __call__(
        self,
        video_path: str,
        output_path: Optional[str] = None,
        force: bool = False,
        seed: Optional[int] = None,
        metadata: Optional[List[Dict[str, Any]]] = None,
    ) -> str:
        """
        @param video_path: the path to the video to be augmented

        @param output_path: the path in which the resulting video will be stored.
            If not passed in, the original video file will be overwritten

        @param force: if set to True, the transform will be applied. Otherwise,
            application is determined by the probability set

        @param seed: if provided, the random seed will be set to this before calling
            the transform

        @param metadata: if set to be a list, metadata about the function execution
            including its name, the source & dest duration, fps, etc. will be appended
            to the inputted list. If set to None, no metadata will be appended or returned

        @returns: the path to the augmented video
        """
        assert type(force) == bool, "Expected type bool for variable `force`"

        if not force and random.random() > self.p:
            return video_path

        if seed is not None:
            random.seed(seed)

        return self.apply_transform(video_path, output_path or video_path, metadata)

    def apply_transform(
        self,
        video_path: str,
        output_path: str,
        metadata: Optional[List[Dict[str, Any]]] = None,
    ) -> str:
        """
        This function is to be implemented in the child classes.
        From this function, call the augmentation function with the
        parameters specified
        """
        raise NotImplementedError()


class AddNoise(BaseTransform):
    def __init__(
        self,
        level: int = 100000,
        add_audio_noise: bool = False,
        p: float = 1.0,
    ):
        """
        @param level: apply noise to every byte for video and every bit for audio
            but don't drop any packets.

        @param add_audio_noise: add noise to video and audio together, rather than
            add noise only to video.

        @param p: the probability of the transform being applied; default value is 1.0
        """
        super().__init__(p)
        self.level = level
        self.add_audio_noise = add_audio_noise

    def apply_transform(
        self,
        video_path: str,
        output_path: str,
        metadata: Optional[List[Dict[str, Any]]] = None,
    ) -> str:
        """
        Adds noise to a video

        @param video_path: the path to the video to be augmented

        @param output_path: the path in which the resulting video will be stored.
            If not passed in, the original video file will be overwritten

        @param metadata: if set to be a list, metadata about the function execution
            including its name, the source & dest duration, fps, etc. will be appended
            to the inputted list. If set to None, no metadata will be appended or returned

        @returns: the path to the augmented video
        """
        return F.add_noise(video_path, output_path, self.level,
            self.add_audio_noise, metadata=metadata)


class AddSilentAudio(BaseTransform):
    def apply_transform(
        self,
        video_path: str,
        output_path: str,
        metadata: Optional[List[Dict[str, Any]]] = None,
    ) -> str:
        """
        Adds silent audio to a video

        @param video_path: the path to the video to be augmented

        @param output_path: the path in which the resulting video will be stored.
            If not passed in, the original video file will be overwritten

        @param metadata: if set to be a list, metadata about the function execution
            including its name, the source & dest duration, fps, etc. will be appended
            to the inputted list. If set to None, no metadata will be appended or returned

        @returns: the path to the augmented video
        """
        return F.add_silent_audio(video_path, output_path, metadata=metadata)


class AudioSwap(BaseTransform):
    def __init__(
        self,
        audio_path: str,
        audio_offset: float = 0.0,
        p: float = 1.0,
    ):
        """
        @param audio_path: the path to the audio you'd like to swap with the
            video's audio

        @param audio_offset: starting point in seconds such that an audio clip of offset to
            offset + video_duration is used in the audio swap. Default value is zero

        @param p: the probability of the transform being applied; default value is 1.0
        """
        super().__init__(p)
        self.audio_path = audio_path
        self.audio_offset = audio_offset

    def apply_transform(
        self,
        video_path: str,
        output_path: str,
        metadata: Optional[List[Dict[str, Any]]] = None,
    ) -> str:
        """
        Swaps the video audio for the given audio starting from an offset

        @param video_path: the path to the video to be augmented

        @param output_path: the path in which the resulting video will be stored.
            If not passed in, the original video file will be overwritten

        @param metadata: if set to be a list, metadata about the function execution
            including its name, the source & dest duration, fps, etc. will be appended
            to the inputted list. If set to None, no metadata will be appended or returned

        @returns: the path to the augmented video
        """
        return F.audio_swap(
            video_path, self.audio_path, output_path, self.audio_offset, metadata=metadata
        )


class BlendVideos(BaseTransform):
    def __init__(
        self,
        overlay_path: str,
        opacity: float = 0.5,
        merge_audio: bool = False,
        p: float = 1.0,
    ):
        """
        @param overlay_path: the path to the video that will be overlaid onto the
            background video

        @param opacity: the lower the opacity, the more transparent the overlaid video

        @param merge_audio: merge the audio of the background and overlaid videos
        together

        @param p: the probability of the transform being applied; default value is 1.0
        """
        super().__init__(p)
        self.overlay_path = overlay_path
        self.opacity = opacity
        self.merge_audio = merge_audio

    def apply_transform(
        self,
        video_path: str,
        output_path: str,
        metadata: Optional[List[Dict[str, Any]]] = None,
    ) -> str:
        """
        Blends two videos together

        @param video_path: the path to the video to be augmented

        @param output_path: the path in which the resulting video will be stored.
            If not passed in, the original video file will be overwritten

        @param metadata: if set to be a list, metadata about the function execution
            including its name, the source & dest duration, fps, etc. will be appended
            to the inputted list. If set to None, no metadata will be appended or returned

        @returns: the path to the augmented video
        """
        return F.blend_videos(
            video_path,
            self.overlay_path,
            output_path,
            self.opacity,
            self.merge_audio,
            metadata=metadata,
        )


class Blur(BaseTransform):
    def __init__(self, sigma: float = 1.0, p: float = 1.0):
        """
        @param sigma: horizontal sigma, standard deviation of Gaussian blur

        @param p: the probability of the transform being applied; default value is 1.0
        """
        super().__init__(p)
        self.sigma = sigma

    def apply_transform(
        self,
        video_path: str,
        output_path: str,
        metadata: Optional[List[Dict[str, Any]]] = None,
    ) -> str:
        """
        Blurs a video

        @param video_path: the path to the video to be augmented

        @param output_path: the path in which the resulting video will be stored.
            If not passed in, the original video file will be overwritten

        @param metadata: if set to be a list, metadata about the function execution
            including its name, the source & dest duration, fps, etc. will be appended
            to the inputted list. If set to None, no metadata will be appended or returned

        @returns: the path to the augmented video
        """
        return F.blur(video_path, output_path, self.sigma, metadata=metadata)


class Brightness(BaseTransform):
    def __init__(self, level: float = 0.15, p: float = 1.0):
        """
        @param level: the value must be a float value in range -1.0 to 1.0, where a
            negative value darkens and positive brightens

        @param p: the probability of the transform being applied; default value is 1.0
        """
        super().__init__(p)
        self.level = level

    def apply_transform(
        self,
        video_path: str,
        output_path: str,
        metadata: Optional[List[Dict[str, Any]]] = None,
    ) -> str:
        """
        Brightens or darkens a video

        @param video_path: the path to the video to be augmented

        @param output_path: the path in which the resulting video will be stored.
            If not passed in, the original video file will be overwritten

        @param metadata: if set to be a list, metadata about the function execution
            including its name, the source & dest duration, fps, etc. will be appended
            to the inputted list. If set to None, no metadata will be appended or returned

        @returns: the path to the augmented video
        """
        return F.brightness(
            video_path,
            output_path,
            level=self.level,
            metadata=metadata,
        )


class ChangeAspectRatio(BaseTransform):
    def __init__(self, ratio: float = 1.0, p: float = 1.0):
        """
        @param ratio: aspect ratio, i.e. width/height, of the new video

        @param p: the probability of the transform being applied; default value is 1.0
        """
        super().__init__(p)
        self.ratio = ratio

    def apply_transform(
        self,
        video_path: str,
        output_path: str,
        metadata: Optional[List[Dict[str, Any]]] = None,
    ) -> str:
        """
        Changes the sample aspect ratio attribute of the video, and resizes the
            video to reflect the new aspect ratio

        @param video_path: the path to the video to be augmented

        @param output_path: the path in which the resulting video will be stored.
            If not passed in, the original video file will be overwritten

        @param metadata: if set to be a list, metadata about the function execution
            including its name, the source & dest duration, fps, etc. will be appended
            to the inputted list. If set to None, no metadata will be appended or returned

        @returns: the path to the augmented video
        """
        return F.change_aspect_ratio(
            video_path, output_path, self.ratio, metadata=metadata
        )


class ChangeVideoSpeed(BaseTransform):
    def __init__(self, factor: float = 1.0, p: float = 1.0):
        """
        @param factor: the factor by which to alter the speed of the video. A factor
            less than one will slow down the video, a factor equal to one won't alter
            the video, and a factor greater than one will speed up the video

        @param p: the probability of the transform being applied; default value is 1.0
        """
        super().__init__(p)
        self.factor = factor

    def apply_transform(
        self,
        video_path: str,
        output_path: str,
        metadata: Optional[List[Dict[str, Any]]] = None,
    ) -> str:
        """
        Changes the speed of the video

        @param video_path: the path to the video to be augmented

        @param output_path: the path in which the resulting video will be stored.
            If not passed in, the original video file will be overwritten

        @param metadata: if set to be a list, metadata about the function execution
            including its name, the source & dest duration, fps, etc. will be appended
            to the inputted list. If set to None, no metadata will be appended or returned

        @returns: the path to the augmented video
        """
        return F.change_video_speed(
            video_path, output_path, self.factor, metadata=metadata
        )


class ColorJitter(BaseTransform):
    def __init__(
        self,
        brightness_factor: float = 0,
        contrast_factor: float = 1.0,
        saturation_factor: float = 1.0,
        p: float = 1.0,
    ):
        """
        @param brightness_factor: set the brightness expression. The value must be
            a float value in range -1.0 to 1.0. The default value is 0

        @param contrast_factor: set the contrast expression. The value must be a
            float value in range -1000.0 to 1000.0. The default value is 1

        @param saturation_factor: set the saturation expression. The value must be a
            float in range 0.0 to 3.0. The default value is 1

        @param p: the probability of the transform being applied; default value is 1.0
        """
        super().__init__(p)
        self.brightness_factor = brightness_factor
        self.contrast_factor = contrast_factor
        self.saturation_factor = saturation_factor

    def apply_transform(
        self,
        video_path: str,
        output_path: str,
        metadata: Optional[List[Dict[str, Any]]] = None,
    ) -> str:
        """
        Color jitters the video

        @param video_path: the path to the video to be augmented

        @param output_path: the path in which the resulting video will be stored.
            If not passed in, the original video file will be overwritten

        @param metadata: if set to be a list, metadata about the function execution
            including its name, the source & dest duration, fps, etc. will be appended
            to the inputted list. If set to None, no metadata will be appended or returned

        @returns: the path to the augmented video
        """
        return F.color_jitter(
            video_path,
            output_path,
            self.brightness_factor,
            self.contrast_factor,
            self.saturation_factor,
            metadata=metadata,
        )


class Concat(BaseTransform):
    def __init__(
        self,
        other_video_paths: List[str],
        src_video_path_index: int = 0,
        pad_color: Tuple[int, int, int] = helpers.DEFAULT_COLOR,
        p: float = 1.0,
    ):
        """
        @param other_video_paths: a list of paths to all the videos to be concatenated (in
            order)

        @param src_video_path_index: for metadata purposes, this indicates which video in
            the list `video_paths` should be considered the `source` or original video
        
        @param pad_color: RGB color for padding of other videos after resizing

        @param p: the probability of the transform being applied; default value is 1.0
        """
        super().__init__(p)
        self.other_video_paths = other_video_paths
        self.src_video_path_index = src_video_path_index
        self.pad_color = pad_color

    def apply_transform(
        self,
        video_path: str,
        output_path: str,
        metadata: Optional[List[Dict[str, Any]]] = None,
    ) -> str:
        """
        Concatenates videos together. Resizes all other videos to the size of the
        `source` video (video_paths[src_video_path_index]), preserving their aspect
        ratios

        @param video_path: the path to the video to be augmented

        @param output_path: the path in which the resulting video will be stored.
            If not passed in, the original video file will be overwritten

        @param metadata: if set to be a list, metadata about the function execution
            including its name, the source & dest duration, fps, etc. will be appended
            to the inputted list. If set to None, no metadata will be appended or returned

        @returns: the path to the augmented video
        """
        video_paths = (
            self.other_video_paths[: self.src_video_path_index]
            + [video_path]
            + self.other_video_paths[self.src_video_path_index :]
        )
        return F.concat(
            video_paths, output_path, self.src_video_path_index, self.pad_color,
            metadata=metadata,
        )


class Contrast(BaseTransform):
    def __init__(self, level: float = 1.0, p: float = 1.0):
        """
        @param level: the value must be a float value in range -1000.0 to 1000.0,
            where a negative value removes contrast and a positive value adds contrast

        @param p: the probability of the transform being applied; default value is 1.0
        """
        super().__init__(p)
        self.level = level

    def apply_transform(
        self,
        video_path: str,
        output_path: str,
        metadata: Optional[List[Dict[str, Any]]] = None,
    ) -> str:
        """
        Alters the contrast of a video

        @param video_path: the path to the video to be augmented

        @param output_path: the path in which the resulting video will be stored.
            If not passed in, the original video file will be overwritten

        @param metadata: if set to be a list, metadata about the function execution
            including its name, the source & dest duration, fps, etc. will be appended
            to the inputted list. If set to None, no metadata will be appended or returned

        @returns: the path to the augmented video
        """
        return F.contrast(video_path, output_path, self.level, metadata=metadata)


class Crop(BaseTransform):
    def __init__(
        self,
        left: float = 0.25,
        top: float = 0.25,
        right: float = 0.75,
        bottom: float = 0.75,
        p: float = 1.0,
    ):
        """
        @param left: left positioning of the crop; between 0 and 1, relative to
            the video width

        @param top: top positioning of the crop; between 0 and 1, relative to
            the video height

        @param right: right positioning of the crop; between 0 and 1, relative to
            the video width

        @param bottom: bottom positioning of the crop; between 0 and 1, relative to
            the video height

        @param p: the probability of the transform being applied; default value is 1.0
        """
        super().__init__(p)
        self.left, self.right, self.top, self.bottom = left, right, top, bottom

    def apply_transform(
        self,
        video_path: str,
        output_path: str,
        metadata: Optional[List[Dict[str, Any]]] = None,
    ) -> str:
        """
        Crops the video

        @param video_path: the path to the video to be augmented

        @param output_path: the path in which the resulting video will be stored.
            If not passed in, the original video file will be overwritten

        @param metadata: if set to be a list, metadata about the function execution
            including its name, the source & dest duration, fps, etc. will be appended
            to the inputted list. If set to None, no metadata will be appended or returned

        @returns: the path to the augmented video
        """
        return F.crop(
            video_path,
            output_path,
            self.left,
            self.top,
            self.right,
            self.bottom,
            metadata=metadata,
        )


class Emboss(BaseTransform):
    def apply_transform(
        self,
        video_path: str,
        output_path: str,
        metadata: Optional[List[Dict[str, Any]]] = None,
    ) -> str:
        """
        Emboss a video

        @param video_path: the path to the video to be augmented

        @param output_path: the path in which the resulting video will be stored.
            If not passed in, the original video file will be overwritten

        @param metadata: if set to be a list, metadata about the function execution
            including its name, the source & dest duration, fps, etc. will be appended
            to the inputted list. If set to None, no metadata will be appended or returned

        @returns: the path to the augmented video
        """
        return F.emboss(
            video_path,
            output_path,
            metadata=metadata,
        )


class EncodingQuality(BaseTransform):
    def __init__(self, quality: int = 23, p: float = 1.0):
        """
        @param quality: CRF scale is 0–51, where 0 is lossless, 23 is the default,
            and 51 is worst quality possible. A lower value generally leads to higher
            quality, and a subjectively sane range is 17–28

        @param p: the probability of the transform being applied; default value is 1.0
        """
        super().__init__(p)
        self.quality = quality

    def apply_transform(
        self,
        video_path: str,
        output_path: str,
        metadata: Optional[List[Dict[str, Any]]] = None,
    ) -> str:
        """
        Alters the encoding quality of a video

        @param video_path: the path to the video to be augmented

        @param output_path: the path in which the resulting video will be stored.
            If not passed in, the original video file will be overwritten

        @param metadata: if set to be a list, metadata about the function execution
            including its name, the source & dest duration, fps, etc. will be appended
            to the inputted list. If set to None, no metadata will be appended or returned

        @returns: the path to the augmented video
        """
        return F.encoding_quality(
            video_path,
            output_path,
            quality=int(self.quality),
            metadata=metadata,
        )


class FPS(BaseTransform):
    def __init__(self, fps: int = 15, p: float = 1.0):
        """
        @param fps: the desired output frame rate. Note that a FPS value greater than
            the original FPS of the video will result in an unaltered video

        @param p: the probability of the transform being applied; default value is 1.0
        """
        super().__init__(p)
        self.fps = fps

    def apply_transform(
        self,
        video_path: str,
        output_path: str,
        metadata: Optional[List[Dict[str, Any]]] = None,
    ) -> str:
        """
        Alters the FPS of a video

        @param video_path: the path to the video to be augmented

        @param output_path: the path in which the resulting video will be stored.
            If not passed in, the original video file will be overwritten

        @param metadata: if set to be a list, metadata about the function execution
            including its name, the source & dest duration, fps, etc. will be appended
            to the inputted list. If set to None, no metadata will be appended or returned

        @returns: the path to the augmented video
        """
        return F.fps(video_path, output_path, self.fps, metadata=metadata)


class FStack(BaseTransform):
    def __init__(
        self,
        second_video_path: str,
        third_video_path: str,
        fourth_video_path: str,
        merge_audio: bool = False,
        target_grid: int = 0,
        preserve_aspect_ratio: bool = False,
        pad_video: bool = False,
        pad_color: Tuple[int, int, int] = helpers.DEFAULT_COLOR,
        max_height: int = 1920,
        p: float = 1.0,
    ):
        """
        @param second_video_path: the path to the video that will be stacked on
        the top right

        @param third_video_path: the path to the video that will be stacked on
        the bottom left

        @param fourth_video_path: the path to the video that will be stacked on
        the bottom right

        @param output_path: the path in which the resulting video will be stored.
            If not passed in, the original video file will be overwritten

        @param merge_audio: if set to True, the audio from all four videos will
            be merged

        @param target_grid: where to put the target video. 0 for top left (default),
            1 for top right, 2 for bottom left, 3 for bottom right.

        @param preserve_aspect_ratio: keep the original aspect ratio of the second
            video

        @param pad_video: if set to True, all other videos will be padded

        @param pad_color: RGB color for padding of other videos

        @param max_height: resize the output video preserving the aspect ratio if
            the height exceeds the specified value

        @param p: the probability of the transform being applied; default value is 1.0
        """
        super().__init__(p)
        self.second_video_path = second_video_path
        self.third_video_path = third_video_path
        self.fourth_video_path = fourth_video_path
        self.merge_audio = merge_audio
        self.target_grid = target_grid
        self.preserve_aspect_ratio = preserve_aspect_ratio
        self.pad_video = pad_video
        self.pad_color = pad_color
        self.max_height = max_height

    def apply_transform(
        self,
        video_path: str,
        output_path: str,
        metadata: Optional[List[Dict[str, Any]]] = None,
    ) -> str:
        """
        Stack four videos in a grid

        @param video_path: the path to the video to be augmented

        @param output_path: the path in which the resulting video will be stored.
            If not passed in, the original video file will be overwritten

        @param metadata: if set to be a list, metadata about the function execution
            including its name, the source & dest duration, fps, etc. will be appended
            to the inputted list. If set to None, no metadata will be appended or returned

        @returns: the path to the augmented video
        """
        return F.fstack(
            video_path,
            self.second_video_path,
            self.third_video_path,
            self.fourth_video_path,
            output_path,
            self.merge_audio,
            self.target_grid,
            self.preserve_aspect_ratio,
            self.pad_video,
            self.pad_color,
            self.max_height,
            metadata=metadata,
        )


class Gradient(BaseTransform):
    def apply_transform(
        self,
        video_path: str,
        output_path: str,
        metadata: Optional[List[Dict[str, Any]]] = None,
    ) -> str:
        """
        Overlay a horizontal gradient onto a video

        @param video_path: the path to the video to be augmented

        @param output_path: the path in which the resulting video will be stored.
            If not passed in, the original video file will be overwritten

        @param metadata: if set to be a list, metadata about the function execution
            including its name, the source & dest duration, fps, etc. will be appended
            to the inputted list. If set to None, no metadata will be appended or returned

        @returns: the path to the augmented video
        """
        return F.gradient(
            video_path,
            output_path,
            metadata=metadata,
        )


class Grayscale(BaseTransform):
    def apply_transform(
        self,
        video_path: str,
        output_path: str,
        metadata: Optional[List[Dict[str, Any]]] = None,
    ) -> str:
        """
        Changes a video to be grayscale

        @param video_path: the path to the video to be augmented

        @param output_path: the path in which the resulting video will be stored.
            If not passed in, the original video file will be overwritten

        @param metadata: if set to be a list, metadata about the function execution
            including its name, the source & dest duration, fps, etc. will be appended
            to the inputted list. If set to None, no metadata will be appended or returned

        @returns: the path to the augmented video
        """
        return F.grayscale(video_path, output_path, metadata=metadata)


class HFlip(BaseTransform):
    def apply_transform(
        self,
        video_path: str,
        output_path: str,
        metadata: Optional[List[Dict[str, Any]]] = None,
    ) -> str:
        """
        Horizontally flips a video

        @param video_path: the path to the video to be augmented

        @param output_path: the path in which the resulting video will be stored.
            If not passed in, the original video file will be overwritten

        @param metadata: if set to be a list, metadata about the function execution
            including its name, the source & dest duration, fps, etc. will be appended
            to the inputted list. If set to None, no metadata will be appended or returned

        @returns: the path to the augmented video
        """
        return F.hflip(video_path, output_path, metadata=metadata)


class HStack(BaseTransform):
    def __init__(
        self,
        second_video_path: str,
        merge_audio: bool = False,
        target_grid: int = 0,
        preserve_aspect_ratio: bool = False,
        pad_second_video: bool = False,
        pad_color: Tuple[int, int, int] = helpers.DEFAULT_COLOR,
        max_width: int = 1920,
        p: float = 1.0,
    ):
        """
        @param second_video_path: the path to the video that will be stacked on
        the right

        @param output_path: the path in which the resulting video will be stored.
            If not passed in, the original video file will be overwritten

        @param merge_audio: if set to True, the audio from both videos will be merged

        @param target_grid: where to put the target video. 0 for left (default),
            1 for right.

        @param preserve_aspect_ratio: keep the original aspect ratio of the second
            video

        @param pad_second_video: if set to True, the second video will be padded

        @param pad_color: RGB color for padding of second video

        @param max_width: resize the output video preserving the aspect ratio if
            the width exceeds the specified value

        @param p: the probability of the transform being applied; default value is 1.0
        """
        super().__init__(p)
        self.second_video_path = second_video_path
        self.merge_audio = merge_audio
        self.target_grid = target_grid
        self.preserve_aspect_ratio = preserve_aspect_ratio
        self.pad_second_video = pad_second_video
        self.pad_color = pad_color
        self.max_width = max_width

    def apply_transform(
        self,
        video_path: str,
        output_path: str,
        metadata: Optional[List[Dict[str, Any]]] = None,
    ) -> str:
        """
        Horizontally stacks two videos

        @param video_path: the path to the video to be augmented

        @param output_path: the path in which the resulting video will be stored.
            If not passed in, the original video file will be overwritten

        @param metadata: if set to be a list, metadata about the function execution
            including its name, the source & dest duration, fps, etc. will be appended
            to the inputted list. If set to None, no metadata will be appended or returned

        @returns: the path to the augmented video
        """
        return F.hstack(
            video_path,
            self.second_video_path,
            output_path,
            self.merge_audio,
            self.target_grid,
            self.preserve_aspect_ratio,
            self.pad_second_video,
            self.pad_color,
            self.max_width,
            metadata=metadata,
        )


class InsertInBackground(BaseTransform):
    def __init__(
        self,
        background_path: Optional[str] = None,
        start: Optional[float] = None,
        end: Optional[float] = None,
        background_offset: Optional[float] = None,
        pad_color: Tuple[int, int, int] = helpers.DEFAULT_COLOR,
        p: float = 1.0,
    ):
        """
        @param background_path: the path to the video in which to insert the main
            video

        @param start: start time in seconds from which the video will be inserted into
            the background video

        @param end: end time in seconds until which the video will be inserted into
            the background video

        @param background_offset: the point measured in seconds in the background
            video from which the main video starts to play

        @param pad_color: the pad color of the video after resizing it to the size
            of the background video, preserving the aspect ratio


        @param p: the probability of the transform being applied; default value is 1.0
        """
        super().__init__(p)
        self.background_path = background_path
        self.start = start
        self.end = end
        self.background_offset = background_offset
        self.pad_color = pad_color

    def apply_transform(
        self,
        video_path: str,
        output_path: str,
        metadata: Optional[List[Dict[str, Any]]] = None,
    ) -> str:
        """
        Insert the video in the middle of the background video

        @param video_path: the path to the video to be augmented

        @param output_path: the path in which the resulting video will be stored.
            If not passed in, the original video file will be overwritten

        @param metadata: if set to be a list, metadata about the function execution
            including its name, the source & dest duration, fps, etc. will be appended
            to the inputted list. If set to None, no metadata will be appended or returned

        @returns: the path to the augmented video
        """
        return F.insert_in_background(
            video_path,
            self.background_path,
            output_path,
            self.start,
            self.end,
            self.background_offset,
            self.pad_color,
            metadata=metadata,
        )


class Loop(BaseTransform):
    def __init__(self, num_loops: int = 0, p: float = 1.0):
        """
        @param num_loops: the number of times to loop the video. 0 means that the
            video will play once (i.e. no loops)

        @param p: the probability of the transform being applied; default value is 1.0
        """
        super().__init__(p)
        self.num_loops = num_loops

    def apply_transform(
        self,
        video_path: str,
        output_path: str,
        metadata: Optional[List[Dict[str, Any]]] = None,
    ) -> str:
        """
        Loops a video `num_loops` times

        @param video_path: the path to the video to be augmented

        @param output_path: the path in which the resulting video will be stored.
            If not passed in, the original video file will be overwritten

        @param metadata: if set to be a list, metadata about the function execution
            including its name, the source & dest duration, fps, etc. will be appended
            to the inputted list. If set to None, no metadata will be appended or returned

        @returns: the path to the augmented video
        """
        return F.loop(video_path, output_path, self.num_loops, metadata=metadata)


class Overlay(BaseTransform):
    def __init__(
        self,
        overlay_path: str,
        overlay_size: Optional[float] = None,
        x_factor: float = 0.0,
        y_factor: float = 0.0,
        merge_audio: bool = False,
        metadata: Optional[List[Dict[str, Any]]] = None,
        p: float = 1.0,
    ):
        """
        @param overlay_path: the path to the media (image or video) that will be
            overlaid onto the video

        @param overlay_size: size of the overlaid media with respect to the background
            video. If set to None, the original size of the overlaid media is used

        @param x_factor: specifies where the left side of the overlaid media should be
            placed, relative to the video width

        @param y_factor: specifies where the top side of the overlaid media should be
            placed, relative to the video height

        @param merge_audio: if set to True and the media type is a video, the
            audio of the overlaid video will be merged with the main/background
            video's audio

        @param p: the probability of the transform being applied; default value is 1.0
        """
        super().__init__(p)
        self.overlay_path = overlay_path
        self.overlay_size = overlay_size
        self.x_factor = x_factor
        self.y_factor = y_factor
        self.merge_audio = merge_audio

    def apply_transform(
        self,
        video_path: str,
        output_path: str,
        metadata: Optional[List[Dict[str, Any]]] = None,
    ) -> str:
        """
        Overlays media onto the video at position (width * x_factor, height * y_factor)

        @param video_path: the path to the video to be augmented

        @param output_path: the path in which the resulting video will be stored.
            If not passed in, the original video file will be overwritten

        @param metadata: if set to be a list, metadata about the function execution
            including its name, the source & dest duration, fps, etc. will be appended
            to the inputted list. If set to None, no metadata will be appended or returned

        @returns: the path to the augmented video
        """
        return F.overlay(
            video_path,
            self.overlay_path,
            output_path,
            self.overlay_size,
            self.x_factor,
            self.y_factor,
            self.merge_audio,
            metadata=metadata,
        )


class OverlayEmoji(BaseTransform):
    def __init__(
        self,
        emoji_path: str = helpers.EMOJI_PATH,
        x_factor: float = 0.4,
        y_factor: float = 0.4,
        opacity: float = 1.0,
        emoji_size: float = 0.15,
        p: float = 1.0,
    ):
        """
        @param emoji_path: path to the emoji image

        @param x_factor: specifies where the left side of the emoji should be
            placed, relative to the video width

        @param y_factor: specifies where the top side of the emoji should be placed,
            relative to the video height

        @param opacity: opacity of the emoji image

        @param emoji_size: emoji size relative to the height of the video frame

        @param p: the probability of the transform being applied; default value is 1.0
        """
        super().__init__(p)
        self.emoji_path = emoji_path
        self.x_factor = x_factor
        self.y_factor = y_factor
        self.opacity = opacity
        self.emoji_size = emoji_size

    def apply_transform(
        self,
        video_path: str,
        output_path: str,
        metadata: Optional[List[Dict[str, Any]]] = None,
    ) -> str:
        """
        Overlays an emoji onto each frame of a video

        @param video_path: the path to the video to be augmented

        @param output_path: the path in which the resulting video will be stored.
            If not passed in, the original video file will be overwritten

        @param metadata: if set to be a list, metadata about the function execution
            including its name, the source & dest duration, fps, etc. will be appended
            to the inputted list. If set to None, no metadata will be appended or returned

        @returns: the path to the augmented video
        """
        return F.overlay_emoji(
            video_path,
            output_path,
            self.emoji_path,
            self.x_factor,
            self.y_factor,
            self.opacity,
            self.emoji_size,
            metadata=metadata,
        )


class OverlayText(BaseTransform):
    def __init__(
        self,
        font: Optional[str] = helpers.FONT_PATH,
        fontsize: Optional[int] = 0.1,
        num_lines: int = 3,
        opacity: float = 0.5,
        p: float = 1.0,
    ):
        """
        @param font: a path to the font file. Note that font file is associated with
            different sets of characters (western, cyrillic, chinese, etc.)

        @param fontsize: the font size given as a factor of the video height

        @param num_lines: number of text lines

        @param opacity: the lower the opacity, the more transparent the overlaid video

        @param p: the probability of the transform being applied; default value is 1.0
        """
        super().__init__(p)
        self.font = font
        self.fontsize = fontsize
        self.num_lines = num_lines
        self.opacity = opacity

    def apply_transform(
        self,
        video_path: str,
        output_path: str,
        metadata: Optional[List[Dict[str, Any]]] = None,
    ) -> str:
        """
        Overlay random text onto a video

        @param video_path: the path to the video to be augmented

        @param output_path: the path in which the resulting video will be stored.
            If not passed in, the original video file will be overwritten

        @param metadata: if set to be a list, metadata about the function execution
            including its name, the source & dest duration, fps, etc. will be appended
            to the inputted list. If set to None, no metadata will be appended or returned

        @returns: the path to the augmented video
        """
        return F.overlay_text(
            video_path,
            output_path,
            self.font,
            self.fontsize,
            self.num_lines,
            self.opacity,
            metadata=metadata,
        )


class Pad(BaseTransform):
    def __init__(
        self,
        w_factor: float = 0.25,
        h_factor: float = 0.25,
        color: Tuple[int, int, int] = helpers.DEFAULT_COLOR,
        p: float = 1.0,
    ):
        """
        @param w_factor: pad right and left with w_factor * frame width

        @param h_factor: pad bottom and top with h_factor * frame height

        @param color: RGB color of the padded margin

        @param p: the probability of the transform being applied; default value is 1.0
        """
        super().__init__(p)
        self.w_factor, self.h_factor = w_factor, h_factor
        self.color = color

    def apply_transform(
        self,
        video_path: str,
        output_path: str,
        metadata: Optional[List[Dict[str, Any]]] = None,
    ) -> str:
        """
        Pads the video

        @param video_path: the path to the video to be augmented

        @param output_path: the path in which the resulting video will be stored.
            If not passed in, the original video file will be overwritten

        @param metadata: if set to be a list, metadata about the function execution
            including its name, the source & dest duration, fps, etc. will be appended
            to the inputted list. If set to None, no metadata will be appended or returned

        @returns: the path to the augmented video
        """
        return F.pad(
            video_path,
            output_path,
            self.w_factor,
            self.h_factor,
            self.color,
            metadata=metadata,
        )


class Pixelization(BaseTransform):
    def __init__(self, ratio: float = 1.0, p: float = 1.0):
        """
        @param ratio: smaller values result in a more pixelated image, 1.0 indicates
            no change, and any value above one doesn't have a noticeable effect

        @param p: the probability of the transform being applied; default value is 1.0
        """
        super().__init__(p)
        self.ratio = ratio

    def apply_transform(
        self,
        video_path: str,
        output_path: str,
        metadata: Optional[List[Dict[str, Any]]] = None,
    ) -> str:
        """
        Pixelizes the video

        @param video_path: the path to the video to be augmented

        @param output_path: the path in which the resulting video will be stored.
            If not passed in, the original video file will be overwritten

        @param metadata: if set to be a list, metadata about the function execution
            including its name, the source & dest duration, fps, etc. will be appended
            to the inputted list. If set to None, no metadata will be appended or returned

        @returns: the path to the augmented video
        """
        return F.pixelization(
            video_path,
            output_path,
            ratio=self.ratio,
            metadata=metadata,
        )


class RandomFrames(BaseTransform):
    def __init__(self, num_frames: int = 30, p: float = 1.0):
        """
        @param num_frames: the number of frames in the cache from which to
            take the next frame randomly without replacement for video output

        @param p: the probability of the transform being applied; default value is 1.0
        """
        super().__init__(p)
        self.num_frames = num_frames

    def apply_transform(
        self,
        video_path: str,
        output_path: str,
        metadata: Optional[List[Dict[str, Any]]] = None,
    ) -> str:
        """
        Flush video frames from internal cache of frames into a random order. No
            frame is discarded.

        @param video_path: the path to the video to be augmented

        @param output_path: the path in which the resulting video will be stored.
            If not passed in, the original video file will be overwritten

        @param metadata: if set to be a list, metadata about the function execution
            including its name, the source & dest duration, fps, etc. will be appended
            to the inputted list. If set to None, no metadata will be appended or returned

        @returns: the path to the augmented video
        """
        return F.random_frames(
            video_path,
            output_path,
            num_frames=self.num_frames,
            metadata=metadata,
        )


class RemoveAudio(BaseTransform):
    def apply_transform(
        self,
        video_path: str,
        output_path: str,
        metadata: Optional[List[Dict[str, Any]]] = None,
    ) -> str:
        """
        Removes the audio stream from a video

        @param video_path: the path to the video to be augmented

        @param output_path: the path in which the resulting video will be stored.
            If not passed in, the original video file will be overwritten

        @param metadata: if set to be a list, metadata about the function execution
            including its name, the source & dest duration, fps, etc. will be appended
            to the inputted list. If set to None, no metadata will be appended or returned

        @returns: the path to the augmented video
        """
        return F.remove_audio(video_path, output_path, metadata=metadata)


class Resize(BaseTransform):
    def __init__(
        self, width: Optional[int] = None, height: Optional[int] = None, p: float = 1.0
    ):
        """
        @param width: the width in which the video should be resized to. If None, the
            original video width will be used

        @param height: the height in which the video should be resized to. If None,
            the original video height will be used

        @param p: the probability of the transform being applied; default value is 1.0
        """
        super().__init__(p)
        self.width, self.height = width, height

    def apply_transform(
        self,
        video_path: str,
        output_path: str,
        metadata: Optional[List[Dict[str, Any]]] = None,
    ) -> str:
        """
        Resizes a video

        @param video_path: the path to the video to be augmented

        @param output_path: the path in which the resulting video will be stored.
            If not passed in, the original video file will be overwritten

        @param metadata: if set to be a list, metadata about the function execution
            including its name, the source & dest duration, fps, etc. will be appended
            to the inputted list. If set to None, no metadata will be appended or returned

        @returns: the path to the augmented video
        """
        return F.resize(
            video_path, output_path, self.width, self.height, metadata=metadata
        )


class Rotate(BaseTransform):
    def __init__(self, degrees: float = 15.0, p: float = 1.0):
        """
        @param degrees: expression for the angle by which to rotate the input video
            clockwise, expressed in degrees (supports negative values as well)

        @param p: the probability of the transform being applied; default value is 1.0
        """
        super().__init__(p)
        self.degrees = degrees

    def apply_transform(
        self,
        video_path: str,
        output_path: str,
        metadata: Optional[List[Dict[str, Any]]] = None,
    ) -> str:
        """
        Rotates a video

        @param video_path: the path to the video to be augmented

        @param output_path: the path in which the resulting video will be stored.
            If not passed in, the original video file will be overwritten

        @param metadata: if set to be a list, metadata about the function execution
            including its name, the source & dest duration, fps, etc. will be appended
            to the inputted list. If set to None, no metadata will be appended or returned

        @returns: the path to the augmented video
        """
        return F.rotate(video_path, output_path, self.degrees, metadata=metadata)


class Scale(BaseTransform):
    def __init__(self, factor: float = 0.5, p: float = 1.0):
        """
        @param factor: the ratio by which the video should be down-scaled or upscaled

        @param p: the probability of the transform being applied; default value is 1.0
        """
        super().__init__(p)
        self.factor = factor

    def apply_transform(
        self,
        video_path: str,
        output_path: str,
        metadata: Optional[List[Dict[str, Any]]] = None,
    ) -> str:
        """
        Alters the resolution of a video

        @param video_path: the path to the video to be augmented

        @param output_path: the path in which the resulting video will be stored.
            If not passed in, the original video file will be overwritten

        @param metadata: if set to be a list, metadata about the function execution
            including its name, the source & dest duration, fps, etc. will be appended
            to the inputted list. If set to None, no metadata will be appended or returned

        @returns: the path to the augmented video
        """
        return F.scale(video_path, output_path, self.factor, metadata=metadata)


class Transpose(BaseTransform):
    def __init__(self, direction: int = 0, p: float = 1.0):
        """
        @param direction: specify transposition direction and flip:
            0 - Rotate by 90 degrees counter-clockwise and flip vertically (default)
            1 - Rotate by 90 degrees clockwise
            2 - Rotate by 90 degrees counter-clockwise
            3 - Rotate by 90 degrees clockwise and flip vertically

        @param p: the probability of the transform being applied; default value is 1.0
        """
        super().__init__(p)
        self.direction = direction

    def apply_transform(
        self,
        video_path: str,
        output_path: str,
        metadata: Optional[List[Dict[str, Any]]] = None,
    ) -> str:
        """
        Transpose rows with columns in the input video and optionally flip it.

        @param video_path: the path to the video to be augmented

        @param output_path: the path in which the resulting video will be stored.
            If not passed in, the original video file will be overwritten

        @param metadata: if set to be a list, metadata about the function execution
            including its name, the source & dest duration, fps, etc. will be appended
            to the inputted list. If set to None, no metadata will be appended or returned

        @returns: the path to the augmented video
        """
        return F.transpose(video_path, output_path, self.direction, metadata=metadata)


class Trim(BaseTransform):
    def __init__(
        self, start: Optional[float] = None, end: Optional[float] = None, p: float = 1.0
    ):
        """
        @param start: starting point in seconds of when the trimmed video should start.
            If None, start will be 0

        @param end: ending point in seconds of when the trimmed video should end.
            If None, the end will be the duration of the video

        @param p: the probability of the transform being applied; default value is 1.0
        """
        super().__init__(p)
        self.start, self.end = start, end

    def apply_transform(
        self,
        video_path: str,
        output_path: str,
        metadata: Optional[List[Dict[str, Any]]] = None,
    ) -> str:
        """
        Trims the video using the specified start and end parameters

        @param video_path: the path to the video to be augmented

        @param output_path: the path in which the resulting video will be stored.
            If not passed in, the original video file will be overwritten

        @param metadata: if set to be a list, metadata about the function execution
            including its name, the source & dest duration, fps, etc. will be appended
            to the inputted list. If set to None, no metadata will be appended or returned

        @returns: the path to the augmented video
        """
        return F.trim(video_path, output_path, self.start, self.end, metadata=metadata)


class VFlip(BaseTransform):
    def apply_transform(
        self,
        video_path: str,
        output_path: str,
        metadata: Optional[List[Dict[str, Any]]] = None,
    ) -> str:
        """
        Vertically flips a video

        @param video_path: the path to the video to be augmented

        @param output_path: the path in which the resulting video will be stored.
            If not passed in, the original video file will be overwritten

        @param metadata: if set to be a list, metadata about the function execution
            including its name, the source & dest duration, fps, etc. will be appended
            to the inputted list. If set to None, no metadata will be appended or returned

        @returns: the path to the augmented video
        """
        return F.vflip(video_path, output_path, metadata=metadata)


class VStack(BaseTransform):
    def __init__(
        self,
        second_video_path: str,
        merge_audio: bool = False,
        target_grid: int = 0,
        preserve_aspect_ratio: bool = False,
        pad_second_video: bool = False,
        pad_color: Tuple[int, int, int] = helpers.DEFAULT_COLOR,
        max_height: int = 1920,
        p: float = 1.0,
    ):
        """
        @param second_video_path: the path to the video that will be stacked on
        the bottom

        @param output_path: the path in which the resulting video will be stored.
            If not passed in, the original video file will be overwritten

        @param merge_audio: if set to True, the audio from both videos will be merged

        @param target_grid: where to put the target video. 0 for top (default),
            1 for bottom.

        @param preserve_aspect_ratio: keep the original aspect ratio of the second
            video

        @param pad_second_video: if set to True, the second video will be padded

        @param pad_color: RGB color for padding of second video

        @param max_height: resize the output video preserving the aspect ratio if
            the height exceeds the specified value

        @param p: the probability of the transform being applied; default value is 1.0
        """
        super().__init__(p)
        self.second_video_path = second_video_path
        self.merge_audio = merge_audio
        self.target_grid = target_grid
        self.preserve_aspect_ratio = preserve_aspect_ratio
        self.pad_second_video = pad_second_video
        self.pad_color = pad_color
        self.max_height = max_height

    def apply_transform(
        self,
        video_path: str,
        output_path: str,
        metadata: Optional[List[Dict[str, Any]]] = None,
    ) -> str:
        """
        Vertically stacks two videos

        @param video_path: the path to the video to be augmented

        @param output_path: the path in which the resulting video will be stored.
            If not passed in, the original video file will be overwritten

        @param metadata: if set to be a list, metadata about the function execution
            including its name, the source & dest duration, fps, etc. will be appended
            to the inputted list. If set to None, no metadata will be appended or returned

        @returns: the path to the augmented video
        """
        return F.vstack(
            video_path,
            self.second_video_path,
            output_path,
            self.merge_audio,
            self.target_grid,
            self.preserve_aspect_ratio,
            self.pad_second_video,
            self.pad_color,
            self.max_height,
            metadata=metadata,
        )
