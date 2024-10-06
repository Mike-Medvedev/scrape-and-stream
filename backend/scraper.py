import asyncio
import subprocess
from pyppeteer import launch


async def main():
    browser = await launch(headless=False, args=[
        '--start-fullscreen'  # This will launch Chromium in full-screen mode
    ])
    page = await browser.newPage()
    await page.setViewport({'width': 1280, 'height': 720})
    # Navigate to the URL and wait for the page to fully load
    await page.goto('https://mantine.dev', {'waitUntil': 'networkidle2'})

    # Wait for a specific element to ensure page has fully loaded
    # Adjust this based on an important page element
    await page.waitForSelector('body')

    # Get the page content (HTML)
    content = await page.content()

    # Print the HTML content of the page
    print(content)
    # Start FFmpeg for screen recording (customize the input and output as needed)
    ffmpeg_command = [
        'ffmpeg',
        '-y',  # overwrite output file if exists
        '-f', 'avfoundation',  # macOS input format
        '-probesize', '50M',  # increase probesize to analyze more frames
        '-framerate', '30',  # frame rate for input capture
        '-r', '30',  # limit output frame rate to 30 fps
        '-i', '1',  # capture screen (1 for main display)
        '-vf', 'scale=1280:720',  # Force the output video size to 1280x720
        '-c:v', 'libx264',  # use the H.264 codec for video
        '-preset', 'fast',  # encoding speed
        '-crf', '23',  # quality level
        '-pix_fmt', 'yuv420p',  # ensure compatibility with QuickTime
        '-level', '4.2',  # set H.264 level to handle the resolution
        'output.mp4'  # output file
    ]

    # Start recording
    process = subprocess.Popen(ffmpeg_command)

    await asyncio.sleep(5)  # Do your browser tasks here for 10 seconds

    # Stop FFmpeg process
    process.terminate()
    process.wait()  # Ensure FFmpeg finishes properly

    await browser.close()

# Run the Pyppeteer script
asyncio.run(main())
