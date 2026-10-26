from typing import Literal

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from pydantic import BaseModel, Field

from ajan_ekibi.tools.custom_tool import SkillOkumaAraci


# Each unit's visual color code: shown in the terminal while it works and on the deliveries
AJAN_RENKLERI = {
    "arastirmaci": {"ad": "Araştırmacı", "emoji": "🔵", "renk": "Mavi", "hex": "#3B82F6", "ansi": "\033[94m"},
    "metin_yazari": {"ad": "Metin Yazarı", "emoji": "🟠", "renk": "Turuncu", "hex": "#F97316", "ansi": "\033[38;5;208m"},
    "editor": {"ad": "Editör", "emoji": "🟣", "renk": "Mor", "hex": "#8B5CF6", "ansi": "\033[95m"},
    "grafiker": {"ad": "Grafiker", "emoji": "🟢", "renk": "Yeşil", "hex": "#22C55E", "ansi": "\033[92m"},
    "kalite_kontrol": {"ad": "Kalite Kontrol", "emoji": "🔴", "renk": "Kırmızı", "hex": "#EF4444", "ansi": "\033[91m"},
}

GOREV_BIRIMI = {
    "arastirma_gorevi": "arastirmaci",
    "metin_gorevi": "metin_yazari",
    "editor_gorevi": "editor",
    "grafik_gorevi": "grafiker",
    "kalite_gorevi": "kalite_kontrol",
}


def etiket(birim: str, renkli: bool = False) -> str:
    """The unit's badge, e.g. '🔵 Araştırmacı'; colored for a terminal when renkli is True."""
    r = AJAN_RENKLERI[birim]
    metin = f"{r['emoji']} {r['ad']}"
    return f"{r['ansi']}{metin}\033[0m" if renkli else metin


class KaliteRaporu(BaseModel):
    """Kalite kontrolün kararı. Revizyonun hangi birime gideceğini kod buna göre seçer."""

    uygun: bool = Field(description="İş hedef kitleye ve ajans standartlarına uygunsa true")
    revize_birimi: Literal["metin_yazari", "editor", "grafiker", "yok"] = Field(
        description="Uygun değilse sorunu düzeltecek birim, uygunsa 'yok'"
    )
    notlar: str = Field(description="Değerlendirme ya da somut revizyon notları")


@CrewBase
class AjanEkibi():
    """SKONSTART ajansı: sahibi işi verir, ekip yapar, son sonuç sahibinin onayına sunulur."""

    agents: list[BaseAgent]
    tasks: list[Task]

    @agent
    def arastirmaci(self) -> Agent:
        return Agent(
            config=self.agents_config['arastirmaci'], # type: ignore[index]
            verbose=True
        )

    @agent
    def metin_yazari(self) -> Agent:
        return Agent(
            config=self.agents_config['metin_yazari'], # type: ignore[index]
            verbose=True
        )

    @agent
    def editor(self) -> Agent:
        return Agent(
            config=self.agents_config['editor'], # type: ignore[index]
            verbose=True
        )

    @agent
    def grafiker(self) -> Agent:
        return Agent(
            config=self.agents_config['grafiker'], # type: ignore[index]
            tools=[SkillOkumaAraci()],
            verbose=True
        )

    @agent
    def kalite_kontrol(self) -> Agent:
        return Agent(
            config=self.agents_config['kalite_kontrol'], # type: ignore[index]
            verbose=True
        )

    @task
    def arastirma_gorevi(self) -> Task:
        return Task(
            config=self.tasks_config['arastirma_gorevi'], # type: ignore[index]
        )

    @task
    def metin_gorevi(self) -> Task:
        return Task(
            config=self.tasks_config['metin_gorevi'], # type: ignore[index]
        )

    @task
    def editor_gorevi(self) -> Task:
        return Task(
            config=self.tasks_config['editor_gorevi'], # type: ignore[index]
        )

    @task
    def grafik_gorevi(self) -> Task:
        return Task(
            config=self.tasks_config['grafik_gorevi'], # type: ignore[index]
        )

    @task
    def kalite_gorevi(self) -> Task:
        return Task(
            config=self.tasks_config['kalite_gorevi'], # type: ignore[index]
            output_pydantic=KaliteRaporu
        )

    @crew
    def crew(self) -> Crew:
        """Creates the SKONSTART crew (all five steps once, in order).

        The day-to-day flow with revisions and the owner's approval is in main.py.
        """
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )

    def tek_gorev(self, gorev_adi: str) -> Crew:
        """A crew that runs only one step, used by main.py to send work back for revision."""
        gorev = getattr(self, gorev_adi)()
        return Crew(agents=[gorev.agent], tasks=[gorev], verbose=True)
