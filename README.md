# Vehicle Radio Music Pack Kit

A Windows tool for making music packs for Vehicle Radio Framework in Helldivers 2.

Choose a folder, enter a pack name, and click **Build Pack**. The tool converts the songs and creates a ZIP that players can import into their mod manager.

## Using the kit

1. Extract the entire kit. Keep the `Tools` folder beside the EXE.
2. Put songs in `Music`, or use **Browse** to choose another folder.
3. Open `Music Pack Builder.exe` (English) or `Music Pack Maker.exe` (Chinese).
4. Enter a pack name and click **Build Pack**.
5. Share the ZIP from `Output`.

Supported formats: MP3, WAV, OGG, FLAC, and M4A. Pack names use ASCII characters. Generated mods have an empty description.

To update an existing pack, rebuild it under the same name and keep `Tools/pack_ids.json`. A different name creates a separate pack.

Players need **Bingus Shared Loader** and **Vehicle Radio Framework**. They do not need the kit, Python, or FFmpeg installed separately.

## Source and builds

Both GUI editions and the pack builder are included in `src`. See [BUILD.md](BUILD.md) for the Windows build commands and [THIRD_PARTY.md](THIRD_PARTY.md) for dependencies.

The repository contains no music or game assets.

## Files

- `src/music_pack_maker.py`: English GUI and build worker.
- `src/music_pack_maker_zh.py`: Chinese GUI and build worker.
- `src/build_music_pack.py`: audio conversion and music-pack generation.
- `src/build_addon.py`: mod manifest and ZIP packaging.
- `src/hd2_archive.py`: Lua resource archive writer.
- `build.py`: builds either or both Windows kits.

Audio is converted to mono, 22,050 Hz, 16-bit PCM and embedded in the Lua addon. Finished packs can be larger than the original compressed songs.

## Cover images

Put `cover.png`, `cover.jpg`, or `cover.jpeg` in the music folder and rebuild the pack. The image is cropped to a square and embedded automatically. Vehicle Radio Framework v0.4.2 displays it above the pack name in the wheel center. The English kit builds a 512 x 512 game texture, displayed as one image. Use a square 512 x 512 or 1024 x 1024 source for best results. Packs without a cover still work.

The English kit also includes the original cover image in the generated mod ZIP and sets it as the mod manager preview. The mod description stays empty.
