# Building the Windows tools

## Requirements

- Windows 10 or 11, 64-bit.
- Python 3.14 with Tcl/Tk support. The published tools were built with Python 3.14.6.
- PyInstaller 6.22.3.
- A Windows `ffmpeg.exe`. The published kit uses FFmpeg 6.1.1, Gyan essentials build.

Install Python from [python.org](https://www.python.org/downloads/windows/). FFmpeg builds are available from [Gyan](https://www.gyan.dev/ffmpeg/builds/). Use the version above when matching the existing kit.

## Build

Open PowerShell in the repository folder:

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-build.txt
.\.venv\Scripts\python.exe build.py --ffmpeg "C:\ffmpeg\bin\ffmpeg.exe"
```

Replace the FFmpeg path with the location on your computer. The command builds both editions:

```text
dist/Vehicle Radio Music Pack Kit/Music Pack Builder.exe
dist/Vehicle Radio Music Pack Kit Chinese/Music Pack Maker.exe
```

To build just one edition, add `--language en` or `--language zh`.

Each output folder contains the EXE, its `Tools` runtime, FFmpeg, and empty `Music` and `Output` folders. Distribute the whole folder. The EXE cannot run on its own.

Python and PyInstaller versions affect the generated binary, so these commands reproduce the build process rather than guarantee a byte-for-byte identical EXE.

## Check a build

1. Open the EXE.
2. Select a folder containing a short audio file.
3. Build a pack and check that a ZIP appears in `Output`.
4. Import it into the mod manager alongside Vehicle Radio Framework and test playback in a vehicle.

A failed pack build writes details to `Tools/last_build.log`.

## Command-line pack generation

You can build a pack without compiling the GUI:

```powershell
.\.venv\Scripts\python.exe src/build_music_pack.py --id my_music_pack --name "My Music Pack" --input "C:\Music" --output "Output\My Music Pack.zip" --ffmpeg "C:\ffmpeg\bin\ffmpeg.exe"
```

Keep the same `--id` when updating a pack. No third-party Python packages are required for this command. If Lupa is installed, the builder also checks the generated Lua syntax.
