# CLAUDE.md

Claude Code loads this file and ignores `AGENTS.md`. The import below pulls in the
shared CrewAI guidance so every coding assistant works from the same instructions.
Keep shared conventions in `AGENTS.md`; add Claude-specific notes under the import.

@AGENTS.md

## Claude-specific notes

- The owner writes in Turkish. Reply in Turkish, and write agent roles, goals, backstories and task text in Turkish unless told otherwise.
- The agents and tasks currently in `config/agents.yaml` and `config/tasks.yaml` are CrewAI's template examples. When the owner describes the team they want, replace them (and the matching methods in `crew.py` and the inputs in `main.py`) instead of adding next to them.
- Models are Claude via the Anthropic provider: default `anthropic/claude-sonnet-5-5` from `MODEL` in `.env`; per-agent overrides go in `agents.yaml` as `llm:`.
- Never commit `.env` or print the API key. `.env.example` holds the variable names only.
- After changing the crew, run `crewai install` and check that `python -c "from ajan_ekibi.crew import AjanEkibi; AjanEkibi().crew()"` builds without errors before committing. A real `crewai run` needs the owner's API key and costs money; ask before running it.

## SKONSTART

This project is **SKONSTART**, the owner's agency of AI agents. Keep its operating model in every change:

- The agents work and think in place of the owner. The owner only gives the job and approves the result.
- The team: `arastirmaci` (research), `metin_yazari` (copy), `editor` (edits for the target audience), `grafiker` (Ghibli-inspired animation plans with the Remotion skill in `skills/remotion-effects/`), `kalite_kontrol` (checks the work and routes revisions).
- The flow lives in `main.py` (`calistir`): research → copy → edit → design → quality control. Quality control returns a `KaliteRaporu`; code (not an agent) sends the work back to the unit it names, following `REVIZYON_ZINCIRI`, at most `MAKS_REVIZYON` times.
- The owner always approves last. In a terminal, `calistir` shows the result and waits: Enter approves, any text is the owner's feedback and goes through quality control again. Without a terminal (`gunluk`, scheduled runs) the result is saved in `teslimler/` as "ONAY BEKLİYOR". Never remove or bypass this approval step.
- The team learns from `hafiza/onaylananlar.md` and `hafiza/geri_bildirimler.md` (fed in as `{gecmis}`) and from the agency profile in `knowledge/ajans_profili.md` (fed in as `{profil}`). CrewAI memory and knowledge sources are not used because their default embedder needs an OpenAI key.
- Every task input is passed on every step (see `durum` in `calistir`), so a new `{placeholder}` in `tasks.yaml` must be added there and in `_ornek_girdiler`.
- The designer reads skill files only through `SkillOkumaAraci`, which cannot leave `skills/`. Do not give agents a general file reader: it could read `.env`.
- New agents are SKONSTART staff: mention the agency in their backstory, write everything in Turkish, and keep outputs directly usable so the owner can approve without extra work.

## Running the agency for the owner in a cloud session

The owner gives jobs in chat and approves in chat. `ANTHROPIC_API_KEY` comes from the cloud environment's variables (never from chat; never print it). Check it is set with `[ -n "$ANTHROPIC_API_KEY" ]` before running.

1. Setup once per session: `uv tool install crewai` if `crewai` is missing, then `crewai install`.
2. A job from the owner: `uv run run_crew "<the job, in the owner's words>" < /dev/null` (run it in the background; a job takes several minutes). With no terminal the result is saved as `teslimler/<date>-<name>.md` with status "ONAY BEKLİYOR", plus a `.json` with the full state.
3. Show the owner the delivery: the post text, the animation plan and the quality control note from the `.md`. If the owner wants a video, save the designer's Remotion code under `video/src/sahneler/`, register it in `video/src/Root.tsx`, render it and send the file.
4. The owner's answer:
   - Approves → `uv run onayla teslimler/<file>.md`
   - Wants changes → `uv run revize teslimler/<file>.md "<the owner's note>"`, then show the new version and ask again.
5. Commit `teslimler/` and `hafiza/` after each approval so the team's memory survives the session, and push.

Never approve on the owner's behalf. Running a job costs the owner money, so run one only when the owner gives a job.
