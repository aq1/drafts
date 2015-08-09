import os
import asyncio
import threading
import urllib.request
import functools
import aiohttp


urls = ['http://2ch.pm/b/src/99284101/14389720891310.webm',
         'http://2ch.pm/b/src/99284101/14389721638670.webm',
         'http://2ch.pm/b/src/99284101/14389721957510.webm',
         'http://2ch.pm/b/src/99284101/14389721959701.webm',
         'http://2ch.pm/b/src/99284101/14389722171650.webm',
         'http://2ch.pm/b/src/99284101/14389722174071.webm',
         'http://2ch.pm/b/src/99284101/14389722213260.webm',
         'http://2ch.pm/b/src/99284101/14389722416830.webm',
         'http://2ch.pm/b/src/99284101/14389722419241.webm',
         'http://2ch.pm/b/src/99284101/14389722852240.webm',
         'http://2ch.pm/b/src/99284101/14389723002181.webm',
         'http://2ch.pm/b/src/99284101/14389723002732.webm',
         'http://2ch.pm/b/src/99284101/14389723145160.webm',
         'http://2ch.pm/b/src/99284101/14389723147541.webm',
         'http://2ch.pm/b/src/99284101/14389723498290.webm',
         'http://2ch.pm/b/src/99284101/14389723500641.webm',
         'http://2ch.pm/b/src/99284101/14389723595740.webm',
         'http://2ch.pm/b/src/99284101/14389723751160.webm',
         'http://2ch.pm/b/src/99284101/14389723751391.webm',
         'http://2ch.pm/b/src/99284101/14389723751722.webm',
         'http://2ch.pm/b/src/99284101/14389723751893.webm',
         'http://2ch.pm/b/src/99284101/14389723786420.webm',
         'http://2ch.pm/b/src/99284101/14389723788861.webm',
         'http://2ch.pm/b/src/99284101/14389724048520.webm',
         'http://2ch.pm/b/src/99284101/14389724242550.webm',
         'http://2ch.pm/b/src/99284101/14389724475510.webm',
         'http://2ch.pm/b/src/99284101/14389724943380.webm',
         'http://2ch.pm/b/src/99284101/14389725281430.webm',
         'http://2ch.pm/b/src/99284101/14389725283841.webm',
         'http://2ch.pm/b/src/99284101/14389725597280.webm',
         'http://2ch.pm/b/src/99284101/14389725599651.webm',
         'http://2ch.pm/b/src/99284101/14389725745400.webm',
         'http://2ch.pm/b/src/99284101/14389725894550.webm',
         'http://2ch.pm/b/src/99284101/14389725896971.webm',
         'http://2ch.pm/b/src/99284101/14389726059920.webm',
         'http://2ch.pm/b/src/99284101/14389726120900.webm',
         'http://2ch.pm/b/src/99284101/14389726315830.webm',
         'http://2ch.pm/b/src/99284101/14389726318301.webm',
         'http://2ch.pm/b/src/99284101/14389726740530.webm',
         'http://2ch.pm/b/src/99284101/14389726742911.webm',
         'http://2ch.pm/b/src/99284101/14389726926000.webm',
         'http://2ch.pm/b/src/99284101/14389728367140.webm',
         'http://2ch.pm/b/src/99284101/14389728369561.webm',
         'http://2ch.pm/b/src/99284101/14389728591520.webm',
         'http://2ch.pm/b/src/99284101/14389728593961.webm',
         'http://2ch.pm/b/src/99284101/14389728940240.webm',
         'http://2ch.pm/b/src/99284101/14389728942681.webm',
         'http://2ch.pm/b/src/99284101/14389729010590.webm',
         'http://2ch.pm/b/src/99284101/14389729013051.webm',
         'http://2ch.pm/b/src/99284101/14389729491560.webm',
         'http://2ch.pm/b/src/99284101/14389729494121.webm',
         'http://2ch.pm/b/src/99284101/14389729614870.webm',
         'http://2ch.pm/b/src/99284101/14389729617101.webm',
         'http://2ch.pm/b/src/99284101/14389729978550.webm',
         'http://2ch.pm/b/src/99284101/14389729980971.webm',
         'http://2ch.pm/b/src/99284101/14389730096350.webm',
         'http://2ch.pm/b/src/99284101/14389730200230.webm',
         'http://2ch.pm/b/src/99284101/14389730202571.webm',
         'http://2ch.pm/b/src/99284101/14389730698110.webm',
         'http://2ch.pm/b/src/99284101/14389730700491.webm',
         'http://2ch.pm/b/src/99284101/14389730755180.webm',
         'http://2ch.pm/b/src/99284101/14389731051500.webm',
         'http://2ch.pm/b/src/99284101/14389731053901.webm',
         'http://2ch.pm/b/src/99284101/14389731458990.webm',
         'http://2ch.pm/b/src/99284101/14389731461421.webm',
         'http://2ch.pm/b/src/99284101/14389731893240.webm',
         'http://2ch.pm/b/src/99284101/14389731895611.webm',
         'http://2ch.pm/b/src/99284101/14389732051760.webm',
         'http://2ch.pm/b/src/99284101/14389732310630.webm',
         'http://2ch.pm/b/src/99284101/14389732417170.webm',
         'http://2ch.pm/b/src/99284101/14389734175460.webm',
         'http://2ch.pm/b/src/99284101/14389735621560.webm',
         'http://2ch.pm/b/src/99284101/14389736013630.webm',
         'http://2ch.pm/b/src/99284101/14389736015921.webm',
         'http://2ch.pm/b/src/99284101/14389737976190.webm',
         'http://2ch.pm/b/src/99284101/14389737978611.webm',
         'http://2ch.pm/b/src/99284101/14389738567370.webm',
         'http://2ch.pm/b/src/99284101/14389738569761.webm',
         'http://2ch.pm/b/src/99284101/14389738913160.webm',
         'http://2ch.pm/b/src/99284101/14389738915571.webm',
         'http://2ch.pm/b/src/99284101/14389739243440.webm',
         'http://2ch.pm/b/src/99284101/14389739246271.webm',
         'http://2ch.pm/b/src/99284101/14389739491810.webm',
         'http://2ch.pm/b/src/99284101/14389739494191.webm',
         'http://2ch.pm/b/src/99284101/14389739617520.webm',
         'http://2ch.pm/b/src/99284101/14389739619791.webm',
         'http://2ch.pm/b/src/99284101/14389739643500.webm',
         'http://2ch.pm/b/src/99284101/14389741088500.webm',
         'http://2ch.pm/b/src/99284101/14389741766230.webm',
         'http://2ch.pm/b/src/99284101/14389741920990.webm',
         'http://2ch.pm/b/src/99284101/14389741923141.webm',
         'http://2ch.pm/b/src/99284101/14389742423100.webm',
         'http://2ch.pm/b/src/99284101/14389742598040.webm',
         'http://2ch.pm/b/src/99284101/14389742600691.webm',
         'http://2ch.pm/b/src/99284101/14389743108930.webm',
         'http://2ch.pm/b/src/99284101/14389743110901.webm',
         'http://2ch.pm/b/src/99284101/14389743694030.webm',
         'http://2ch.pm/b/src/99284101/14389743695581.webm',
         'http://2ch.pm/b/src/99284101/14389743881960.webm',
         'http://2ch.pm/b/src/99284101/14389744171070.webm',
         'http://2ch.pm/b/src/99284101/14389744171171.webm',
         'http://2ch.pm/b/src/99284101/14389744745370.webm',
         'http://2ch.pm/b/src/99284101/14389745605990.webm',
         'http://2ch.pm/b/src/99284101/14389745607431.webm',
         'http://2ch.pm/b/src/99284101/14389745927560.webm',
         'http://2ch.pm/b/src/99284101/14389747002900.webm',
         'http://2ch.pm/b/src/99284101/14389747009970.webm',
         'http://2ch.pm/b/src/99284101/14389748470810.webm',
         'http://2ch.pm/b/src/99284101/14389749567620.webm',
         'http://2ch.pm/b/src/99284101/14389750067680.webm',
         'http://2ch.pm/b/src/99284101/14389750332580.webm',
         'http://2ch.pm/b/src/99284101/14389750436610.webm',
         'http://2ch.pm/b/src/99284101/14389750611120.webm',
         'http://2ch.pm/b/src/99284101/14389750706110.webm',
         'http://2ch.pm/b/src/99284101/14389751201140.webm',
         'http://2ch.pm/b/src/99284101/14389753346310.webm',
         'http://2ch.pm/b/src/99284101/14389753372640.webm',
         'http://2ch.pm/b/src/99284101/14389754958410.webm',
         'http://2ch.pm/b/src/99284101/14389755648030.webm',
         'http://2ch.pm/b/src/99284101/14389756179900.webm',
         'http://2ch.pm/b/src/99284101/14389756572840.webm',
         'http://2ch.pm/b/src/99284101/14389758514090.webm',
         'http://2ch.pm/b/src/99284101/14389761969500.webm',
         'http://2ch.pm/b/src/99284101/14389762266680.webm',
         'http://2ch.pm/b/src/99284101/14389762446410.webm',
         'http://2ch.pm/b/src/99284101/14389762447811.webm',
         'http://2ch.pm/b/src/99284101/14389764950200.webm',
         'http://2ch.pm/b/src/99284101/14389766882500.webm',
         'http://2ch.pm/b/src/99284101/14389766884931.webm',
         'http://2ch.pm/b/src/99284101/14389767671890.webm',
         'http://2ch.pm/b/src/99284101/14389768230310.webm',
         'http://2ch.pm/b/src/99284101/14389768232371.webm',
         'http://2ch.pm/b/src/99284101/14389768302850.webm',
         'http://2ch.pm/b/src/99284101/14389769050010.webm',
         'http://2ch.pm/b/src/99284101/14389769052421.webm',
         'http://2ch.pm/b/src/99284101/14389771850430.webm',
         'http://2ch.pm/b/src/99284101/14389773496930.webm',
         'http://2ch.pm/b/src/99284101/14389776224640.webm',
         'http://2ch.pm/b/src/99284101/14389776990070.webm',
         'http://2ch.pm/b/src/99284101/14389777475810.webm',
         'http://2ch.pm/b/src/99284101/14389778486420.webm',
         'http://2ch.pm/b/src/99284101/14389783244640.webm',
         'http://2ch.pm/b/src/99284101/14389783977680.webm',
         'http://2ch.pm/b/src/99284101/14389785399770.webm',
         'http://2ch.pm/b/src/99284101/14389786024250.webm',
         'http://2ch.pm/b/src/99284101/14389786740480.webm',
         'http://2ch.pm/b/src/99284101/14389788059090.webm',
         'http://2ch.pm/b/src/99284101/14389788962920.webm',
         'http://2ch.pm/b/src/99284101/14389789640780.webm',
         'http://2ch.pm/b/src/99284101/14389790303560.webm',
         'http://2ch.pm/b/src/99284101/14389792370460.webm',
         'http://2ch.pm/b/src/99284101/14389793561050.webm']
session = aiohttp.ClientSession()

FOLDER = 'webm'


@asyncio.coroutine
def save_file(data, name):
    with open(os.path.join(FOLDER, name), 'wb') as f:
        f.write(data)

    print('Finished %s' % name)


@asyncio.coroutine
def get_url(url):
    response = yield from session.get(url)
    yield from save_file(response.read(), url.split('/')[-1])


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    for url in urls[:2]:
        asyncio.async(functools.partial(get_url, url), loop=loop)
