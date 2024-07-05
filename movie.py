import moviepy
import ides
from moviepy.editor import  concatenate_videoclips
from moviepy.editor import ImageClip, AudioFileClip
import moviepy.editor as mpy 

clips = []

id = "1bszocg"
com_ides = ["kxix00w","kxj5v6k","kxj6zqq"]


def create_clip(screenshot, audio):
    # Load the audio file to get its duration
    audioclip = AudioFileClip(audio)
    # Load the image and set its duration to match the audio duration
    imageclip = ImageClip(screenshot).set_duration(audioclip.duration)
    # Set the audio of the image clip
    videoclip = imageclip.set_audio(audioclip)
    return videoclip


def make_output_clip(id,comment_ides):

    
    print("making title clip ...")
    titleclip = create_clip(f"temp/{id}_title.png","temp/title.mp3")
    clips.append(titleclip)

    print("making body sclip ...")
    if ides.assert_png(id) == True:
        bodyclip = create_clip(f"temp/{id}_body.png","temp/body.mp3")    
        clips.append(bodyclip)
        
    print("making comments clip ...")
    for com_id in comment_ides:
        commentclip = create_clip(f"temp/{com_id}_comment.png",f'temp/{com_id}_comment.mp3')
        clips.append(commentclip)


    titlebodycommentsclip = concatenate_videoclips(clips)

    return titlebodycommentsclip




