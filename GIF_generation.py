import os
from datetime import datetime
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

# 用户参数
input_video = "output_result.mp4"
start_time = 1
end_time = 10
fps = 10
temp_clip = "temp_subclip.mp4"

# 截取视频
ffmpeg_extract_subclip(input_video, start_time, end_time, temp_clip)

# 读取截取后的视频
clip = VideoFileClip(temp_clip)

# 自动生成输出 GIF 文件名：原名 + 时间戳
base_name = os.path.splitext(os.path.basename(input_video))[0]
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_gif = f"{base_name}_{timestamp}.gif"

# 输出 GIF
clip.write_gif(output_gif, fps=fps)
print(f"GIF 已生成: {output_gif}")

# 关闭资源
clip.close()

# 删除临时文件
if os.path.exists(temp_clip):
    os.remove(temp_clip)
