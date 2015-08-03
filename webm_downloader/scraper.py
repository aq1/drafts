import asyncio
import threading

import aiohttp

links = ['http://2ch.pm/b/src/98987889/14386055038900.webm',
         'http://2ch.pm/b/src/98987889/14386055848260.webm',
         'http://2ch.pm/b/src/98987889/14386056289180.webm',
         'http://2ch.pm/b/src/98987889/14386057016060.webm',
         'http://2ch.pm/b/src/98987889/14386057018441.webm',
         'http://2ch.pm/b/src/98987889/14386058349550.webm',
         'http://2ch.pm/b/src/98987889/14386059229340.webm',
         'http://2ch.pm/b/src/98987889/14386059659950.webm',
         'http://2ch.pm/b/src/98987889/14386060859290.webm',
         'http://2ch.pm/b/src/98987889/14386060860311.webm',
         'http://2ch.pm/b/src/98987889/14386065241840.webm',
         'http://2ch.pm/b/src/98987889/14386065939650.webm',
         'http://2ch.pm/b/src/98987889/14386065941561.webm',
         'http://2ch.pm/b/src/98987889/14386066217110.webm',
         'http://2ch.pm/b/src/98987889/14386068177330.webm',
         'http://2ch.pm/b/src/98987889/14386071253680.webm',
         'http://2ch.pm/b/src/98987889/14386071256081.webm',
         'http://2ch.pm/b/src/98987889/14386072221650.webm',
         'http://2ch.pm/b/src/98987889/14386072797100.webm',
         'http://2ch.pm/b/src/98987889/14386074075830.webm',
         'http://2ch.pm/b/src/98987889/14386075254310.webm',
         'http://2ch.pm/b/src/98987889/14386079967570.webm',
         'http://2ch.pm/b/src/98987889/14386080027110.webm',
         'http://2ch.pm/b/src/98987889/14386082105690.webm',
         'http://2ch.pm/b/src/98987889/14386083818740.webm',
         'http://2ch.pm/b/src/98987889/14386084170970.webm',
         'http://2ch.pm/b/src/98987889/14386088180820.webm',
         'http://2ch.pm/b/src/98987889/14386089108090.webm',
         'http://2ch.pm/b/src/98987889/14386089109771.webm',
         'http://2ch.pm/b/src/98987889/14386089111282.webm',
         'http://2ch.pm/b/src/98987889/14386090071090.webm',
         'http://2ch.pm/b/src/98987889/14386090073421.webm',
         'http://2ch.pm/b/src/98987889/14386091176790.webm',
         'http://2ch.pm/b/src/98987889/14386094278910.webm',
         'http://2ch.pm/b/src/98987889/14386095512550.webm',
         'http://2ch.pm/b/src/98987889/14386095538830.webm',
         'http://2ch.pm/b/src/98987889/14386096215940.webm',
         'http://2ch.pm/b/src/98987889/14386097179700.webm',
         'http://2ch.pm/b/src/98987889/14386099222150.webm',
         'http://2ch.pm/b/src/98987889/14386101195890.webm',
         'http://2ch.pm/b/src/98987889/14386103142810.webm',
         'http://2ch.pm/b/src/98987889/14386106165700.webm',
         'http://2ch.pm/b/src/98987889/14386107923040.webm',
         'http://2ch.pm/b/src/98987889/14386109569360.webm',
         'http://2ch.pm/b/src/98987889/14386110439130.webm',
         'http://2ch.pm/b/src/98987889/14386111477550.webm',
         'http://2ch.pm/b/src/98987889/14386111587790.webm',
         'http://2ch.pm/b/src/98987889/14386112946000.webm',
         'http://2ch.pm/b/src/98987889/14386113137240.webm',
         'http://2ch.pm/b/src/98987889/14386114343650.webm',
         'http://2ch.pm/b/src/98987889/14386115306230.webm',
         'http://2ch.pm/b/src/98987889/14386117909460.webm',
         'http://2ch.pm/b/src/98987889/14386119920580.webm',
         'http://2ch.pm/b/src/98987889/14386120306340.webm',
         'http://2ch.pm/b/src/98987889/14386120308581.webm',
         'http://2ch.pm/b/src/98987889/14386120548860.webm',
         'http://2ch.pm/b/src/98987889/14386121626810.webm',
         'http://2ch.pm/b/src/98987889/14386121987870.webm',
         'http://2ch.pm/b/src/98987889/14386122729510.webm',
         'http://2ch.pm/b/src/98987889/14386123029920.webm',
         'http://2ch.pm/b/src/98987889/14386124008380.webm',
         'http://2ch.pm/b/src/98987889/14386125395120.webm',
         'http://2ch.pm/b/src/98987889/14386125427180.webm',
         'http://2ch.pm/b/src/98987889/14386125429751.webm',
         'http://2ch.pm/b/src/98987889/14386126707730.webm',
         'http://2ch.pm/b/src/98987889/14386127135250.webm',
         'http://2ch.pm/b/src/98987889/14386127137431.webm',
         'http://2ch.pm/b/src/98987889/14386127441980.webm',
         'http://2ch.pm/b/src/98987889/14386129558710.webm',
         'http://2ch.pm/b/src/98987889/14386129558831.webm',
         'http://2ch.pm/b/src/98987889/14386129558962.webm',
         'http://2ch.pm/b/src/98987889/14386129646260.webm',
         'http://2ch.pm/b/src/98987889/14386130455140.webm',
         'http://2ch.pm/b/src/98987889/14386130649740.webm',
         'http://2ch.pm/b/src/98987889/14386131054470.webm',
         'http://2ch.pm/b/src/98987889/14386131195690.webm',
         'http://2ch.pm/b/src/98987889/14386131197821.webm',
         'http://2ch.pm/b/src/98987889/14386131465220.webm',
         'http://2ch.pm/b/src/98987889/14386131722490.webm',
         'http://2ch.pm/b/src/98987889/14386131999570.webm',
         'http://2ch.pm/b/src/98987889/14386132311540.webm',
         'http://2ch.pm/b/src/98987889/14386132374660.webm',
         'http://2ch.pm/b/src/98987889/14386132427790.webm',
         'http://2ch.pm/b/src/98987889/14386132475580.webm',
         'http://2ch.pm/b/src/98987889/14386132663030.webm',
         'http://2ch.pm/b/src/98987889/14386132749150.webm',
         'http://2ch.pm/b/src/98987889/14386133929070.webm',
         'http://2ch.pm/b/src/98987889/14386133954700.webm',
         'http://2ch.pm/b/src/98987889/14386134826980.webm',
         'http://2ch.pm/b/src/98987889/14386134829231.webm',
         'http://2ch.pm/b/src/98987889/14386134913830.webm',
         'http://2ch.pm/b/src/98987889/14386135009620.webm',
         'http://2ch.pm/b/src/98987889/14386135085620.webm',
         'http://2ch.pm/b/src/98987889/14386135218700.webm',
         'http://2ch.pm/b/src/98987889/14386135220611.webm',
         'http://2ch.pm/b/src/98987889/14386135642600.webm',
         'http://2ch.pm/b/src/98987889/14386135661580.webm',
         'http://2ch.pm/b/src/98987889/14386135715650.webm',
         'http://2ch.pm/b/src/98987889/14386135717211.webm',
         'http://2ch.pm/b/src/98987889/14386135887820.webm',
         'http://2ch.pm/b/src/98987889/14386136343300.webm',
         'http://2ch.pm/b/src/98987889/14386136345361.webm',
         'http://2ch.pm/b/src/98987889/14386136786110.webm',
         'http://2ch.pm/b/src/98987889/14386136903510.webm',
         'http://2ch.pm/b/src/98987889/14386136925090.webm',
         'http://2ch.pm/b/src/98987889/14386136927011.webm',
         'http://2ch.pm/b/src/98987889/14386137266130.webm',
         'http://2ch.pm/b/src/98987889/14386137412080.webm',
         'http://2ch.pm/b/src/98987889/14386137413961.webm',
         'http://2ch.pm/b/src/98987889/14386138005190.webm',
         'http://2ch.pm/b/src/98987889/14386139624210.webm',
         'http://2ch.pm/b/src/98987889/14386139640410.webm',
         'http://2ch.pm/b/src/98987889/14386139640731.webm',
         'http://2ch.pm/b/src/98987889/14386142450660.webm',
         'http://2ch.pm/b/src/98987889/14386142760920.webm',
         'http://2ch.pm/b/src/98987889/14386142761021.webm',
         'http://2ch.pm/b/src/98987889/14386144441020.webm',
         'http://2ch.pm/b/src/98987889/14386145159040.webm',
         'http://2ch.pm/b/src/98987889/14386145982680.webm',
         'http://2ch.pm/b/src/98987889/14386145984111.webm',
         'http://2ch.pm/b/src/98987889/14386147067010.webm',
         'http://2ch.pm/b/src/98987889/14386148339160.webm',
         'http://2ch.pm/b/src/98987889/14386148401570.webm',
         'http://2ch.pm/b/src/98987889/14386149985410.webm',
         'http://2ch.pm/b/src/98987889/14386150874270.webm',
         'http://2ch.pm/b/src/98987889/14386150876621.webm',
         'http://2ch.pm/b/src/98987889/14386151313600.webm']


session = aiohttp.ClientSession()


@asyncio.coroutine
def fetch_page(url):
    response = yield from session.request('GET', url)
    assert response.status == 200
    print(response.status, response.url)
    return (yield from response.read())

loop = asyncio.get_event_loop()


a = loop.run_until_complete(asyncio.wait([fetch_page(x) for x in links[:3]]))


def write(f, name):
    with open("%s.webm" % name, 'wb') as ff:
        ff.write(f)
        print(name, 'done')

for i, x in enumerate(a[0]):
    threading.Thread(target=write, args=(x.result(), i)).run()
