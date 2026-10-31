# Sahne tarifi şablonu

Grafiker her sahneyi bu üç parçayla teslim eder. Kod tarafı Python tarifini `video/piksel/<seri>.py` dosyasına,
`Bolum` satırını `video/src/sahneler/<Seri>.tsx` dosyasına olduğu gibi koyar; bu yüzden parametre adları
`fonksiyonlar.md` ile bire bir aynı olmalıdır.

## 1) Sahne planı (Türkçe, 3-6 satır)

```
Sahne 71 — Sistan çölü, 1363, öğle: kayalık setin üstünde üç okçu (sola bakar), aşağıda Timur kılıçla
yürür; f ≥ 0.5'te iki ok saplanır, Timur diz çöker. At solda eyerli bekler.
Zemin: sprite tabanı 630; set üstü taban−34 (düz). Işık: sağ üstten, sarı-bej çöl paleti.
Hareket: okçular kol 0.4 → 0 (yay iner), oklar f 0-0.5 arasında uçar. Kamera: yakin 1.9 (geniş), sakin.
Ses: rüzgâr, ok vınlaması, düşüş.
```

## 2) Python tarifi (`sahneNN()`)

Kalıp: önce dört katman (`gokyuzu`, `uzak`, `orta`, `on`) ya da iç mekân (`ic_mekan`), sonra `kare(t, z, i)` ve `sprite(...)`.

```python
def sahne71():
    """Sistan, 1363: çölde pusu; setin üstündeki okçular atar, Timur diz çöker."""
    # Gökyüzü: 5-6 renkli gradyan (üstten alta), güneş (x, y, yarıçap, [çekirdek, hale]), bulutlar [(x, y, boy)],
    # bulut renkleri (ışık, orta, gölge). Bulutlar y 245'in altında (yazı bandı dışında).
    gokyuzu(71, ["#c8a070", "#d8b080", "#e8c890", "#f0d8a0", "#f4e0b0"], (90, 300, 26, ["#fff8e0", "#ffe8b0"]),
            [(420, 360, 26)], ("#fff4e0", "#f0dcc0", "#d8b898"))
    # Uzak plan: dağ (koyu, açık), tepe (koyu, açık), ova (3 ton). dag_y=(tepe, etek) yüksekliği belirler.
    uzak(71, ["#b8906a", "#a8805e"], ["#c8a070", "#b89062"], ["#d8b480", "#c8a472", "#b89464"], dag_y=(340, 420))
    # Orta plan: üst kenar aralığı, 5 ton (yakına doğru koyulaşır), ışıklı kenar rengi; ekle= ile arka plan figürleri
    # (orta plan 810 geniş: ızgara x'e 135 ekle; düz zemin duz(588)).
    orta(71, (528, 562), ["#d8b07a", "#c8a06e", "#b89062", "#a88056", "#98704c"], "#f0d098",
         ekle=lambda img, z: [figur(img, taslar, x, duz(588), 1.2) for x in (60, 700)])
    # Ön plan: 3 çimen tonu + ışık rengi
    on(71, ["#98704c", "#b89062", "#a88056"], "#f0d8a0")

    def kare(t, z, i):          # t: 440x160 saydam tuval, z: son satıra basan düz zemin, i: 0-23
        f = i / KARE
        y = z[0]
        figur(t, at, 110, z, 2.9, 1, "#6b3f24", "#2b1a12", eyer=True, dur=True, bas=0.2)   # at: ızgara x 50+110=160
        if f >= 0.5:
            figur(t, timur, 190, z, 2.6, 1, diz=True)                                       # insan = at boyunun ~%70'i
        else:
            figur(t, timur, 190, z, 2.6, 1, adim=f * 2 % 1, silah="kilic")
        ust = duz(y - 34, 440)                                                              # setin düz üstü (ayrı zemin)
        for j, x in enumerate((340, 375, 410)):
            figur(t, kisi, x, ust, 2.4, "#4a5a3a", "kalpak", "#3a2a1a", "#2a1a12", yon=-1, silah="yay",
                  kol=0.4 if f < 0.5 else 0.0)

    sprite(71, "karakter", 440, 160, KARE, kare)   # kare boyu, 24 kare; taban_denetimi otomatik
```

Sık kullanılan parçalar:

| İstek | Çağrı |
|---|---|
| yürüyen insan | `figur(t, insan, x, z, 2.4, "#3a5a8a", adim=f, yon=1)` |
| adlı kişi (başlık, sakal, silah) | `figur(t, kisi, x, z, 2.6, "#7a1e22", "sarik", "#f4f0e6", "#2a1a12", silah="mizrak", kol=0.3)` — bas: bork, sarik, migfer, kalpak, tac, sapka, kasket, sorguc |
| diz çökmüş | `figur(t, kisi, x, z, 3.0, ..., diz=True)` |
| yürüyen at + binici | `figur(t, at, x, z, 3.1, -1, "#6b3f24", binici="#3a5a8a", faz=f, adim=0.45)` |
| dörtnala atlı savaşçı | `figur(t, atli, x, z, 2.6, 1, faz=f, zirh="#9aa2ac", silah="kilic", adim=0.75)` |
| duran at (otluyor) | `figur(t, at, x, z, 2.3, 1, dur=True, bas=0.8 + 0.2*math.sin(f*2*math.pi))` |
| yurt + duman | `baca = figur(t, yurt, x, z, 3.8, isik=True); duman(t, baca[0], baca[1], 115, 1, faz=f)` |
| otağ (dalgalanan sancak) | `figur(t, otag, x, z, 3.0, "#2a6a3a", "#e0b040", faz=f, acik=True)` |
| kamp ateşi / şamdan / kandil | `ates(t, x, z, f, 1.0)`, `mumluk(t, x, z, f, 3)`, `kandil(t, x, ust_y, f)` |
| orta planda şehir | `ekle=lambda img, z: figur(img, orta_asya_sehri, PAY+20, PAY+280, duz(588), 2.2, tohum=71)` |
| orta planda kalabalık | `kalabalik(img, duz(588), PAY+40, PAY+500, 11, 71, ("#2a2420", "#3a3030"), s=1.1, yon=-1)` |
| yağmur / kar katmanı | `hava(71, "yagmur", 260, egim=0.25, simsek=(5, 17))` / `hava(71, "kar", 180)` — TSX'te `hava: 30` / `hava: 10` |
| iç mekân | `ic_mekan(71, duvar, kemer, cini, pencere=("#1a2a4a", "#f4f8ff"), zemin_renk, hali=True)` sonra `kare` + `sprite` |
| ufukta ikinci sprite | `sprite(71, "karakter2", 248, 68, KARE, kervan)`; `Bolum.sprite` tek sprite alır: ikinci sprite'ı kullanmak için `dosya: "karakter2"` ile ayrı bir sahne yaz ya da hareketsiz kervanı `orta(..., ekle=)` ile orta plana çiz (en kolay yol) |

## 3) TSX `Bolum` satırı

```ts
{
  no: 71, yakin: 1.9, kamera: 30, sprite: { w: 440, h: 160, fps: 10, x: 270, taban: 630 },
  yazilar: [
    { satirlar: ["Sistan'da iki ok yedi:", "sağ dizine, sağ koluna."], sure: 3.2, renk: KIZIL },
    { satirlar: ["Artık", "Aksak Timur'du."], sure: 1.4, boy: 110, renk: ALTIN },
  ],
},
```

- `fps`: yürüyüş 16–20, dörtnala 24–30, olay/iç mekân 8–12, duran sahne 10–14.
- `x: [200, 320]`: sprite sahne boyunca sağa kayar; figürler `yon=1` ve `adim=f` ile yürür.
- Yağmur/kar varsa `hava:`; savaşta `sarsinti: 2`; yakın plan portre için `yakin: 2.8, odakY: 560`.
- Yazı süresi tahmini: harf sayısı / 14 (+0.4 sn); seslendirme gelince kod hizalar.

## Teslim biçimi (grafik_gorevi çıktısı)

1. Sahne planı listesi (her sahne: numara, süre, konu, zemin, hareket, kamera, ses).
2. Her sahne için Python tarifi (yukarıdaki kalıp) — hepsi tek bir `video/piksel/<seri>.py` dosyasına girecek biçimde,
   gerekli `import` satırlarıyla (`from ciz import ...`, `from sahneler import ...`, `from timur_figur import ...`).
3. `Seri` nesnesi: `etiket`, `kapak` (sahip verdiyse), `bolumler[]`, `kapanis`; `video/src/sahneler/<Seri>.tsx` için.
4. "Yeni figür isteği" (varsa): kütüphanede olmayan figürün adı, boyu, zemine nasıl bastığı, hangi sahnede.
