import os
import subprocess
import re

CD_DEVICE = "/dev/sr0"

def find_tracks(stderr_output):
    tracks = []
    for line in stderr_output.splitlines():
        match = re.match(r"\s*(\d+)\.", line)
        if match:
            tracks.append(int(match.group(1)))
    return tracks

def play_track(track):
    filename = f"track_{track}.wav"
    subprocess.run(["cdparanoia", "-w", str(track), filename])
    subprocess.run(["aplay", filename])

def play_track(track):
    read_cd = subprocess.Popen(
        ["cdparanoia", "-p", str(track)],
        stdout=subprocess.PIPE
    )
    player = subprocess.Popen(
        ["aplay", "-f", "cd"],
        stdin=read_cd.stdout
    )
    read_cd.stdout.close()
    player.wait()

if os.path.exists(CD_DEVICE):
    print("Your CD drive detected.")

    result = subprocess.run(
        ["cdparanoia", "-Q"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if "track" in result.stderr.lower():
        print("CD Detected")

        tracks = find_tracks(result.stderr)
        print("Tracks Found\n", tracks)

        play_input = input("Choose a track number (or 'all'): ").strip()

        if play_input.lower() == "all":
            play_all(tracks)
        else:
            try:
                play_track(int(play_input))
            except ValueError:
                print("Invalid track number.")
    else:
        print("No CD Detected")
else:
    print("Your CD drive has not been detected. Make sure the device is connected.")
