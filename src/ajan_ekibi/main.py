#!/usr/bin/env python
import json
import re
import sys
import warnings

from datetime import datetime
from pathlib import Path

from ajan_ekibi.crew import AjanEkibi, KaliteRaporu

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

KOK = Path(__file__).resolve().parents[2]
PROFIL = KOK / "knowledge" / "ajans_profili.md"
ONAYLANANLAR = KOK / "hafiza" / "onaylananlar.md"
GERI_BILDIRIMLER = KOK / "hafiza" / "geri_bildirimler.md"
TESLIMLER = KOK / "teslimler"

# Quality control can send work back at most this many times before it goes to the owner anyway
MAKS_REVIZYON = 3

# Which steps run again when a unit gets work back: a text change must pass the editor and designer again
REVIZYON_ZINCIRI = {
    "metin_yazari": ["metin", "editor", "grafik"],
    "editor": ["editor", "grafik"],
    "grafiker": ["grafik"],
}

GUNLUK_GOREV = (
    "Bugünün günlük gönderisi. Ajans profilindeki konulardan, geçmişte işlenmemiş "
    "ve hedef kitle için şu an en ilgi çekici olanı seç; metni ve animasyonu hazırla."
)


def _oku(yol: Path, son_karakter: int | None = None) -> str:
    if not yol.exists():
        return ""
    metin = yol.read_text(encoding="utf-8")
    return metin[-son_karakter:] if son_karakter else metin


def _ekle(yol: Path, metin: str) -> None:
    yol.parent.mkdir(parents=True, exist_ok=True)
    with yol.open("a", encoding="utf-8") as f:
        f.write(metin)


def _adim(gorev_adi: str, durum: dict) -> str:
    sonuc = AjanEkibi().tek_gorev(gorev_adi).kickoff(inputs=durum)
    return sonuc.raw


def _kalite(durum: dict) -> KaliteRaporu:
    sonuc = AjanEkibi().tek_gorev("kalite_gorevi").kickoff(inputs=durum)
    rapor = sonuc.pydantic
    if not isinstance(rapor, KaliteRaporu):
        rapor = KaliteRaporu.model_validate_json(sonuc.raw)
    return rapor


def _zinciri_calistir(adimlar: list[str], durum: dict) -> None:
    if "metin" in adimlar:
        durum["metin"] = _adim("metin_gorevi", durum)
    if "editor" in adimlar:
        durum["duzenlenmis_metin"] = _adim("editor_gorevi", durum)
    if "grafik" in adimlar:
        durum["grafik"] = _adim("grafik_gorevi", durum)


def _kalite_dongusu(durum: dict) -> KaliteRaporu:
    """Quality control checks the work and sends it back to the right unit until it passes."""
    for tur in range(MAKS_REVIZYON + 1):
        rapor = _kalite(durum)
        durum["sahip_notu"] = ""
        if rapor.uygun or rapor.revize_birimi == "yok":
            return rapor
        if tur == MAKS_REVIZYON:
            break
        print(f"\n[Kalite kontrol] Revizyon {tur + 1}: {rapor.revize_birimi} -> {rapor.notlar}\n")
        durum["revizyon_notu"] = rapor.notlar
        _zinciri_calistir(REVIZYON_ZINCIRI[rapor.revize_birimi], durum)
        durum["revizyon_notu"] = ""
    return rapor


def _teslim_metni(durum: dict, rapor: KaliteRaporu, onay_durumu: str) -> str:
    return (
        f"# SKONSTART teslimi\n\n"
        f"- **İş:** {durum['gorev']}\n"
        f"- **Tarih:** {datetime.now():%Y-%m-%d %H:%M}\n"
        f"- **Durum:** {onay_durumu}\n"
        f"- **Kalite kontrol:** {'uygun' if rapor.uygun else 'revizyon sınırına ulaşıldı, son notlar aşağıda'}\n\n"
        f"## Gönderi metni\n\n{durum['duzenlenmis_metin']}\n\n"
        f"## Animasyon ve grafik\n\n{durum['grafik']}\n\n"
        f"## Kalite kontrol notu\n\n{rapor.notlar}\n\n"
        f"## Araştırma\n\n{durum['arastirma']}\n"
    )


def _kaydet(durum: dict, rapor: KaliteRaporu, onay_durumu: str, yol: Path | None = None) -> Path:
    """Writes the delivery (.md for the owner) and its full state (.json, so it can be approved or revised later)."""
    if yol is None:
        TESLIMLER.mkdir(parents=True, exist_ok=True)
        kisa_ad = durum["gorev"].translate(str.maketrans("çğıöşüÇĞİÖŞÜ", "cgiosuCGIOSU")).lower()
        kisa_ad = re.sub(r"[^a-z0-9]+", "-", kisa_ad)[:40].strip("-") or "is"
        yol = TESLIMLER / f"{datetime.now():%Y-%m-%d-%H%M}-{kisa_ad}.md"
    yol.write_text(_teslim_metni(durum, rapor, onay_durumu), encoding="utf-8")
    yol.with_suffix(".json").write_text(
        json.dumps({"durum": durum, "rapor": rapor.model_dump()}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return yol


def _yukle(yol: Path) -> tuple[dict, KaliteRaporu]:
    veri = json.loads(yol.with_suffix(".json").read_text(encoding="utf-8"))
    return veri["durum"], KaliteRaporu.model_validate(veri["rapor"])


def _gecmis() -> str:
    # The team learns from what the owner approved and said before
    return (
        "Onaylanan son işler:\n" + (_oku(ONAYLANANLAR, 4000) or "Henüz yok.")
        + "\n\nAjans sahibinin geri bildirimleri:\n" + (_oku(GERI_BILDIRIMLER, 4000) or "Henüz yok.")
    )


def _sahip_notunu_uygula(durum: dict, not_: str) -> KaliteRaporu:
    """The owner's feedback is remembered and goes through quality control, which routes it to the right unit."""
    _ekle(GERI_BILDIRIMLER, f"- {datetime.now():%Y-%m-%d} ({durum['gorev'][:60]}): {not_}\n")
    durum["gecmis"] = _gecmis()
    durum["sahip_notu"] = not_
    return _kalite_dongusu(durum)


def _onayla(durum: dict, rapor: KaliteRaporu, yol: Path | None = None) -> Path:
    yol = _kaydet(durum, rapor, "ONAYLANDI", yol)
    _ekle(
        ONAYLANANLAR,
        f"\n## {datetime.now():%Y-%m-%d} — {durum['gorev'][:80]}\n\n{durum['duzenlenmis_metin'][:600]}\n",
    )
    print(f"\nOnaylandı ve kaydedildi: {yol}")
    return yol


def calistir(gorev: str, etkilesimli: bool) -> Path:
    """The whole agency at work: research, write, edit, design, quality control, owner approval."""
    durum = {
        "gorev": gorev,
        "current_year": str(datetime.now().year),
        "profil": _oku(PROFIL),
        "gecmis": _gecmis(),
        "arastirma": "",
        "metin": "",
        "duzenlenmis_metin": "",
        "grafik": "",
        "revizyon_notu": "",
        "sahip_notu": "",
    }

    durum["arastirma"] = _adim("arastirma_gorevi", durum)
    _zinciri_calistir(["metin", "editor", "grafik"], durum)
    rapor = _kalite_dongusu(durum)

    if not etkilesimli:
        # Nobody is at the terminal (scheduled run): the work waits in teslimler/ for the owner
        yol = _kaydet(durum, rapor, "ONAY BEKLİYOR")
        print(f"\nTeslim onayını bekliyor: {yol}")
        return yol

    while True:
        print("\n" + "=" * 70)
        print(_teslim_metni(durum, rapor, "ONAYINI BEKLİYOR"))
        print("=" * 70)
        cevap = input(
            "\nOnaylıyorsan Enter'a bas. Değişiklik istiyorsan ne değişsin, yaz: "
        ).strip()
        if not cevap:
            break
        rapor = _sahip_notunu_uygula(durum, cevap)

    return _onayla(durum, rapor)


def run():
    """
    Run the agency. The job comes from the command line or is asked for.
    """
    gorev = " ".join(sys.argv[1:]).strip() or input(
        "SKONSTART - ekibe vereceğin iş (boş bırakırsan günlük gönderi): "
    ).strip()

    try:
        calistir(gorev or GUNLUK_GOREV, etkilesimli=sys.stdin.isatty())
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def gunluk():
    """
    Daily run for a scheduler: the team picks today's topic itself and the result waits for approval.
    """
    try:
        return calistir(GUNLUK_GOREV, etkilesimli=False)
    except Exception as e:
        raise Exception(f"An error occurred while running the daily crew: {e}")


def onayla():
    """
    Approve a delivery waiting in teslimler/: uv run onayla teslimler/<file>.md
    """
    if len(sys.argv) < 2:
        raise Exception("Kullanım: uv run onayla teslimler/<dosya>.md")
    yol = Path(sys.argv[1])
    durum, rapor = _yukle(yol)
    return _onayla(durum, rapor, yol)


def revize():
    """
    Send a waiting delivery back with the owner's note: uv run revize teslimler/<file>.md "<note>"
    """
    if len(sys.argv) < 3:
        raise Exception('Kullanım: uv run revize teslimler/<dosya>.md "ne değişsin"')
    yol = Path(sys.argv[1])
    durum, _ = _yukle(yol)
    try:
        rapor = _sahip_notunu_uygula(durum, " ".join(sys.argv[2:]).strip())
    except Exception as e:
        raise Exception(f"An error occurred while revising: {e}")
    yol = _kaydet(durum, rapor, "ONAY BEKLİYOR", yol)
    print(f"\nRevize edildi, onayını bekliyor: {yol}")
    return yol


def _ornek_girdiler() -> dict:
    return {
        "gorev": "Yapay zekâ ajanları hakkında bir gönderi hazırla",
        "current_year": str(datetime.now().year),
        "profil": _oku(PROFIL),
        "gecmis": "",
        "arastirma": "",
        "metin": "",
        "duzenlenmis_metin": "",
        "grafik": "",
        "revizyon_notu": "",
        "sahip_notu": "",
    }


def train():
    """
    Train the crew for a given number of iterations.
    """
    try:
        AjanEkibi().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=_ornek_girdiler())

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        AjanEkibi().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    try:
        AjanEkibi().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=_ornek_girdiler())

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

def run_with_trigger():
    """
    Run the crew with trigger payload.
    """
    import json

    if len(sys.argv) < 2:
        raise Exception("No trigger payload provided. Please provide JSON payload as argument.")

    try:
        trigger_payload = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        raise Exception("Invalid JSON payload provided as argument")

    try:
        gorev = trigger_payload.get("gorev") if isinstance(trigger_payload, dict) else None
        return calistir(gorev or GUNLUK_GOREV, etkilesimli=False)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew with trigger: {e}")
