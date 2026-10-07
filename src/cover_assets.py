"""Compile a square RGBA cover into Stingray GUI texture/material resources.

The GUI material layout and shader identifier match the game native
content/ui/shared/material/gui_diffuse_map resource.
"""
import struct
from hd2_archive import resource_hash

SIZE = 512

def compile_cover(resource, rgba):
    if len(rgba) != SIZE * SIZE * 4:
        raise ValueError('Expected a 512 x 512 RGBA image')
    texture_name = resource + '/cover'
    material_name = resource + '/cover_material'
    # Standard DDS DX10 header. The engine stores header and pixels separately.
    header = [124, 0x100F, SIZE, SIZE, SIZE * 4, 0, 1]
    header += [0] * 11
    header += [32, 4, int.from_bytes(b'DX10', 'little'), 0, 0, 0, 0, 0]
    header += [0x1000, 0, 0, 0, 0]
    dds = b'DDS ' + struct.pack('<31I', *header)
    dds += struct.pack('<5I', 28, 3, 0, 1, 0)  # RGBA8, Texture2D, one layer
    texture = b'\0' * 8 + b'\xff' * 4 + b'\0' * 180 + dds
    material = bytearray(160)
    struct.pack_into('<4I', material, 0, 0x120, 1, 24, 124)
    struct.pack_into('<I', material, 64, 1)  # texture count
    struct.pack_into('<QIQ', material, 128, 0xBA25DE35, 0x3AA8B87E,
                     resource_hash(texture_name))
    return material_name, [
        (texture_name, 'texture', texture, rgba),
        (material_name, 'material', bytes(material), b''),
    ]

def make_archive(resources):
    """Return main/GPU files for (name, type, main, GPU) resources."""
    types = sorted({kind for _, kind, _, _ in resources}, key=resource_hash)
    start = (72 + 32 * len(types) + 80 * len(resources) + 15) & ~15
    main, gpu, rows = bytearray(start), bytearray(), bytearray()
    for index, (name, kind, body, pixels) in enumerate(resources, 1):
        main += b'\0' * (-len(main) % 16)
        gpu += b'\0' * (-len(gpu) % 64)
        rows += struct.pack('<7Q6I', resource_hash(name), resource_hash(kind),
                            len(main), 0, len(gpu) if pixels else 0,
                            0xB000, 0x7C100, len(body), 0, len(pixels), 16, 64, index)
        main += body
        gpu += pixels
    table = struct.pack('<III20sQQ24s', 0xF0000011, len(types), len(resources),
                        b'', len(main), len(gpu), b'')
    for kind in types:
        table += struct.pack('<IIQIIII', 0, 0, resource_hash(kind),
                             sum(r[1] == kind for r in resources), 0, 16, 64)
    main[:len(table) + len(rows)] = table + rows
    return bytes(main), bytes(gpu)

