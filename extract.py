import subprocess
import os
import sys
import argparse

def print_help():
    print("Extract frames and audio from video files using ffmpeg.\n Usage: python extract.py <input_file>")
    sys.exit(0)

def check_ffmpeg():
    return subprocess.call(['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0

def extract_frames_and_audio(input_file):
    if not os.path.exists(input_file):
        print(f"Input file not found: {input_file}")
        return

    filename = os.path.basename(input_file)
    filename_noext = os.path.splitext(filename)[0]
    output_folder = f"./{filename_noext}"

    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
        print(f"Created folder: {output_folder}")

    # Use ffmpeg to extract video frames into PNG images
    subprocess.run(['ffmpeg', '-i', input_file, f'{output_folder}/%10d.png'])

    # Use ffmpeg to extract audio as WAV
    subprocess.run(['ffmpeg', '-i', input_file, '-map', '0:a:0', f'{output_folder}/ambiance.wav'])

        # Use ffmpeg to extract audio as WAV
    subprocess.run(['ffmpeg', '-i', input_file, '-map', '0:a:1', f'{output_folder}/voices.wav'])

    print(f"Extraction complete for {input_file}. PNG images and WAV file saved in: {output_folder}")

def main():
    parser = argparse.ArgumentParser(prog='extract.py', description='Extract frames and audio from video files using ffmpeg.')
    parser.add_argument('input_files', nargs='*', help=argparse.SUPPRESS)

    # Check for the help flag
    if "-h" in sys.argv or "--help" in sys.argv:
        print_help()

    args = parser.parse_args()

    if not check_ffmpeg():
        print("ffmpeg not found. Please install ffmpeg.")
        exit(1)

    if not args.input_files:
        print_help()

    for input_file in args.input_files:
        extract_frames_and_audio(input_file)

if __name__ == "__main__":
    main()
