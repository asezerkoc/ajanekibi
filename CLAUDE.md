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
- The job comes in as the `gorev` input (`main.py` asks for it, or takes it from the command line). Every task text uses `{gorev}`.
- The final task of the crew always has `human_input=True`, so the result is shown to the owner for approval before it is written to `sonuc.md`. Never remove this approval step.
- New agents are SKONSTART staff: mention the agency in their backstory, write everything in Turkish, and keep outputs directly usable so the owner can approve without extra work.
