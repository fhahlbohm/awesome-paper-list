from PIL import Image
from moviepy.editor import VideoFileClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_resize
from pathlib import Path


def compress_image(file: Path, target_resolution: tuple[int, int]) -> None:
    with Image.open(file) as image:
        if file.suffix.lower() in ['.jpg', '.jpeg'] and image.size == target_resolution:
            return
        image.thumbnail(target_resolution)
        offset = (max((target_resolution[0] - image.size[0]) // 2, 0), max((target_resolution[1] - image.size[1]) // 2, 0))
        image_out = Image.new(mode='RGB', size=target_resolution, color=(255, 255, 255))
        image_out.paste(image, offset)
        file_out = file.parent / f'{file.stem}.jpg'
        image_out.save(file_out, 'JPEG')
    if file_out != file:
        file.unlink()


def compress_video(file: Path, target_resolution: tuple[int, int]):
    with VideoFileClip(str(file), audio=False) as video:
        width, height = video.size
        if width == target_resolution[0] or height == target_resolution[1]:
            return
        video_new = video.set_fps(30)
        file_tmp = file.parent / f'{file.stem}_tmp.mp4'
        video_new.write_videofile(str(file_tmp), codec='libx264', audio=False)
    aspect_ratio = width / height
    target_aspect_ratio = target_resolution[0] / target_resolution[1]
    if aspect_ratio > target_aspect_ratio:
        target_resolution = (target_resolution[0], round(target_resolution[0] / aspect_ratio))
    else:
        target_resolution = (round(target_resolution[1] * aspect_ratio), target_resolution[1])
    file_out = file.parent / f'{file.stem}.mp4'
    file.unlink()
    ffmpeg_resize(str(file_tmp), str(file_out), target_resolution)
    file_tmp.unlink()


def compress_assets(path: Path, target_resolution: tuple[int, int]) -> None:
    for file in path.glob('*'):
        if file.suffix.lower() in ['.jpg', '.jpeg', '.png']:
            compress_image(file, target_resolution)
        elif file.suffix.lower() in ['.mp4']:
            compress_video(file, target_resolution)
