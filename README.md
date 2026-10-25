# SKONSTART

SKONSTART, yapay zekâ ajanlarından oluşan bir ajans. Ajanlar ajans sahibinin yerine çalışır ve düşünür. Sahip sadece işi verir, ekibin yaptığı işin sonucunu görür ve onaylar.

[CrewAI](https://github.com/crewAIInc/crewAI) ile kuruldu ve Claude modelini kullanıyor.

## Nasıl çalışır

1. **İşi verirsin:** `crewai run` komutunu çalıştırırsın ve ekibe vereceğin işi yazarsın.
2. **Ekip çalışır:** ajanlar işi sırayla, birbirine devrederek yapar.
3. **Onay verirsin:** son sonuç ekranda sana gösterilir. Boş bırakıp Enter'a basarsan onaylanmış olur. Bir düzeltme yazarsan ekip sonucu ona göre düzeltip tekrar sunar.
4. **Teslim:** onaylanan sonuç `sonuc.md` dosyasına yazılır.

Ekipteki ajanlar henüz belirlenmedi. Şu an içinde örnek bir ekip var: bir araştırmacı ve bir raporlayıcı. Ajansın gerçek çalışanları tanımlanınca onların yerini alacaklar.

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
# SKONSTART - ekibe vereceğin iş: <işi buraya yaz>
```

Ekip işi bitirince sonucu gösterir ve onayını sorar. Onaylanan sonuç `sonuc.md` dosyasına yazılır.

## Model

`.env` içindeki `MODEL` satırı tüm ajanların modelidir. Varsayılan `anthropic/claude-sonnet-5-5`. Daha ucuz ve hızlı bir model için `anthropic/claude-haiku-5-5`, en güçlüsü için `anthropic/claude-opus-5-5` yazabilirsin. Bir ajana ayrı model vermek için `agents.yaml` içinde o ajana `llm: anthropic/claude-haiku-5-5` ekle.

## Proje yapısı

| Dosya | Ne işe yarar |
| --- | --- |
| `src/ajan_ekibi/config/agents.yaml` | Ajanlar: rol, hedef, geçmiş |
| `src/ajan_ekibi/config/tasks.yaml` | Görevler: açıklama, beklenen çıktı, hangi ajan yapacak |
| `src/ajan_ekibi/crew.py` | Ajanları ve görevleri ekip olarak birleştirir |
| `src/ajan_ekibi/main.py` | Ekibi başlatır ve girdileri verir |
| `src/ajan_ekibi/tools/` | Ajanlara verilecek özel araçlar |
| `knowledge/` | Ajanların bilmesi gereken metinler |
