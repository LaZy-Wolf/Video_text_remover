Video Text Remover
Video Text Remover is a Python application designed to remove text from videos by allowing users to draw rectangular masks over text regions and apply inpainting using OpenCV. The application features a user-friendly GUI built with Tkinter, supporting video frame navigation, mask management, and video processing with progress tracking.
Features

Load and Navigate Videos: Load video files (MP4, AVI, MOV, MKV) and navigate through frames using a slider or buttons.
Draw and Edit Masks: Draw rectangular masks over text regions, resize, move, or delete them with undo/redo functionality.
Inpainting: Remove text from masked regions using OpenCV's inpainting algorithm (TELEA method).
Progress Monitoring: Track processing progress with a progress bar and detailed logs.
Customizable Output: Save processed videos in MP4, AVI, or MOV formats.
Modern UI: Dark-themed interface with a tabbed layout for video controls, mask tools, and processing settings.

Prerequisites

Python: Version 3.6 or higher.
Operating System: Windows, macOS, or Linux.
Dependencies:
opencv-python: For video processing and inpainting.
numpy: For numerical operations.
Pillow: For image handling in Tkinter.
Tkinter: Included with standard Python installations.



Installation

Clone the Repository:
git clone https://github.com/LaZy-Wolf/Video_text_remover.git
cd Video_text_remover


Create a Virtual Environment (optional but recommended):
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install Dependencies:
pip install opencv-python numpy Pillow


Run the Application:
python video_text_remover.py



Usage

Launch the Application:

Run the script to open the GUI.


Load a Video:

Go to the Video tab and click Load Video.
Select a video file (supports MP4, AVI, MOV, MKV).


Navigate Frames:

Use the slider or navigation buttons (<<, <, >, >>) to browse video frames.


Draw Masks:

Switch to the Mask Tools tab.
Click and drag on the canvas to draw rectangular masks over text regions.
Resize or move masks using the handles (visible when selected).
Use Undo, Redo, Delete, or Clear All to manage masks.


Process the Video:

Go to the Processing tab.
Choose an output format (MP4, AVI, MOV).
Click Process Video and select a save location.
Monitor progress in the progress bar and log window.
Click Cancel Processing to stop if needed.


View Output:

Once processing is complete, the output video will be saved to the specified location.



Example

Load a video with subtitles.
Draw masks over the subtitle regions in the desired frames.
Process the video to remove the subtitles, saving the output as output.mp4.
Play the output video to verify the text has been removed.

Notes

Performance: Processing time depends on video length and resolution. Ensure sufficient disk space for output files.
Icon File: The application attempts to load an icon.ico file for the window icon. If you have a custom icon, place it in the project directory; otherwise, the default Tkinter icon will be used.
Canvas Scaling: Masks are drawn on a scaled canvas, but coordinates are automatically adjusted to match the original video resolution during processing.
Limitations: Inpainting quality depends on the surrounding pixels. Complex backgrounds may require manual mask adjustments for optimal results.

Troubleshooting

"Could not open video file": Ensure the video file is not corrupted and is in a supported format.
Dependencies not found: Verify that opencv-python, numpy, and Pillow are installed.
GUI issues: Ensure Tkinter is properly installed with your Python distribution.
Processing errors: Check the log window for detailed error messages.

Contributing
Contributions are welcome! To contribute:

Fork the repository.
Create a new branch (git checkout -b feature/your-feature).
Make your changes and commit (git commit -m "Add your feature").
Push to your branch (git push origin feature/your-feature).
Open a Pull Request.

License
This project is licensed under the MIT License. See the LICENSE file for details.
Contact
For issues or suggestions, open an issue on GitHub or contact the maintainer at your-email@example.com.

Happy coding with Video Text Remover!
