import gradio as gr
import subprocess
import shutil
import os
from datetime import datetime

def run_scripts(target, source):
    outputfile=[]
    for target_file in target :
        target_extension = os.path.splitext(target_file.name)[-1]
        target_name = os.path.splitext(target_file.name)[1]
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        output_path1 = "output" + timestamp + target_extension

        cmd1 = ["python3", "run.py", "-s", source.name, "-t", target_file.name, "-o", output_path1, "--frame-processor", "face_swapper","face_enhancer",'--many-faces']
        subprocess.run(cmd1)
        outputfile.append(output_path1)

    return outputfile

iface = gr.Interface(
    fn=run_scripts,
    inputs=["files","file"],
    outputs="files",
    title="Face swapper",
    description="Upload a target image/video and a source image to swap faces.",
    live=False
)

iface.launch(debug=True)