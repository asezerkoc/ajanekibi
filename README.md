# SKONSTART

SKONSTART, yapay zekâ ajanlarından oluşan bir ajans. Ajanlar ajans sahibinin yerine çalışır ve düşünür. Sahip sadece işi verir, sonucu görür ve onaylar.

[CrewAI](https://github.com/crewAIInc/crewAI) ile kuruldu ve Claude modelini kullanıyor.

## Ekip

| Ajan | Görevi |
| --- | --- |
| **Araştırmacı** | Verilen işi araştırır. İş konu belirtmiyorsa ajansın konularından, daha önce işlenmemiş olanı kendisi seçer. |
| **Metin yazarı** | Araştırmaya dayanarak gönderi metnini yazar: kanca, ana metin, kapanış, hashtag'ler, videoda ekrana yazılacak cümleler. |
| **Editör** | Metni dil, akış ve doğruluk açısından kontrol eder, hedef kitleye göre düzenler. |
| **Grafiker** | Metni Ghibli-esinli, el çizimi havasında bir animasyona dönüştürür: sahne planı, görsel üretme komutları ve ajansın Remotion efekt kütüphanesiyle yazılmış video kodu. |
| **Kalite kontrol** | İşin hedef kitleye ve ajansın tarzına uygun olup olmadığına bakar. Uygun değilse sorunu düzeltecek birime notlarıyla geri gönderir. Uygunsa sana sunar. |

## Nasıl çalışır

1. **İşi verirsin:** `crewai run` komutunu çalıştırıp işi yazarsın. Boş bırakırsan ekip o günün gönderisini kendisi seçer.
2. **Ekip çalışır:** araştırma → metin → editör → grafik → kalite kontrol.
3. **Revizyon:** kalite kontrol beğenmezse işi ilgili birime geri gönderir. Metin sorunu metin yazarına, ton ve dil sorunu editöre, görsel sorunu grafikere gider. En fazla 3 tur revizyon yapılır.
4. **Onay verirsin:** sonuç ekranda gösterilir. Enter'a basarsan onaylanır. Bir şey yazarsan bu senin notun olur, ekip düzeltip tekrar sunar.
5. **Teslim:** sonuç `teslimler/` klasörüne kaydedilir.
6. **Öğrenme:** onayladığın işler `hafiza/onaylananlar.md`'ye, notların `hafiza/geri_bildirimler.md`'ye yazılır. Ekip her işte bunları okur ve zamanla senin zevkini öğrenir.

## Önce bunu doldur

`knowledge/ajans_profili.md` dosyası ekibin "beyni": ajansın ne yaptığı, konular, hedef kitle, marka sesi ve görsel tarz. Köşeli parantezli yerleri doldurmazsan ekip hedef kitleyi tahmin etmek zorunda kalır.

## Kurulum

Python 3.10–3.13 ve [uv](https://docs.astral.sh/uv/) gerekir.

```sh
uv tool install crewai          # CrewAI komut satırı aracı
cp .env.example .env            # ayar dosyasını oluştur
# .env içine Anthropic API anahtarını yaz: ANTHROPIC_API_KEY=sk-ant-...
crewai install                  # bağımlılıkları kur
```

API anahtarı https://console.anthropic.com adresinden alınır. `.env` dosyası git'e eklenmez, anahtarı başka bir yere yazma.

## Çalıştırma

```sh
crewai run
# SKONSTART - ekibe vereceğin iş (boş bırakırsan günlük gönderi): <işi yaz>
```

Bir iş, revizyonlarla birlikte 5-15 Claude çağrısı yapar. Ücret, Anthropic hesabındaki kullanıma göre ödenir.

## Her gün kendi kendine çalışma

`gunluk` komutu ekibe o günün gönderisini hazırlatır. Kimse ekran başında olmadığı için sonucu "ONAY BEKLİYOR" olarak `teslimler/` klasörüne bırakır. Sen sonra bakıp onaylarsın.

```sh
uv run gunluk
```

Her sabah otomatik çalışması için bir zamanlayıcı gerekir. Mac veya Linux'ta `crontab -e` ile şunu ekle (her gün 09:00):

```
0 9 * * * cd /proje/yolu/ajanekibi && /usr/local/bin/uv run gunluk >> gunluk.log 2>&1
```

Bilgisayar kapalıyken de çalışsın istersen projeyi CrewAI'ın bulut hizmetine (CrewAI AMP) yükleyip orada zamanlama kurman gerekir.

## Grafikerin çıktısı nasıl videoya dönüşür

Grafiker resim ya da video dosyası üretmez. Üç şey teslim eder:

1. **Sahne planı:** her sahnenin süresi, efekti ve ekranda yazacak metin.
2. **Görsel komutları:** her sahnenin arka planı için, görsel üretme araçlarına (Midjourney, Ideogram, Flux vb.) yapıştırılacak İngilizce komutlar.
3. **Remotion kodu:** `skills/remotion-effects/` kütüphanesindeki efektlerle yazılmış video kodu.

Video stüdyosu `video/` klasöründe hazır: 22 efektin hepsi `video/src/effects/` altında kurulu. Örnek olarak `video/src/sahneler/Tanitim.tsx` içinde 18 saniyelik bir SKONSTART tanıtım videosu var.

```sh
cd video
npm install                     # ilk seferde
npm run dev                     # Remotion Studio: videoları tarayıcıda önizle
npx remotion render src/index.ts Tanitim out/tanitim.mp4
```

Grafikerin kodunu `video/src/sahneler/` altına kaydet, `video/src/Root.tsx` içine bir `<Composition>` olarak ekle, görselleri `video/public/` klasörüne koy ve render et.

## Model

`.env` içindeki `MODEL` satırı bütün ajanların modelidir. Varsayılan `anthropic/claude-sonnet-5-5`. Daha ucuz bir model için `anthropic/claude-haiku-5-5`, en güçlüsü için `anthropic/claude-opus-5-5` yaz. Bir ajana ayrı model vermek için `agents.yaml` içinde o ajana `llm: anthropic/claude-haiku-5-5` ekle.

## Proje yapısı

| Dosya | Ne işe yarar |
| --- | --- |
| `knowledge/ajans_profili.md` | Ajansın konuları, hedef kitlesi, marka sesi, görsel tarzı |
| `src/ajan_ekibi/config/agents.yaml` | Ajanlar: rol, hedef, geçmiş |
| `src/ajan_ekibi/config/tasks.yaml` | Her ajanın görevi ve teslim etmesi gereken çıktı |
| `src/ajan_ekibi/crew.py` | Ajanları ve görevleri tanımlar; kalite raporunun biçimi |
| `src/ajan_ekibi/main.py` | Çalışma akışı: revizyon döngüsü, onay, teslim, hafıza, günlük mod |
| `src/ajan_ekibi/tools/custom_tool.py` | Grafikerin efekt kütüphanesini okuma aracı |
| `skills/remotion-effects/` | 22 test edilmiş Remotion efekti (grafikerin başvuru kütüphanesi) |
| `video/` | Remotion video stüdyosu: kurulu efektler ve sahneler |
| `hafiza/` | Onaylanan işler ve geri bildirimler (ekibin öğrendikleri) |
| `teslimler/` | Ekibin teslim ettiği işler |
