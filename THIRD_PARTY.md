# Dependencies

The EXE is a PyInstaller bundle of the Python source in this repository. FFmpeg is a separate executable used to convert audio.

- **Python**: [source and license](https://github.com/python/cpython). Published kit: 3.14.6. PSF license.
- **Tcl/Tk**: [source and license](https://www.tcl.tk/software/tcltk/). Used by the GUI through Python's tkinter module.
- **PyInstaller**: [source and license](https://github.com/pyinstaller/pyinstaller). Build dependency: 6.22.3. GPL with the PyInstaller bootloader exception.
- **FFmpeg**: [upstream source](https://git.ffmpeg.org/ffmpeg.git), [6.1.1 source archive](https://ffmpeg.org/releases/ffmpeg-6.1.1.tar.xz), and [Gyan Windows build information](https://www.gyan.dev/ffmpeg/builds/). The bundled 6.1.1 essentials build enables GPL and version 3 components. Consult the build provider's source and license materials when redistributing that executable.

FFmpeg is not included in this source repository. Supply it with `--ffmpeg` when building a kit. For the exact configuration of your executable, run `ffmpeg.exe -version` and `ffmpeg.exe -buildconf`.

The archive-writing code follows the Bingus Shared Loader addon format and standard MurmurHash64A resource hashing. It does not contain game assets.
