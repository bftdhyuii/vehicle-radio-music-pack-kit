HOW TO MAKE A MUSIC PACK

1. Add your songs.
   Put MP3, WAV, OGG, FLAC or M4A files directly in the Input folder.
   All songs in the selected folder become one music pack. Do not put them
   in subfolders. You can also select another folder with Browse...

2. Add a cover (optional).
   Put cover.png, cover.jpg or cover.jpeg beside the songs.
   Use one cover image per pack. A square 512 x 512 or 1024 x 1024 image
   is recommended. Other shapes are cropped from the center to a square.
   The builder creates a 512 x 512 game texture and uses the original
   image as the mod manager preview. Packs without a cover still work.

3. Open Music Pack Builder.exe.
   Check the Input folder path and enter a pack name. This name appears
   in the radio wheel. Use English letters, numbers, spaces or basic
   punctuation. Avoid Chinese characters and Windows filename symbols
   such as /, \, :, *, ?, a double quote, <, > or |.

4. Click Build Pack.
   Wait until the build finishes. The Output folder opens automatically.
   Your music pack is saved there as <pack name>.zip.
   Audio is converted to mono, 22,050 Hz, 16-bit PCM, so the finished ZIP
   may be larger than the original compressed songs.

5. Install or share the finished ZIP.
   Import it into your mod manager and enable it alongside Bingus Shared
   Loader and Vehicle Radio Framework. Fully restart the game after
   installing or replacing a pack.
   Each pack takes one music slot, assigned in addon loading order.
   Selecting a pack plays a random song from it. Up to 12 packs are supported.

UPDATING OR MAKING ANOTHER PACK

To update a pack, change its songs or cover, keep the same pack name,
and click Build Pack again. The matching ZIP in Output is overwritten.
Replace the previous version in the mod manager.

Keep Tools/pack_ids.json when moving or updating the kit. It stores the
identity of each pack. A different name creates a separate pack.
For another pack, use a different music folder or replace the songs in
Input, then enter a new pack name and build.

FOLDERS

Input   - Songs and an optional cover.
Output  - Finished music pack ZIPs.
Tools   - Files needed by the builder. Keep this folder intact.

If a build fails, check Tools/last_build.log.
Do not run the EXE inside a ZIP or move it away from Tools!!!
