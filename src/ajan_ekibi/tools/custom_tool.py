from pathlib import Path
from typing import Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

SKILLS_DIR = Path(__file__).resolve().parents[3] / "skills"


class SkillOkumaGirdisi(BaseModel):
    """Input schema for SkillOkumaAraci."""

    dosya: str = Field(
        ...,
        description="skills/ klasörüne göre dosya yolu, ör. 'remotion-effects/SKILL.md' "
        "ya da 'remotion-effects/references/01-orbit.md'",
    )


class SkillOkumaAraci(BaseTool):
    name: str = "Skill dosyası oku"
    description: str = (
        "Ajansın skills/ klasöründeki bir dosyayı okur (ör. Remotion efekt kütüphanesi). "
        "Önce 'remotion-effects/SKILL.md' dosyasını oku, sonra ihtiyacın olan efektin "
        "references/ altındaki dosyasını aç."
    )
    args_schema: Type[BaseModel] = SkillOkumaGirdisi

    def _run(self, dosya: str) -> str:
        # Only files inside skills/ can be read, so agents never reach .env or other project files
        hedef = (SKILLS_DIR / dosya.removeprefix("skills/")).resolve()
        if not hedef.is_relative_to(SKILLS_DIR) or not hedef.is_file():
            mevcut = sorted(
                str(p.relative_to(SKILLS_DIR)) for p in SKILLS_DIR.rglob("*.md")
            )
            return f"Dosya bulunamadı: {dosya}. Okunabilecek dosyalar: {', '.join(mevcut)}"
        return hedef.read_text(encoding="utf-8")
