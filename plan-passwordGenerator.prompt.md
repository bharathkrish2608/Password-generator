# Password Generator – improvement plan

1. Security/entropy

- Switch generation to `secrets` instead of `random` in Python; keep symbol set explicit.
- Add plaintext-saving warning before writing to passwords.txt; let user opt in each run.
- Clamp length bounds (min 4, max 64) and validate symbols toggle.

2. CLI UX

- Add argparse flags: `--length`, `--count`, `--no-symbols`, `--save` (path optional), `--quiet`.
- Keep interactive mode as default when no flags; short help text with examples.

3. Robustness

- Harden file writes with try/except and clear errors.
- Validate numeric input (reject blank/invalid, enforce bounds).

4. Tests/tooling

- Add pytest covering generate_password, assess_strength, and CLI arg parsing.
- Add ruff + black + mypy configs; type-hint public functions fully.

5. Web UI alignment

- Ensure JS and Python share the same symbol set and strength rules; document limits.
- Add quick “copy success/failure” state and optional “regenerate” button.

6. Packaging/docs

- Add requirements.txt (or uv/poetry) listing deps (stdlib only, note that).
- Expand README with CLI examples, web UI note, security caveats, and testing commands.

7. Optional next steps

- Provide simple API endpoint (FastAPI/Flask) if backend use is desired.
- Add GitHub Actions for lint + tests.
