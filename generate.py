#!/usr/bin/env python3
import argparse
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path


PROMPT = "Create a low-poly 3D horse running in a seamless loop using Three.js. Build it procedurally from primitive geometry, animate the legs, body, head, and tail, and return a single self-contained HTML file."


def main():
    parser = argparse.ArgumentParser(description="Generate an HTML file with a headless coding harness.")
    parser.add_argument("--harness", choices=["claude", "codex", "jcode", "pi", "cline", "dsh"], default="claude")
    parser.add_argument("--model", required=True)
    parser.add_argument("--provider")
    parser.add_argument("--effort", choices=["off", "minimal", "low", "medium", "high", "xhigh", "max"])
    parser.add_argument("--prompt", default=PROMPT)
    parser.add_argument("--output", type=Path, default=Path("output"))
    args = parser.parse_args()

    harness = shutil.which(args.harness)
    if not harness:
        parser.exit(1, f"{args.harness} is not installed or is not on PATH.\n")
    if args.provider and args.harness not in {"jcode", "pi", "cline"}:
        parser.error("--provider is supported by jcode, pi, and cline")
    if args.effort and args.harness == "jcode":
        parser.error("jcode run has no effort flag")
    if args.harness == "claude" and args.effort in {"off", "minimal"}:
        parser.error("Claude effort must be low, medium, high, xhigh, or max")

    args.output.mkdir(parents=True, exist_ok=True)
    output = args.output.resolve()
    prompt = args.prompt + "\nReturn only the HTML, without Markdown fences or explanation. Do not write files or use tools; your final answer must contain the complete HTML source, which the caller saves."
    if args.harness == "claude":
        command = [harness, "-p", "--model", args.model, "--output-format", "text", "--tools", ""]
        if args.effort:
            command += ["--effort", args.effort]
        command += ["--"]
    elif args.harness == "codex":
        command = [harness, "exec", "--model", args.model, "--skip-git-repo-check",
                   "--ignore-user-config", "--ephemeral", "--sandbox", "read-only", "--color", "never",
                   "--output-last-message", str(output / "response.txt")]
        if args.effort:
            command += ["-c", f'model_reasoning_effort="{args.effort}"']
    elif args.harness == "jcode":
        command = [harness, "run", "--model", args.model, "--tool-profile", "none", "--no-update", "--quiet"]
        if args.provider:
            command += ["--provider", args.provider]
    elif args.harness == "pi":
        command = [harness, "--print", "--model", args.model, "--no-session", "--no-tools"]
        if args.provider:
            command += ["--provider", args.provider]
        if args.effort:
            command += ["--thinking", args.effort]
    elif args.harness == "cline":
        command = [harness, "--auto-approve", "true", "--json", "--model", args.model]
        if args.provider:
            command += ["--provider", args.provider]
        if args.effort:
            command += ["--thinking", args.effort]
    else:
        patch = output / "dsh.patch.yml"
        config = {"provider": "deepseek-official", "model": args.model}
        if args.effort:
            config["reasoningEffort"] = args.effort
        patch.write_text(json.dumps([{"id": "agent-default-model", "config": config}]))
        command = [harness, "--profile", "headless", "--patch", str(patch)]

    print(f"Generating with {args.harness} ({args.model}, effort={args.effort or 'default'})…", flush=True)
    scratch = tempfile.TemporaryDirectory(prefix="horse-cline-") if args.harness == "cline" else None
    with (output / "stdout.log").open("w", encoding="utf-8") as stdout_log, (output / "stderr.log").open("w", encoding="utf-8") as stderr_log:
        process = subprocess.run(
            command + [prompt], cwd=scratch.name if scratch else output,
            stdin=subprocess.DEVNULL, stdout=stdout_log, stderr=stderr_log,
        )
    if scratch:
        scratch.cleanup()
    if process.returncode:
        parser.exit(1, f"Harness failed; see {output / 'stderr.log'} and stdout.log.\n")

    response = (output / "response.txt").read_text(encoding="utf-8") if args.harness == "codex" else (output / "stdout.log").read_text(encoding="utf-8")
    if args.harness == "cline":
        texts = []
        final_text = None
        for line in response.splitlines():
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if event.get("type") == "run_result" and event.get("text"):
                final_text = event["text"]
            if event.get("type") == "agent_event" and event.get("event", {}).get("text"):
                texts.append(event["event"]["text"])
        response = final_text or "".join(texts)
    match = re.search(r"(?:<!doctype\s+html[^>]*>\s*)?<html\b[^>]*>.*?</html\s*>", response, re.IGNORECASE | re.DOTALL)
    if not match:
        parser.exit(1, f"Harness did not return an HTML document; see {output / 'stdout.log'}.\n")
    html = match.group()

    destination = args.output / "index.html"
    destination.write_text(html + "\n", encoding="utf-8")
    print(f"Saved {destination.resolve()}")


if __name__ == "__main__":
    main()
