# SKONSTART · İş özeti, 26-30 Ekim 2026

Ajans sahibine toplu rapor: Piksel Tarihim (@pikseltarihim) için yapılan işler, durumları ve ekibin kazandığı yetenekler.

## 1) Yayınlanan ve onaylanan işler

| İş | Durum | Dosya |
|---|---|---|
| Cengiz Han (Bölüm 1, 64-bit piksel, sesli) | Yayınlandı: Instagram + TikTok | `teslimler/video/pikseltarihim-cengiz-han-reels.mp4` (+20/40 MB sürümler) |
| Kayıp Mezar (Cengiz Han'ın mezarı) | Yayınlandı, en çok tutan video | `teslimler/video/pikseltarihim-kayip-mezar-reels.mp4`, kapak `kayip-mezar-kapak.png` |
| Timur 1/3 Topal Kurt (78 sn) | Yayınlandı | `teslimler/video/pikseltarihim-timur-1-topal-kurt.mp4` |
| Timur 2/3 İki Yıldırım (80 sn) | Onaylı, paylaşıldı | `teslimler/video/pikseltarihim-timur-2-iki-yildirim.mp4` |
| Timur 3/3 Lanetli Mezar (88 sn) | Onaylı, sırada | `teslimler/video/pikseltarihim-timur-3-lanetli-mezar.mp4` |
| 29 Ekim story (poster + Remotion efektli video) | Teslim edildi | `teslimler/kapak-29-ekim-story.png`, `video/pikseltarihim-29-ekim-story.mp4` |
| Sosyal medya paketi (açıklamalar, etiketler, takvim, 4K kuralı) | Onaylı | `teslimler/2026-10-27-sosyal-medya-paketi.md` |

## 2) Onay bekleyen işler

### Timur'un Soyundan Kalender (3 dk, piksel)
- Metin: sahibin yönlendirmesiyle yazıldı (Bâbür Kalender Mîrzâ, altı beyitlik gazel bütün), editör düzenledi, **sahip onayladı**.
- Seslendirme: vcvcvc (ElevenLabs klon), 173 sn.
- 18 piksel sahne (72-89), seslendirmeye çapa tabanlı hizalama (`video/ses/hizala_ankor.py`).
- Kalite kontrol 7 tur not verdi; 4-7. turların düzeltmeleri yapıldı (omuz tabutu, tavana bağlı kandiller, ölçek, ay/hilal konumu, çadır, atlılar). Kalan notlar motorun sınırına dayanıyor (profil figür, yüz ifadesi, Arap kara çadırı: yeni figür istekleri).
- Video: `teslimler/video/pikseltarihim-kalender-timurun-soyundan.mp4` (7. tur sürümü). **Sahibin kararı bekleniyor.**

### Cem Sultan'ın Zehirli Tıraşı (1:51, piksel)
- Araştırmacı dosyası: Kutsal Mızrak belgesi (Burchard) ile zehirli tıraş rivayeti (Guicciardini, İnalcık, Vatin) ayrıştırıldı; KAYNAKSIZ listesi.
- Metin: tek soru "O tıraş gerçekten zehirli miydi?"; sahibin notuyla 127 → 194 kelimeye çıktı, kederli tona geçti ("Evi, denizin öbür yanında" → "Kimse onu eve göndermez" → "Eve ancak ölü döner"). Editör 7 maddelik sahip isteği denetimini geçti; kalite kontrol metni onayladı. **Sahip metni onayladı.**
- Seslendirme: Mehmet (sıcak ton), 2. kayıt, 105 sn.
- 32 piksel sahne (90-121), 38 ekran kartı sese hizalı; kapak "Eve dönemeyen şehzade".
- Görsel kalite kontrol: 2 turda düzeltmeler yapıldı (ölçek %30+, ustura, kandiller, Bayezid, Papa, Bursa tabutu, kapak süresi, motif rengi). Kalan 6 not: mızrak uçları yazı bandında, Yenişehir yazı/otağ çakışması, ustura sapı, kapakta logo, teslim sahnesinde at, koyu sahnelerde kontur.
- Video: `teslimler/video/pikseltarihim-cem-sultan-zehirli-tiras.mp4`. **Sahibin kararı bekleniyor.**
- Yayın paketi hazır: açıklama, 8 hashtag, sabit ilk yorum (teslim dosyasında).

## 3) Araştırma ve planlama
- 9 derin yan konu alternatifi (ONAY BEKLİYOR): 1. Cem Sultan ve Kutsal Mızrak (seçildi, üretildi), 2. Karakurum'un Gümüş Ağacı, 3. Raziye Sultan, Kaşgarlı, Orhun yazıtları, matbaa "yasağı" vb. → `teslimler/2026-10-29-yan-konu-alternatifleri.md`
- Ünal 2022 makalesi (DergiPark) özeti: Bâbür Kalender, Timur ve sufiler, Baysungur akademisi → `research_notes/.../ek_unal2022_babur_kalender.md`
- Kalender doğrulama raporu (araştırmacının interneti olmadığı için sınırlı) → `teslimler/2026-10-29-kalender-dogrulama.md`

## 4) Tarz denemeleri (sahibin kararıyla kapatıldı)
- 10 sanat tarzı karşılaştırması (piksel, izometrik, çizgi roman, anime, minyatür, suluboya, vektör, yağlıboya, gravür, low-poly) → `teslimler/2026-10-29-sanat-tarzlari/`
- Kalender low-poly 3D sürümü: 19 görsel + Remotion kamera hareketi, 2 kalite turu (uygun). Karakterler hareket etmediği için sahip iptal etti; piksel tarzına dönüldü. Video arşivde: `pikseltarihim-kalender-lowpoly-deneme.mp4`.
- Higgsfield / Kling 3.0 için X Paşa darağacı sahnesi (sahne 71) ve İngilizce prompt.

## 5) Ekibin kazandığı yetenekler ve araçlar
- 🟢 Grafiker: `skills/piksel-sahne/` (katmanlar, zemin çizgileri, ölçek, kamera; 97 fonksiyon, 56 sahne kataloğu). Yeni figürler: darağacı, asılı, kahkaha atan paşa, rahle, taht, kitaplar, omuz tabutu; Cem Sultan'da ölçüm tabanlı yerleşim (`olcek`, `_kadraj`, ustura hizası).
- 🔵 Araştırmacı: derin araştırma kuralları (birincil/ikincil kaynak, tartışmalılar ayrı, KAYNAKSIZ listesi, 10 katmanlı rapor).
- 🟠 Metin yazarı: 10 ilgi çekicilik kuralı (tek soru, açık döngü kanca, "ama" dönüşü, şimdiki zaman, somut detay).
- 🟣 Editör: ilgi denetimi ve sahip isteği denetimi tablosu.
- 🔴 Kalite kontrol: metin kapısı (grafiker, metin onaylanmadan başlamaz) ve render karelerinde görsel kontrol (`uv run gorsel_kontrol`).
- Kod: `TimurSeri.tsx` düz görsel sahnesi (Ken Burns), yazı tipi bağlamı, `hizala_seri.py` + `hizala_ankor.py`, render betiği, 4K sürüm kuralı.
- Hafıza: `hafiza/onaylananlar.md` (onaylar, yayınlar), `hafiza/geri_bildirimler.md` (araştırma, metin, revizyon notları).

## 6) Hesaplar ve kredi kullanımı
- TikTok hesabı açıldı; Cengiz Han paylaşıldı. Instagram'da Kayıp Mezar, Timur 1 ve 2 yayında.
- ElevenLabs: Kalender (vcvcvc) 2 kayıt, Cem Sultan (Mehmet) 4 kayıt, 9 tarz görseli + 21 low-poly görsel ≈ 11.900 kredi; abonelik kotasından düştü, ayrı ödeme yok.
- Higgsfield: 113 kredi, CDN engelli (ağ izni gerekir).

## 7) Açık kararlar (sahibe)
1. Kalender 7. tur sürümü: onay mı, yeni figürlerle (profil taşıyıcı, kara çadır) 8. tur mu?
2. Cem Sultan revize sürümü: onay mı, kalan 6 notla son tur mu?
3. Sıradaki konu: Gümüş Ağaç (Karakurum) ya da Raziye Sultan; araştırmacı raporu hazır.
4. Araştırmacıya internet: Serper anahtarı; Higgsfield için ağ izni.
