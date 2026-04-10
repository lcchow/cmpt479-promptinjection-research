# OpenClaw Security Research

This repository contains the benchmark artifacts, orchestration code, configuration, and final result tables for a study of indirect prompt injection against OpenClaw-based agent workflows.

## Overview

The benchmark evaluates prompt-injection behavior across three realistic artifact-delivery vectors:

- `html_page`
- `local_docx`
- `agentmail_inbox`

The corpus spans five attack-technique families:

- Naive
- Context Ignoring
- Encoded
- Roleplaying
- Fake Completion

These are evaluated against three adversarial objective classes:

- Information Gathering
- Data Phishing
- Manipulate Content

The repository preserves the final benchmark inputs and the result tables used for analysis.

## Repository structure

- `artifacts/` — benchmark artifacts used in the experiment
  - `html/` — HTML artifacts for the `html_page` vector
  - `docs/` — DOCX artifacts for the `local_docx` vector
  - `pdfs/` — PDF artifacts retained as part of the benchmark corpus
  - `emails/` — email message artifacts/templates
  - `markdown/`, `docx_md/`, `docx_text/` — derived document forms retained from the benchmark workflow
  - `fake user info/` — shared synthetic target files used by some attack cases
- `setup_data/` — benchmark definitions and setup files
  - `Test-Cases.csv` — authoritative case list
  - `agentmail_inboxes.json` — inbox mapping used for the email workflow
- `results/` — final structured results and canonical manifests
- `scripts/` — helper scripts for document extraction, email retrieval, and local hosting
- `orchestrator.py` — main benchmark runner
- `benchmark_config.json` — primary benchmark configuration
- `prompts.xlsx` - summary of all prompt test cases designed

## Main files for reproduction

- `benchmark_config.json`
- `orchestrator.py`
- `setup_data/Test-Cases.csv`
- `results/canonical_manifest.csv`
- `results/canonical_manifest.json`
- `results/experiment_results_html.csv`
- `results/experiment_results_doc.csv`
- `results/experiment_results_email.csv`

## Models represented in the result tables

The repository currently preserves results for the model lanes that were retained during the experiment, including:

- `openai-codex/gpt-5.4`
- `openai/gpt-4o-mini`

## Benchmark configuration

The main configuration file is:

- `benchmark_config.json`

Important fields include:

- `default_model_id` — default model used by the orchestrator
- `active_vectors` — active benchmark source nodes
- `email_rules.exact_message_binding` — ensures the victim fetches the intended email message
- `email_rules.post_send_delay_seconds` — delay before inbox retrieval to reduce race conditions
- `email_rules.use_fresh_isolated_session_per_case` — enables per-case isolation
- `session_cleanup_policy.cleanup_completed_subagents_after_each_test` — cleanup rule after runs

## Reproducibility requirements

Reproducing the benchmark requires an OpenClaw environment with the following capabilities available at runtime:

1. OpenClaw built-in tool-calling and orchestration support
   - file access
   - controlled command execution
   - session/sub-agent isolation
   - web-access support
2. A working browser-backed webpage access path on the host
3. AgentMail access configured for the inbox benchmark
4. Python 3 for the orchestration and helper scripts

### Environment notes

In the original runtime, browser-backed execution was enabled through a host-installed Chrome binary configured for OpenClaw. Email execution was enabled through AgentMail with API-key-based authentication provided to the runtime environment. The benchmark also relied on fresh-session isolation and exact-message retrieval for the email vector.

## How to reproduce the benchmark

### 1. Review the benchmark configuration

Inspect and, if needed, update:

- `benchmark_config.json`

In particular, verify:

- the desired `default_model_id`
- the active vectors
- the email delay and exact-message settings

### 2. Verify artifact and case definitions

Use the authoritative case source and manifest files:

- `setup_data/Test-Cases.csv`
- `results/canonical_manifest.csv`
- `results/canonical_manifest.json`

These files define the benchmark cases and their associated artifacts.

### 3. Ensure required runtime dependencies are available

Before running the benchmark, confirm that:

- OpenClaw is installed and working
- the runtime can execute host-side commands needed by `orchestrator.py`
- browser-backed webpage access is functional
- AgentMail authentication is configured if running the email vector
- Python 3 is available

### 4. Run the orchestrator

The main entry point is:

```bash
python3 orchestrator.py
```

Common run modes include:

```bash
python3 orchestrator.py run-case <PROMPT_ID>
python3 orchestrator.py run-range <START_ID> <END_ID>
python3 orchestrator.py run-all
```

A model can be overridden at runtime with:

```bash
python3 orchestrator.py run-case <PROMPT_ID> --model-id <provider/model>
python3 orchestrator.py run-range <START_ID> <END_ID> --model-id <provider/model>
python3 orchestrator.py run-all --model-id <provider/model>
```

### 5. Review outputs

Structured outputs are written to:

- `results/experiment_results.csv`
- `results/experiment_results_html.csv`
- `results/experiment_results_doc.csv`
- `results/experiment_results_email.csv`

The canonical benchmark mapping is preserved in:

- `results/canonical_manifest.csv`
- `results/canonical_manifest.json`

## Notes on scope

- The final benchmark is centered on `html_page`, `local_docx`, and `agentmail_inbox`.
- PDF artifacts are retained in the corpus, but PDF is not the primary active execution vector for the final benchmark configuration described in this repository.
- The repository has been cleaned for submission and does not include transient runtime logs, archived reset directories, or per-run raw trace folders.

## Practical reproduction guidance

For the most faithful rerun:

1. keep the benchmark vectors aligned with `benchmark_config.json`
2. preserve fresh-session isolation between cases
3. preserve exact-message retrieval for email cases
4. preserve the configured post-send email delay
5. avoid mixing transient debug artifacts into the final result tables

## Citation / usage

If you reuse this repository for follow-on benchmarking, preserve the benchmark structure, case definitions, and vector semantics so that model comparisons remain meaningful.
