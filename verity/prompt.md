Using your workspace, I need you to programmatically generate a fully working Scratch .sb3 project file from this YouTube video: https://m.youtube.com/watch?v=SQ5kgn8JLtg. 

Here is your step-by-step execution plan:

1. Download & Extract: Use yt-dlp and ffmpeg in your workspace to download the video and extract its audio track and image frames. 

2. Specs & Cropping: Target the absolute highest resolution and framerate (up to 1080p 240fps) that you can successfully compile in your workspace without hitting memory limits. Do not stretch or add padding/fillers to the video; crop it to fit a standard 16:9 aspect ratio. Apply minimal compression.

3. Construct the Scratch Logic (project.json): 
   * Intro Sprite: Create a splash screen that says textually: "This project is way better on TurboWarp".
   * Video Sprite: Load all extracted frames as costumes.
   * Scripting: When the green flag is clicked, show the intro sprite for 2 seconds, fade it out or hide it, and then broadcast a message (e.g., 'start_video'). When 'start_video' is received, play the extracted audio and rapidly cycle through the video sprite's costumes at the exact framerate to maintain the original video speed.

4. Package: Compile the JSON, audio, and frames into a ZIP archive, rename the extension to .sb3.

5. Deliverable: Execute this entirely in your workspace and provide me with the final .sb3 file download link.
