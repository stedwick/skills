**Simplify** Always try the simplest possible solution first. Don't go with your first draft. Think about it and come up with a second draft that's simpler.

**Dev servers** Use portless `portless --help` at `--tld dev` for running dev servers.

**Git Butler** Use git butler `but skill` to manage git unless otherwise specified. Use `gh` CLI for GitHub stuff.

**Browsers** Prefer your built-in browsers. If you don't have a browser, use agent-browser `agent-browser skills get core`. Search the web using your built-in tool first. Use Exa through Executor if you need a deeper search. Prefer no-sound.

**Headless Chrome** For headless screenshots or advanced scripted browsing, use agent-browser w/ Google's headless-only Chrome at `~/.cache/chrome-headless-shell/chrome-headless-shell-mac-arm64/chrome-headless-shell` (Chrome for Testing). If installed in a different place, use that. If not installed, ask the user.

**Image generation** Prefer your own built-in tool, otherwise use Codex CLI with my ChatGPT plan. Run it from the output folder: `codex exec --skip-git-repo-check -s workspace-write "Generate an image: <prompt>. Save it as <name>.png in the current directory."` Codex needs network access and `~/.codex`, so run it outside the sandbox.

**Executor** Use Executor to access my additional signed-in tools like Exa or ElevenLabs. If it's less than $1, you have permission without asking.

**Monid** Use `monid --help` for additional premium tools. This also has ElevenLabs. If it's less than $1, you have permission without asking.
