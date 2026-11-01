from __future__ import annotations

import hashlib, json, os, re, threading, time
from dataclasses import dataclass, field, replace

import requests

from .auth import access_token, clear_access_token
from .file_archive import exists as cache_exists, open_file as cache_open


def _messages(prompt) -> list:
    return prompt if isinstance(prompt, list) else [{"role": "user", "content": prompt}]


@dataclass
class Usage:
    calls: int = 0
    cached: int = 0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    thinking_tokens: int = 0
    seconds: float = 0.0
    failures: int = 0

    def as_dict(self):
        return dict(self.__dict__)


@dataclass
class LLM:
    base_url: str
    model: str
    cache_dir: str
    seed: int = 42
    timeout: int = 600
    usage: Usage = field(default_factory=Usage)

    def _path(self, key: str) -> str:
        return os.path.join(self.cache_dir, key[:2], key + ".json")

    variant = ""

    def complete(self, prompt, max_tokens: int = 4096, schema: dict | None = None) -> str:
        base = [self.model, prompt, max_tokens, self.seed] + ([schema] if schema else [])
        paths = [self._path(hashlib.sha256(json.dumps(base).encode()).hexdigest())]
        if self.variant:
            paths.append(self._path(hashlib.sha256(json.dumps(base + [self.variant]).encode()).hexdigest()))
        for p in paths:
            if cache_exists(p):
                entry = json.load(cache_open(p))
                if entry.get("variant", self.variant) == self.variant:
                    self.usage.cached += 1
                    return entry["text"]
        path = paths[0] if not cache_exists(paths[0]) else paths[-1]
        t0 = time.time()
        text, u = self._call(prompt, max_tokens, schema)
        self.usage.calls += 1
        if u.get("failed"):
            self.usage.failures += 1
            return text
        self.usage.prompt_tokens += u.get("prompt_tokens", 0)
        self.usage.completion_tokens += u.get("completion_tokens", 0)
        self.usage.thinking_tokens += u.get("thinking_tokens", 0)
        self.usage.seconds += time.time() - t0
        os.makedirs(os.path.dirname(path), exist_ok=True)
        tmp = f"{path}.{os.getpid()}.{threading.get_ident()}.tmp"
        with open(tmp, "w") as f:
            json.dump({"model": self.model, "variant": self.variant, "prompt": prompt, "text": text, "usage": u}, f)
        os.replace(tmp, path)
        return text

    def _call(self, prompt, max_tokens: int, schema: dict | None = None):
        body = {"model": self.model, "temperature": 0, "seed": self.seed, "max_tokens": max_tokens,
                "messages": _messages(prompt)}
        if schema:
            body["response_format"] = {"type": "json_schema", "json_schema": {"name": "reply", "strict": True, "schema": schema}}
        r = requests.post(f"{self.base_url}/chat/completions", timeout=self.timeout, json=body)
        r.raise_for_status()
        body = r.json()
        return body["choices"][0]["message"]["content"] or "", body.get("usage", {})

    def json(self, prompt: str, max_tokens: int = 4096) -> dict:
        retry = min(max_tokens * 2, 65536)
        attempts = [(self, max_tokens), (self, retry)]
        attempts += [(replace(self, seed=self.seed + i, usage=self.usage), retry) for i in (1, 2)]
        for llm, budget in attempts:
            text = llm.complete(prompt, budget)
            m = re.search(r"\{.*\}", text, re.S)
            if m:
                try:
                    return json.loads(m.group(0))
                except json.JSONDecodeError:
                    pass
        self.usage.failures += 1
        return {"error": "unparseable reply", "reply": text[:2000]}


@dataclass
class GeminiLLM(LLM):
    thinking_level: str = "HIGH"

    @property
    def variant(self) -> str:
        return f"thinking={self.thinking_level}" if self.thinking_level else ""

    def _post(self, prompt, budget: int, schema: dict | None = None) -> dict:
        project = os.environ["GOOGLE_CLOUD_PROJECT"]
        location = os.environ.get("GOOGLE_CLOUD_LOCATION", "global")
        url = (f"https://aiplatform.googleapis.com/v1/projects/{project}/locations/{location}"
               f"/publishers/google/models/{self.model}:generateContent")
        config = {"maxOutputTokens": budget, "seed": self.seed, "responseMimeType": "application/json"}
        if schema:
            config["responseJsonSchema"] = schema
        if self.thinking_level:
            config["thinkingConfig"] = {"thinkingLevel": self.thinking_level}
        messages = _messages(prompt)
        body = {"contents": [{"role": "model" if m["role"] == "assistant" else "user", "parts": [{"text": m["content"]}]}
                             for m in messages if m["role"] != "system"], "generationConfig": config}
        system = [{"text": m["content"]} for m in messages if m["role"] == "system"]
        if system:
            body["systemInstruction"] = {"parts": system}
        for attempt in range(5):
            r = requests.post(url, json=body, timeout=(30, self.timeout), headers={
                "Authorization": f"Bearer {access_token()}", "x-goog-user-project": project})
            if r.status_code == 401:
                clear_access_token()
            elif r.status_code in (429, 500, 502, 503, 504):
                time.sleep(min(2 ** attempt * 5, 120))
            else:
                break
        if not r.ok:
            raise RuntimeError(f"Gemini HTTP {r.status_code}: {r.text[:300]}")
        return r.json()

    def _call(self, prompt, max_tokens: int, schema: dict | None = None):
        error = ""
        for budget in (max(30000, max_tokens), 65536):
            try:
                data = self._post(prompt, budget, schema)
            except (RuntimeError, requests.RequestException) as e:
                error = str(e)
                break
            cand = data["candidates"][0]
            meta = data.get("usageMetadata", {})
            usage = {"prompt_tokens": meta.get("promptTokenCount", 0), "completion_tokens": meta.get("candidatesTokenCount", 0),
                     "thinking_tokens": meta.get("thoughtsTokenCount", 0)}
            if cand.get("finishReason") == "STOP":
                text = "".join(p.get("text", "") for p in cand.get("content", {}).get("parts", []) if not p.get("thought"))
                return text, usage
            error = f"finishReason={cand.get('finishReason')}"
            self.usage.thinking_tokens += usage["thinking_tokens"]
            self.usage.completion_tokens += usage["completion_tokens"]
            self.usage.prompt_tokens += usage["prompt_tokens"]
            if cand.get("finishReason") != "MAX_TOKENS":
                break
        return "", {"failed": True, "error": error[:300]}


def make_llm(model: str, cache_dir: str, seed: int = 42) -> LLM:
    if os.environ.get("LLM_BACKEND") == "gemini":
        return GeminiLLM("", model, cache_dir, seed=seed, thinking_level=os.environ.get("GEMINI_THINKING_LEVEL", "HIGH"))
    return LLM(os.environ["VLLM_BASE_URL"], model, cache_dir, seed=seed)
