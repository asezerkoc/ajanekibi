import os

# Cloud sessions reserve ANTHROPIC_API_KEY for Claude Code's own login, so the
# owner can store the agency's key as SKONSTART_API_KEY instead.
if not os.environ.get("ANTHROPIC_API_KEY") and os.environ.get("SKONSTART_API_KEY"):
    os.environ["ANTHROPIC_API_KEY"] = os.environ["SKONSTART_API_KEY"]
