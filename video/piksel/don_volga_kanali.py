"""Su Akmıyor: Sokollu Mehmed Paşa'nın Don-Volga kanalı ve Astrahan seferi (1569 → 1952). Piksel Tarih (@pikseltarihim),
sahneler 250-289. Grafikerin tarifi: teslimler/gece/ara/don-volga-kanali/5-grafik.md; kartlar 4-kalite-metin.md
"Nihai ekran kartları" (52 kart, harfi harfine; TSX: video/src/sahneler/DonVolga.tsx).
Kalıp: cem_sultan.py (ölçek ve kadraj), celebi_mehmed_paris.py (TSX'ten okunan yazı bandı denetimi),
orhun_yazitlari.py (kenar denetimi), takiyuddin_rasathanesi.py (suda gemi: gemi sprite'ta, su sprite'ın alt satırlarında).
Yön dili: batı (Don, Azak, İstanbul, dönüş) solda; doğu (Volga, Astrahan) sağda. Hendek her sahnede zemine kazılmış sığ
bir yarık (orta planda), kazıcılar onun tabanına basar.

Yeni figürler (bu dosyada; ciz.py'ye eklenmedi, yalnızca piksel()/hex2()/ImageDraw ve mevcut figürlerle):
  kazici (iki elle kazma vuran asker), kurekci (kürekle toprak atan), toprak_yigini, hendek_yarigi (orta planda sığ yarık),
  harita_sehpasi (iki nehirli harita, ayaklı sehpada), kayik_kutuk (kütükler üstünde karadan çekilen nehir teknesi),
  ahsap_kale (Astrahan: kazık sur, ahşap kuleler, soğan kubbeli kilise), kadirga (latin yelkenli Osmanlı kadırgası, hasar=1
  kırık direk), kon_cadir (Osmanlı ordu çadırı; yikik=1 sökülmüş), harabe (eski Hacı Tarhan'ın kerpiç duvar kalıntıları),
  yatan_asker (yerde ölü asker, kan), dikenli_tel, gozcu_kulesi (alçak), el_arabasi, heykel_kaide (yüzsüz bronz heykel
  silueti ve granit kaide; kim=None boş kaide), kilit (1952 kanal kapağı, önden: iki beton kule ve çelik kapak, akan su).
Hepsi zemine oturur (zemin_y / duz_zemin); gemiler su çizgisine oturur, altları suyun içindedir.
Kullanım: python3 -I video/piksel/don_volga_kanali.py [sahne numaraları]"""
import math
import random
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from PIL import Image, ImageDraw  # noqa: E402

from ciz import (_ac, at, ates_ as _yok, cicek, duman, duz_zemin, figur, gradyan, gunes, hex2, okuz, piksel,  # noqa: E402,F401
                 temas_golgesi, yeni, yildizlar, zemin_y) if False else (None,) * 15
