import gradio as gr
import os

a = os.path.join(os.path.dirname(__file__), "files/a.mp4")  # Video
b = os.path.join(os.path.dirname(__file__), "files/b.mp4")  # Video
s1 = os.path.join(os.path.dirname(__file__), "files/s1.srt")  # Subtitle
s2 = os.path.join(os.path.dirname(__file__), "files/s2.vtt")  # Subtitle


def get_file_size_mb(file_path):
    file_size_mb = os.stat(file_path).st_size / (1024 * 1024)
    return file_size_mb


def filesize_demo(video, audio, file):
    original_file_size_mb = None
    if file is not None:
        original_file_size_mb = get_file_size_mb(file.name)

    gradio_media_file_size_mb = None
    if video is not None:
        gradio_media_file_size_mb = get_file_size_mb(video)
    elif audio is not None:
        gradio_media_file_size_mb = get_file_size_mb(audio)

    return [original_file_size_mb, gradio_media_file_size_mb]


def video_demo(video, audio, file, subtitle=None):
    if video is not None:
        final_file = video
    elif audio is not None:
        final_file = audio
    else:
        final_file = file.name

    if subtitle is None:
        return final_file
    else:
        return [final_file, subtitle.name]


with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            video_input = gr.Video(type="file", label="Video", interactive=True)
            audio_input = gr.Audio(type="filepath", label="Audio", interactive=True)
            file_input = gr.File(label="File")
            subtitle_input = gr.File(label="Subtitle", file_types=[".srt", ".vtt"])
            submit_btn = gr.Button()
        with gr.Column():
            video_out = gr.Video(label="Out")
            original_size_out = gr.Textbox(label="File input filesize")
            upload_size_out = gr.Textbox(label="Media input filesize")
            audio_upload_out = gr.Textbox(label="Audio upload check")

    submit_btn.click(
        video_demo,
        inputs=[video_input, audio_input, file_input, subtitle_input],
        outputs=[video_out],
    )

    submit_btn.click(
        filesize_demo,
        inputs=[video_input, audio_input, file_input],
        outputs=[original_size_out, upload_size_out],
    )

    audio_input.upload(
        lambda: "Work fine",
        inputs=None,
        outputs=[audio_upload_out],
    )


if __name__ == "__main__":
    demo.launch()
