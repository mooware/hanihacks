#!/usr/bin/env python
# -*- coding: utf-8 -*-

ORIG_ROM_SHA1 = '1ddde747140bd3887bc7f4a432a22f13bd52c3a3'

# credits text starts here, with other text following it.
# there is also a big block of 0xFF following it which can probably be used.
CREDITS_TEXT_START = 0x33300

# character table, with unused fields mapped to the unicode replacement char:
# (first char is whitespace)
#
#  !?。.ﾞﾟー⨯©「」+♪:$0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ╟╤╢╧╝╚╗╔����
# あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんぁぃぅぇぉゃゅょっ���������
# アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲンァィゥェォャュョッ♂♀�������

# note that the character table here corresponds to the sprite map,
# where diacritics are separate entries. but in the encoded text,
# characters with diacritics are encoded as one byte

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

CHARACTER_MAP = (' !?。.ﾞﾟー⨯©「」+♪:$0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ╟╤╢╧╝╚╗╔����あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんぁぃぅぇぉゃゅょっ���������アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲンァィゥェォャュョッ♂♀�������'
    'がぎぐげござじずぜぞだぢづでどばびぶべぼ'
    'ガギグゲゴザジズゼゾダヂヅデドバビブベボ'
    'ぱぴぷぺぽ'
    'パピプペポ')

REVERSE_MAP = dict([(c, i) for (i, c) in enumerate(CHARACTER_MAP)])

# intro textbox: 12x6 chars