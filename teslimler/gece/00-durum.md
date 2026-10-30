# Gece vardiyası (30→31 Ekim 2026) · DURUM

**Engel:** Anthropic API kredisi bitti. Üç paralel işçi 19:58'de aynı anda durdu:
`Your credit balance is too low to access the Anthropic API` (hata, 1., 5. ve 8. konuların metin yazarı adımında).
Bu hata ajansın anahtarıyla (`SKONSTART_API_KEY`) yapılan her çağrıda dönüyor; ekip çalışamıyor.

**Sahibin yapması gereken:** console.anthropic.com → Plans & Billing → kredi yükle. Başka bir şey gerekmez.

**Kredi gelince otomatik devam:** bir bekçi betiği 10 dakikada bir API'yi yokluyor (başarısız çağrı ücretsiz).
Kredi geldiği anda üç işçiyi yeniden başlatıyor. İşçiler kayıtlı adımlardan devam eder; biten araştırmalar
yeniden yaptırılmaz.

## Kurtarılan iş (yeniden ödenmeyecek)

| Konu | Adım | Dosya |
|---|---|---|
| 1 Orhun yazıtları (Thomsen) | 🔵 Araştırma tamam (2.766 kelime) | `teslimler/gece/ara/orhun-yazitlari/1-arastirma.md` |
| 5 Çelebi Mehmed Paris | 🔵 Araştırma tamam (2.305 kelime) | `teslimler/gece/ara/celebi-mehmed-paris/1-arastirma.md` |
| 8 Takiyüddin Rasathanesi | 🔵 Araştırma tamam (2.438 kelime) | `teslimler/gece/ara/takiyuddin-rasathanesi/1-arastirma.md` |
| diğer 7 konu | başlamadı | — |

Her adımın çıktısı artık `teslimler/gece/ara/<konu>/<adım>.md` olarak kaydediliyor (1-arastirma, 2-metin, 3-editor, 4-grafik).

## Plan (değişmedi)

10 konu: Orhun yazıtları · matbaa "yasağı" · Raziye Sultan · Don-Volga kanalı · Çelebi Mehmed'in Paris sefareti ·
Piri Reis · Hezarfen · Takiyüddin Rasathanesi · Barbaros Toulon'da · İrlanda kıtlığı yardımı.

Her konu: araştırma → metin (400-470 kelime, ≥3 dk) → editör (sahip isteği denetimi) → kalite kapısı → grafiker → kalite →
`teslimler/gece/NN-konu.md`. Sonra: ElevenLabs "Metin – Calm Narrator" seslendirme → hizalama → render → `teslimler/video/pikseltarihim-<konu>.mp4`
→ tek dosyada 10 Instagram açıklaması + etiket + sabit yorum (`teslimler/gece/00-yayin-paketi.md`).

Süre tahmini kredi geldikten sonra: metin zinciri konu başına ~25-40 dk (3 paralel), ses + render konu başına ~15 dk.
