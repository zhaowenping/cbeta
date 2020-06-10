def fromlatn(ctx, result='', mode=None):
    vowel = {
            'a': chr(0x11580), 'ā': chr(0x11581), 'i': chr(0x11582), 'ī': chr(0x11583),
            'u': chr(0x11584), 'ū': chr(0x11585), 'ṛ': chr(0x11586), 'ṝ': chr(0x11587),
            'ḷ': chr(0x11588), 'ḹ': chr(0x11589), 'e': chr(0x1158a), 'ai': chr(0x1158b),
            'o': chr(0x1158c), 'au': chr(0x1158d),
            }
    dconsonant = {
        'kh': chr(0x1158f), 'gh': chr(0x11591),
        'ch': chr(0x11594),
        'jh': chr(0x11596), 'ṭh': chr(0x11599),
        'ḍh': chr(0x1159b),
        'th': chr(0x1159e), 'dh': chr(0x115a0),
        'ph': chr(0x115a3), 'bh': chr(0x115a5),
        }
    consonant = {
        'k': chr(0x1158e), 'kh': chr(0x1158f), 'g': chr(0x11590), 'gh': chr(0x11591),
        'ṅ': chr(0x11592), 'c': chr(0x11593), 'ch': chr(0x11594), 'j': chr(0x11595),
        'jh': chr(0x11596), 'ñ': chr(0x11597), 'ṭ': chr(0x11598), 'ṭh': chr(0x11599),
        'ḍ': chr(0x1159a), 'ḍh': chr(0x1159b), 'ṇ': chr(0x1159c), 't': chr(0x1159d),
        'th': chr(0x1159e), 'd': chr(0x1159f), 'dh': chr(0x115a0), 'n': chr(0x115a1),
        'p': chr(0x115a2), 'ph': chr(0x115a3), 'b': chr(0x115a4), 'bh': chr(0x115a5),
        'm': chr(0x115a6), 'y': chr(0x115a7), 'r': chr(0x115a8), 'l': chr(0x115a9),
        'v': chr(0x115aa), 'ś': chr(0x115ab), 'ṣ': chr(0x115ac), 's': chr(0x115ad),
        'h': chr(0x115ae),
        }
    sigle_consonant = {
        'k', chr(0x1158f), 'g', chr(0x11591),
        'ṅ', 'c', chr(0x11594), 'j',
        chr(0x11596), 'ñ', 'ṭ', chr(0x11599),
        'ḍ', chr(0x1159b), 'ṇ', 't',
        chr(0x1159e), 'd', chr(0x115a0), 'n',
        'p', chr(0x115a3), 'b', chr(0x115a5),
        'm', 'y', 'r', 'l',
        'v', 'ś', 'ṣ', 's',
        'h'
        }
    consonant2 = {
        chr(0x1158f), chr(0x11591),
        chr(0x11594),
        chr(0x11596), chr(0x11599),
        chr(0x1159b),
        chr(0x1159e), chr(0x115a0),
        chr(0x115a3), chr(0x115a5),
        }
    mata = {
    'ā': chr(0x115af),
    'i': chr(0x115b0),
    'ī': chr(0x115b1),
    'u': chr(0x115b2),
    'ū': chr(0x115b3),
    'r': chr(0x115b4),
    'ṛ': chr(0x115b5),
    'e': chr(0x115b8),
    'ai': chr(0x115b9),
    'o': chr(0x115ba),
    'au': chr(0x115bb),
    }
    sign = {
    'ṃ': chr(0x115bd),
    'ḥ': chr(0x115be),
    }
    tt = {
            ord('a'): 0x11580, ord('ā'): 0x11581, ord('i'): 0x11582, ord('ī'): 0x11583,
            ord('u'): 0x11584, ord('ū'): 0x11585, ord('ṛ'): 0x11586, ord('ṝ'): 0x11587,
            ord('ḷ'): 0x11588, ord('ḹ'): 0x11589, ord('e'): 0x1158a, ord('o'): 0x1158c,
        ord('k'): 0x1158e, ord('g'): 0x11590,
        ord('ṅ'): 0x11592, ord('c'): 0x11593, ord('j'): 0x11595,
        ord('ñ'): 0x11597, ord('ṭ'): 0x11598,
        ord('ḍ'): 0x1159a, ord('ṇ'): 0x1159c, ord('t'): 0x1159d,
        ord('d'): 0x1159f, ord('n'): 0x115a1,
        ord('p'): 0x115a2, ord('b'): 0x115a4,
        ord('m'): 0x115a6, ord('y'): 0x115a7, ord('r'): 0x115a8, ord('l'): 0x115a9,
        ord('v'): 0x115aa, ord('ś'): 0x115ab, ord('ṣ'): 0x115ac, ord('s'): 0x115ad,
        ord('h'): 0x115ae,
    # ord('ā'): 0x115af,
    # ord('i'): 0x115b0,
    # ord('ī'): 0x115b1,
    # ord('u'): 0x115b2,
    # ord('ū'): 0x115b3,
    # ord('r'): 0x115b4,
    # ord('ṛ'): 0x115b5,
    # ord('e'): 0x115b8,
    # ord('o'): 0x115ba,
    ord('ṃ'): 0x115bd,
    ord('ḥ'): 0x115be,
    ord('|'): 0x115c2,
        }
    VIRAMA = chr(0x115bf)
    # '|': chr(0x115c2),
    # '||': chr(0x115c3),
    # 第一遍，替换掉所有的两位辅音
    for letter in dconsonant:
        ctx = ctx.replace(letter, dconsonant[letter])
        ctx = ctx.replace(letter, dconsonant[letter])

    # 第二遍，替换掉所有的两位摩多字母ai,au
    for letter in sigle_consonant:
        ctx = ctx.replace(f'{letter}ai', letter + chr(0x115b9))
        ctx = ctx.replace(f'{letter}au', letter + chr(0x115bb))

    # 第三遍，替换掉所有的两位元音
    ctx = ctx.replace('ai', chr(0x1158b))
    ctx = ctx.replace('au', chr(0x1158d))
    # 第四遍，在辅音中间加上VIRAMA
    result = ['',]
    for letter in ctx:
        if letter in sigle_consonant and result[-1] in sigle_consonant:
            result.append(VIRAMA)
        result.append(letter)
    ctx = ''.join(result[1:])
    # 第五遍，去掉摩多字母
    # TODO 需要考虑去辅音的字母情况
    result = ['',]
    for letter in ctx:
        if letter in 'āiīuūrṛeo' and result[-1] in sigle_consonant:
            result.append(mata[letter])
            continue
        result.append(letter)
    ctx = ''.join(result[1:])

    result = ['',]
    for letter in ctx:
        if letter == 'a' and result[-1] in sigle_consonant:
            continue
        result.append(letter)
    ctx = ''.join(result[1:])

    # ctx = ctx.replace('a', '')
    ctx = ctx.replace('||', chr(0x115c3))
    ctx = ctx.translate(tt)
    return ctx


ctx = 'munivṛndavandyacaraṇo dhvastākhiladoṣa uttamaśrikaḥ| sakalajagadarthadakṣo viśuddhabodhau jino jayati|'
ctx = '''
evaṃ mayā śrutam| ekasmin samaye bhagavān rājagṛhe viharati sma gṛdhrakūṭe parvate mahatā bhikṣusaṃghena sārdhaṃ dvādaśabhirbhikṣuśataiḥ sarvairarhadbhiḥ kṣīṇāsravairniḥkleśairvaśībhūtaiḥ suvimuktacittaiḥ suvimuktaprajñairājāneyairmahānāgaiḥ kṛtakṛtyaiḥ kṛtakaraṇīyairapahṛtabhārairanuprāptasvakārthaiḥ parikṣīṇabhavasaṃyojanaiḥ samyagājñāsuvimuktacittaiḥ sarvacetovaśitāparamapāramitāprāptairabhijñātābhijñātairmahāśrāvakaiḥ| tadyathā-āyuṣmatā ca ājñātakauṇḍinyena, āyuṣmatā ca aśvajitā, āyuṣmatā ca bāṣpeṇa, āyuṣmatā ca mahānāmnā, āyuṣmatā ca bhadrikeṇa, āyuṣmatā ca mahākāśyapena, āyuṣmatā ca urubilvakāśyapena, āyuṣmatā ca nadīkāśyapena, āyuṣmatā ca gayākāśyapena, āyuṣmatā ca śāriputreṇa, āyuṣmatā ca mahāmaudgalyāyanena, āyuṣmatā ca mahākātyāyanena, āyuṣmatā ca aniruddhena, āyuṣmatā ca revatena, āyuṣmatā ca kapphinena, āyuṣmatā ca gavāṃpatinā, āyuṣmatā ca pilindavatsena, āyuṣmatā ca bakkulena, āyuṣmatā ca mahākauṣṭhilena, āyuṣmatā ca bharadvājena, āyuṣmatā ca mahānandena, āyuṣmatā ca upanandena, āyuṣmatā ca sundaranandena, āyuṣmatā ca pūrṇamaitrāyaṇīputreṇa, āyuṣmatā ca subhūtinā āyuṣmatā ca rāhulena| ebhiścānyaiśca mahāśrāvakaiḥ-āyuṣmatā ca ānandena śaikṣeṇa| anyābhyāṃ ca dvābhyāṃ bhikṣusahasrābhyāṃ śaikṣāśaikṣābhyām| mahāprajāpatīpramukhaiśca ṣaḍbhirbhikṣuṇīsahasraiḥ|
'''
print(ctx)
from bottle import get, post
from bottle import route, run, static_file
from bottle import redirect, abort
from bottle import template
from bottle import jinja2_view as view
from bottle import request

html1 = '''<!DOCTYPE html>
<html lang="zh_CN">
<head>
  <meta charset="utf-8">
   <style>
   <!--
   /*
   @font-face {
     font-family: 'dzyz';
     font-style: normal;
     font-weight: normal;
     src:  url(/static/dzyz.woff) format('woff');
   }
   body{
     font-family: 'dzyz';
   }*/

   -->
   </style>
</head>
<body>
'''
html2 ='</body></html>'

@route('/')
def index():
    return html1 + fromlatn(ctx) + html2


#app = default_app()
# run(host='0.0.0.0', port=8081, server='gunicorn', workers=4)

def main():
    ''''''

def test():
    ''''''

if __name__ == "__main__":
    #main()
    test()
    run(host = '0.0.0.0', port = 8000)

