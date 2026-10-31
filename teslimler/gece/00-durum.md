# Gece vardiyası (30→31 Ekim 2026) · DURUM

**03:30 · Sahibin kararı:** CrewAI ekibi (Anthropic API kredisi bitti) devre dışı. İşi Claude Code oturumu, beş alt ajana bölünerek
kendisi yürütüyor: 🔵 araştırmacı, 🟠 metin yazarı, 🟣 editör, 🟢 grafiker, 🔴 kalite kontrol. API kredisi gerekmiyor.
Roller aynı kuralları kullanıyor (config/agents.yaml, config/tasks.yaml, ajans profili, hafıza); alt ajanların
brifleri sahibin gece kararlarını (≥3 dk, 400-470 kelime, niş ve derin, havada cümle yok, hata yok) taşıyor.

Fark: yeni araştırmacıların interneti var (kaynaklar URL'li); grafiker tarifi yazmakla kalmıyor, çiziyor ve sprite'lara bakıp düzeltiyor.

## Zincir (her konu)
1-arastirma → 2-metin → 3-editor → 4-kalite-metin (kapı) → 5-grafik (py + tsx, çizim denetimi) → seslendirme (ElevenLabs "Metin – Calm Narrator")
→ hizalama + bundle + 12 kare → 6-kalite-gorsel → düzeltme → render → `teslimler/video/pikseltarihim-<slug>.mp4` → `teslimler/gece/NN-<slug>.md`
Son: `teslimler/gece/00-yayin-paketi.md` (10 açıklama, etiket, sabit yorum).

## İlerleme (31 Ekim, son güncelleme)
| # | slug | metin zinciri | grafik | ses (Metin) | görsel KK | video |
|---|---|---|---|---|---|---|
| 1 | orhun-yazitlari | ✅ | ✅ | ✅ | ✅ 3. tur | ⏳ render |
| 2 | matbaa-yasagi | ✅ | 🔁 düzeltme | ✅ | ❌ 1. tur | |
| 3 | raziye-sultan | ✅ | ✅ | ✅ | ⏳ | |
| 4 | don-volga-kanali | ✅ | ⏳ | ✅ | | |
| 5 | celebi-mehmed-paris | ✅ | ✅ | ✅ | ✅ | ✅ |
| 6 | piri-reis | ✅ | 🔁 düzeltme | ✅ | ❌ 1. tur | |
| 7 | hezarfen | ✅ | ✅ | ✅ | ✅ 2. tur | ⏳ sırada |
| 8 | takiyuddin-rasathanesi | ✅ | ✅ | ✅ | ✅ | ✅ |
| 9 | toulon-1543 | ✅ | ⏳ | ✅ | | |
| 10 | irlanda-kitligi | ✅ | ⏳ | ✅ | | |

Kesintiler: abonelik kullanım sınırı iki kez doldu (05:30 ve 08:40 civarı; 10 paralel ajan fazlaydı). 14:24'ten itibaren
model Opus 5.5, aynı anda en çok 5 ajan.

Geçmiş: 19:58 CrewAI işçileri kredi hatasıyla durdu; 22:57-03:07 saatlik kontrollerde kredi gelmedi; 03:30 sahip "kendin ajans ol" dedi.
