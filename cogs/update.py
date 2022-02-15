import sys
import subprocess

# implement pip as a subprocess:
if __name__ == '__main__':
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'ffmpeg'])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'ffmpeg-python'])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'yt-dlp'])