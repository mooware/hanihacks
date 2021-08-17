#!/usr/bin/env python
# -*- coding: utf-8 -*-

# expected sha1 hash of the original rom to translate
ORIG_ROM_SHA1 = '1ddde747140bd3887bc7f4a432a22f13bd52c3a3'

# credits text starts here, with other text following it.
# there is also a big block of 0xFF following it which can probably be used.
CREDITS_TEXT_START = 0x33300

# stage names at 0x53f9?
# big block of 0xFF at ~0x6430?
# character tiles around 0x11cc0?
# 72746 is note char, 72790 is "dollar", 73274 is "K"

# character table:
# (first char is whitespace, unused chars set to unicode replacement char)
#
#  !?。.ﾞﾟー⨯©「」+♪:$0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ╟╤╢╧╝╚╗╔����
# あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんぁぃぅぇぉゃゅょっ���������
# アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲンァィゥェォャュョッ♂♀�������

# note that the character table here corresponds to the tile map,
# where diacritics are separate entries. but in the encoded text,
# characters with diacritics are encoded as one byte.

# special characters at 0xC0-0xF1 in the given order:
#  hiragana two lines diacritic:
#   かきくけこさしすせそたちつてとはひふへほ
#  katakana two lines diacritic:
#   カキクケコサシスセソタチツテトハヒフヘホ
#  hiragana circle diacritic:
#   はひふへほ
#  katakana circle diacritic:
#   はひふへほ

# 0xFC = line break
# 0xFF = eol

CHARACTER_MAP = (
    ' !?。.ﾞﾟー⨯©「」+♪:$0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ╟╤╢╧╝╚╗╔����'
    'あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんぁぃぅぇぉゃゅょっ���������'
    'アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲンァィゥェォャュョッ♂♀�������'
    'がぎぐげござじずぜぞだぢづでどばびぶべぼ'
    'ガギグゲゴザジズゼゾダヂヅデドバビブベボ'
    'ぱぴぷぺぽ'
    'パピプペポ')

REVERSE_MAP = dict([(c, i) for (i, c) in enumerate(CHARACTER_MAP)])

# intro textbox: 12x6 chars
# stage name: 10 chars
STAGE_NAMES_RANGE = (0x53f9, 0x550d)
TEXTBOXES_RANGES = [(210761, 211463), (211520, 212981)] # there are a few non-text bytes in-between

def get_translation_table():
    full_map = CHARACTER_MAP.ljust(256, CHARACTER_MAP[190])
    table = list(full_map)
    table[0xFC] = '\n'
    return table

# extract and map stage names, each one is terminated by 0xFF
def extract_texts(data, start, end):
    result = []
    tbl = get_translation_table()
    pos = start
    while True:
        separator = data.find(b'\xFF', pos)
        if separator == -1 or separator > end:
            break
        text = data[pos:separator]
        mapped_text = "".join([tbl[c] for c in text])
        result.append({'start': pos, 'end': separator, 'text': mapped_text})
        pos = separator + 1
    return result

# decode an 8x8 PC Engine tile, description from here: https://www.chibiakumas.com/6502/pcengine.php
def decode_tile(data):
    tile = []
    pos = 0
    for x in range(8):
        row = []
        for y in range(8):
            mask = (128 >> y)
            color = 0
            if (data[pos] & mask):
                color |= 2
            if (data[pos + 1] & mask):
                color |= 1
            if (data[pos + 16] & mask):
                color |= 8
            if (data[pos + 17] & mask):
                color |= 4
            row.append(color)
        tile.append(row)
        pos += 2
    return tile

# generic color palette just to see some shapes
TILE_EXPORT_PALETTE = [
    0x000000, 0x9D9D9D, 0xFFFFFF, 0xBE2633,
    0xE06F8B, 0x493C2B, 0xA46422, 0xEB8931,
    0xF7E26B, 0x2F484E, 0x44891A, 0xA3CE27,
    0x1B2632, 0x005784, 0x31A2F2, 0xB2DCEF]

# write tile data from decode_tile() into a png file
def export_tile(tiledata, outpath):
    from PIL import Image
    img = Image.new('RGB', (8, 8))
    for x in range(8):
        for y in range(8):
            color = TILE_EXPORT_PALETTE[tiledata[y][x]]
            img.putpixel((x, y), color)
    img.save(outpath)

def dump_rom_tiles(data):
    sz = len(data)
    for i in range(0, sz, 32):
        tile = decode_tile(data[i:i+32])
        export_tile(tile, str(i) + ".png")

def dump_rom_tiles_sheet(data, outpath = None, colormask = 0xF):
    sz = len(data)
    from PIL import Image
    width = 16 * 8
    height = ((sz // 32) // 16) * 8 + 8
    img = Image.new('RGB', (width, height))
    for i in range(0, sz, 32):
        tile = decode_tile(data[i:i+32])
        index = i // 32
        sx = (index % 16) * 8
        sy = (index // 16) * 8
        for x in range(8):
            for y in range(8):
                color = tile[y][x]
                if color & colormask:
                    img.putpixel((sx + x, sy + y), TILE_EXPORT_PALETTE[color])
    img.save(outpath or 'tilesheet.png')
