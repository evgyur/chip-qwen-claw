#!/usr/bin/env python3
"""Fix Groq provider: Groq API expects model id 'qwen/qwen3-32b', not 'qwen3-32b'."""
import json
import os
import sys

path = os.path.expanduser("~/.openclaw/openclaw.json")
if len(sys.argv) > 1:
    path = sys.argv[1]

with open(path) as f:
    c = json.load(f)

providers = c.setdefault("models", {}).setdefault("providers", {})
groq = providers.get("groq")
if not groq:
    print("No groq provider found")
    sys.exit(1)

models_list = groq.get("models", [])
updated = False
new_models = []
for m in models_list:
    if not isinstance(m, dict):
        continue
    if m.get("id") == "qwen3-32b":
        # Replace with Groq's actual API model id
        m = dict(m)
        m["id"] = "qwen/qwen3-32b"
        m["name"] = m.get("name") or "Qwen 3 32B (Groq)"
        updated = True
    elif m.get("id") != "qwen/qwen3-32b":
        new_models.append(m)

if updated:
    new_models.append({
        "id": "qwen/qwen3-32b",
        "name": "Qwen 3 32B (Groq)",
        "reasoning": True,
        "input": ["text"],
        "contextWindow": 131072,
        "maxTokens": 40960,
    })
    groq["models"] = new_models
else:
    # No qwen3-32b found; add qwen/qwen3-32b if missing
    ids = [x.get("id") for x in models_list if isinstance(x, dict)]
    if "qwen/qwen3-32b" not in ids:
        models_list.append({
            "id": "qwen/qwen3-32b",
            "name": "Qwen 3 32B (Groq)",
            "reasoning": True,
            "input": ["text"],
            "contextWindow": 131072,
            "maxTokens": 40960,
        })
        groq["models"] = models_list
        updated = True

# Update agents.defaults.model.primary and agents.defaults.models to use groq/qwen/qwen3-32b (so API gets qwen/qwen3-32b)
defaults = c.setdefault("agents", {}).setdefault("defaults", {})
model_cfg = defaults.get("model")
if isinstance(model_cfg, dict) and model_cfg.get("primary") == "groq/qwen3-32b":
    defaults["model"]["primary"] = "groq/qwen/qwen3-32b"
    print("Updated primary to groq/qwen/qwen3-32b")
models_allow = defaults.get("models", {})
if "groq/qwen3-32b" in models_allow:
    alias = models_allow.pop("groq/qwen3-32b")
    models_allow["groq/qwen/qwen3-32b"] = alias
    defaults["models"] = models_allow
    print("Updated models alias to groq/qwen/qwen3-32b")

with open(path, "w") as f:
    json.dump(c, f, indent=2, ensure_ascii=False)
print("Written", path)
