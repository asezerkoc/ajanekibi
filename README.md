# ajanekibi

[CrewAI](https://github.com/crewAIInc/crewAI) ile kurulmuş, Claude modelini kullanan bir yapay zekâ ajan ekibi.

Ekipteki ajanlar ve görevleri henüz belirlenmedi. Şu an içinde CrewAI'ın örnek ekibi var: bir araştırmacı ve bir raporlayıcı. Görevler verildiğinde bu örnek ajanların yerine gerçek ekip yazılacak.

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
```

Ekibin girdileri (ör. `topic`) `src/ajan_ekibi/main.py` içindedir. Çıktı `report.md` dosyasına yazılır.

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
