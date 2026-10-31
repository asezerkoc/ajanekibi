"""Aynı Gökyüzü, İki Gözlemevi: Takiyüddin'in İstanbul Rasathanesi (1577-1580). Piksel Tarih (@pikseltarihim),
sahneler 410-449. Grafikerin tarifi (teslimler/gece/ara/takiyuddin-rasathanesi/5-grafik.md); metin ve kartlar
4-kalite-metin.md'den. Yön dili: sağ = İstanbul / rasathane, sol = Hven / Avrupa.
Kullanım: python3 -I video/piksel/takiyuddin_rasathanesi.py [sahne numaraları]

Yeni figürler (bu dosyada; ciz.py'ye eklenmedi, yalnızca piksel()/hex2()/ImageDraw ve mevcut figürlerle):
  teras, rasathane, ceyrek_daire, armilla, top_, kuyruklu_yildiz, uraniborg, osmanli_camii, ulugbey_rasathanesi,
  dokumhane, masa_saati, minyatur_kitap, minder_sedir. Hepsi zemine oturur (duz_zemin / zemin_y); gökteki tek nesne
  kuyruklu yıldızdır (gökyüzü katmanına çizilir).
"""
import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from PIL import ImageDraw  # noqa: E402

from ciz import KOYU, _ac, _esik, agac, duman, duz_zemin, figur, gunes, hex2, piksel, taslar, temas_golgesi, yeni, zemin_y  # noqa: E402
from sahneler import kaydet, gokyuzu, uzak, orta, on, sprite, duz  # noqa: E402
from timur_figur import kisi, oturan, atli, gemi, sedir, gur_i_emir, orta_asya_sehri_ as _yok  # noqa: E402,F401
