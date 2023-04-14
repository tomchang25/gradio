import gradio as gr
import os

a = os.path.join(os.path.dirname(__file__), "files/a.mp4")  # Video
b = os.path.join(os.path.dirname(__file__), "files/b.mp4")  # Video
s1 = os.path.join(os.path.dirname(__file__), "files/s1.srt")  # Subtitle
s2 = os.path.join(os.path.dirname(__file__), "files/s2.vtt")  # Subtitle


def get_file_size_mb(file_path):
    file_size_mb = os.stat(file_path).st_size / (1024 * 1024)
    return file_size_mb


def video_demo(video, audio, file, subtitle=None):
    original_file_size_mb = None
    if file is not None:
        original_file_size_mb = get_file_size_mb(file.name)

    gradio_media_file_size_mb = None
    if video is not None:
        final_file = video
        gradio_media_file_size_mb = get_file_size_mb(video)
    elif audio is not None:
        final_file = audio
        print(audio)
        gradio_media_file_size_mb = get_file_size_mb(audio)
    else:
        final_file = file.name

    if subtitle is None:
        return [final_file, original_file_size_mb, gradio_media_file_size_mb]
    else:
        return [
            (final_file, subtitle.name),
            original_file_size_mb,
            gradio_media_file_size_mb,
        ]


demo = gr.Interface(
    fn=video_demo,
    inputs=[
        gr.Video(type="file", label="Video", interactive=True),
        gr.Audio(type="filepath", label="Audio", interactive=True),
        gr.File(label="File"),
        gr.File(label="Subtitle", file_types=[".srt", ".vtt"]),
    ],
    outputs=[
        gr.Video(label="Out"),
        gr.outputs.Textbox(label="File input filesize"),
        gr.outputs.Textbox(label="Media input filesize"),
    ],
    examples=[
        [a, s1],
        [b, s2],
        [a, None],
    ],
)

if __name__ == "__main__":
    demo.launch()
