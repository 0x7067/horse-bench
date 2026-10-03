# Horse Bench

[Gallery](https://0x7067.github.io/horse-bench/) · [Repository](https://github.com/0x7067/horse-bench)

Run with Python 3 and an installed, authenticated harness:

```sh
python3 generate.py --harness claude --model claude-opus-5-5 --effort high --output results/claude-opus-5.5-high
python3 generate.py --harness codex --model gpt-6.1-sol --effort high --output results/codex-sol-6.1-high
python3 generate.py --harness jcode --provider zai --model glm-5.3-flash --output results/jcode-glm-5.3-flash
python3 generate.py --harness pi --model devin/swe-2 --output results/pi-swe-2
```

The default prompt generates the running horse. Override it with `--prompt "..."`.
Choose `claude`, `codex`, `jcode`, `pi`, `cline`, or `dsh` with `--harness`; supply the exact model ID with `--model`.
Use `--provider` for Jcode, Pi, or Cline provider selection. Pi also accepts `provider/model` directly.
Use `--effort` for Claude, Codex, or Pi. Omitting it uses the harness default.
Each run saves the response to `index.html` in the output folder, replacing an existing file.
Runs have no execution timeout. Raw stdout and stderr are saved alongside the HTML. Codex also saves `response.txt`.
Claude, Jcode, and Pi run without tools. Codex runs in its read-only sandbox.

Headless invocation follows the [Claude Code guide](https://code.claude.com/docs/en/headless),
[Codex guide](https://learn.chatgpt.com/docs/non-interactive-mode),
[Jcode README](https://github.com/1jehuang/jcode), and
[Pi README](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent).

DeepSeek subscription examples:

```sh
python3 generate.py --harness pi --provider opencode-go --model deepseek-v4-flash --output results/pi-deepseek-v4-flash
python3 generate.py --harness jcode --provider opencode-go --model deepseek-v4-pro --output results/jcode-deepseek-v4-pro
python3 generate.py --harness cline --provider cline-pass --model cline-pass/deepseek-v4-pro --output results/cline-deepseek-v4-pro
python3 generate.py --harness dsh --model deepseek-v4-flash --output results/dsh-deepseek-v4-flash
```

Cline runs headlessly with `--auto-approve true --json` from a temporary directory. DSH uses its headless profile and a per-run model patch.
DSH uses the configured DeepSeek API credentials.
Model IDs are recorded as supplied to each harness.
See the [Cline CLI guide](https://docs.cline.bot/cli/cli-reference), [ClinePass models](https://github.com/cline/cline/blob/main/docs/getting-started/clinepass.mdx), [OpenCode Go models](https://opencode.ai/docs/go/), and [DSH guide](https://github.com/deepseek-ai/deepseek-harness).

All 19 runs returned HTML. Generated files load Three.js from a CDN, so they need internet access. Inline JavaScript syntax and browser canvas creation were checked; animation quality was not graded. Large raw logs are gzip-compressed. Earlier failed attempts are recorded in `results/attempts/`.

`runs.json` records the configurations. `results.json` records outcomes. Each `results/<run>/` contains the generated HTML and harness logs. `docs/` contains the GitHub Pages gallery and copies of the original HTML. Rebuild the gallery with `python3 build_index.py`. GitHub Pages publishes `main` / `docs`.
