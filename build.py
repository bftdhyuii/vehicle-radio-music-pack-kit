from pathlib import Path
import argparse
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent


def build(ffmpeg):
    name = "Music Pack Builder"
    entry = "music_pack_maker.py"
    output = ROOT / "build" / "en" / "app"
    command = [
        sys.executable, "-m", "PyInstaller", "--noconfirm", "--clean",
        "--windowed", "--onedir", "--name", name,
        "--contents-directory", "Tools",
        "--paths", str(ROOT / "src"),
        "--add-data", str(ROOT / "src" / "build_music_pack.py") + ";.",
        "--distpath", str(output),
        "--workpath", str(ROOT / "build" / "en" / "work"),
        "--specpath", str(ROOT / "build" / "en"),
    ]
    for module in ("build_addon", "hd2_archive", "cover_assets", "wave", "hashlib", "math", "tempfile"):
        command.extend(("--hidden-import", module))
    command.append(str(ROOT / "src" / entry))
    subprocess.run(command, cwd=ROOT, check=True)
    title = "Vehicle Radio Music Pack Kit"
    destination = ROOT / "dist" / title
    shutil.copytree(output / name, destination, dirs_exist_ok=True)
    shutil.copy2(ffmpeg, destination / "Tools" / "ffmpeg.exe")
    for folder in ("Input", "Output"):
        (destination / folder).mkdir(exist_ok=True)
    for document in ("README.txt", "先读这个.txt"):
        shutil.copy2(ROOT / document, destination / document)
    shutil.copy2(ROOT / "THIRD_PARTY.md", destination / "Tools" / "Dependencies.md")
    for license_file in (ROOT / "licenses").iterdir():
        shutil.copy2(license_file, destination / "Tools" / license_file.name)
    for name in ("README.md", "READ FIRST.txt", "BUILD.md", "THIRD_PARTY.md"):
        (destination / name).unlink(missing_ok=True)
    print("Kit ready: " + str(destination))


def main():
    parser = argparse.ArgumentParser(description="Build the Vehicle Radio music pack tools.")
    parser.add_argument("--ffmpeg", required=True, type=Path, help="Path to a Windows ffmpeg.exe")
    args = parser.parse_args()
    if sys.platform != "win32":
        parser.error("Build the Windows EXE on Windows.")
    ffmpeg = args.ffmpeg.resolve()
    if not ffmpeg.is_file():
        parser.error("FFmpeg executable not found.")
    subprocess.run([str(ffmpeg), "-version"], check=True, stdout=subprocess.DEVNULL)
    build(ffmpeg)


if __name__ == "__main__":
    main()
