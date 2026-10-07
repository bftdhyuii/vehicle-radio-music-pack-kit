from pathlib import Path
import argparse
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent


def build(language, ffmpeg):
    chinese = language == "zh"
    name = "Music Pack Maker" if chinese else "Music Pack Builder"
    entry = "music_pack_maker_zh.py" if chinese else "music_pack_maker.py"
    output = ROOT / "build" / language / "app"
    command = [
        sys.executable, "-m", "PyInstaller", "--noconfirm", "--clean",
        "--windowed", "--onedir", "--name", name,
        "--contents-directory", "Tools",
        "--paths", str(ROOT / "src"),
        "--add-data", str(ROOT / "src" / ("zh/build_music_pack.py" if chinese else "build_music_pack.py")) + ";.",
        "--distpath", str(output),
        "--workpath", str(ROOT / "build" / language / "work"),
        "--specpath", str(ROOT / "build" / language),
    ]
    for module in ("build_addon", "hd2_archive", "wave", "hashlib", "math", "tempfile"):
        command.extend(("--hidden-import", module))
    command.append(str(ROOT / "src" / entry))
    subprocess.run(command, cwd=ROOT, check=True)
    title = "Vehicle Radio Music Pack Kit Chinese" if chinese else "Vehicle Radio Music Pack Kit"
    destination = ROOT / "dist" / title
    shutil.copytree(output / name, destination, dirs_exist_ok=True)
    shutil.copy2(ffmpeg, destination / "Tools" / "ffmpeg.exe")
    for folder in ("Music", "Output"):
        (destination / folder).mkdir(exist_ok=True)
    for document in ("README.md", "BUILD.md", "THIRD_PARTY.md"):
        shutil.copy2(ROOT / document, destination / document)
    print("Kit ready: " + str(destination))


def main():
    parser = argparse.ArgumentParser(description="Build the Vehicle Radio music pack tools.")
    parser.add_argument("--ffmpeg", required=True, type=Path, help="Path to a Windows ffmpeg.exe")
    parser.add_argument("--language", choices=("en", "zh", "both"), default="both")
    args = parser.parse_args()
    if sys.platform != "win32":
        parser.error("Build the Windows EXE on Windows.")
    ffmpeg = args.ffmpeg.resolve()
    if not ffmpeg.is_file():
        parser.error("FFmpeg executable not found.")
    subprocess.run([str(ffmpeg), "-version"], check=True, stdout=subprocess.DEVNULL)
    for language in (("en", "zh") if args.language == "both" else (args.language,)):
        build(language, ffmpeg)


if __name__ == "__main__":
    main()
