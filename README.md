# chip-qwen-claw

Подключение модели **Qwen 3 32B (Groq)** к [OpenClaw](https://docs.openclaw.ai) с алиасом **`/qwen`**, чтобы на любой машине можно было быстро сделать Qwen разрешённой моделью. Секреты (API-ключи) в репозиторий не входят.

## Зачем

- Одна и та же инструкция для установки модели на разных машинах.
- Модель доступна по команде `/qwen` и по имени `qwen` в выборе модели.
- Документация Groq: [Qwen 3 32B](https://console.groq.com/docs/model/qwen/qwen3-32b), [OpenAI-совместимый API](https://console.groq.com/docs/openai).

## Предусловия

- Установлен OpenClaw, gateway запускается (сервис `openclaw-gateway` или `openclaw gateway`).
- Конфиг: `~/.openclaw/openclaw.json`.
- API-ключ Groq: [console.groq.com → API Keys](https://console.groq.com/keys). **В репозиторий и в конфиг не вставлять.**

## Шаги

### 1. Добавить модель и алиас в конфиг

В `~/.openclaw/openclaw.json` в секции `agents.defaults.models` добавить (или дописать к существующим):

```json
"groq/qwen/qwen3-32b": { "alias": "qwen" }
```

**Важно:** Groq API ожидает id модели `qwen/qwen3-32b`, поэтому в OpenClaw ссылка должна быть именно `groq/qwen/qwen3-32b` (не `groq/qwen3-32b`), иначе будет 404.

Пример полной структуры:

```json
{
  "agents": {
    "defaults": {
      "models": {
        "groq/qwen/qwen3-32b": { "alias": "qwen" }
      }
    }
  }
}
```

Так в чате будут работать **`/qwen`** и выбор модели по имени «qwen».

### 2. Задать API-ключ Groq

Ключ задаётся **только через окружение**, не в конфиге и не в репозитории.

- Если gateway подхватывает `.env` (например unit открывает `~/clawd/.env`), добавить в этот файл:
  ```bash
  GROQ_API_KEY=ваш_ключ_из_console_groq_com
  ```
- Или в unit systemd: `Environment=GROQ_API_KEY=...` (лучше не коммитить unit с ключом в общий репозиторий).

### 3. Перезапустить gateway

```bash
systemctl --user restart openclaw-gateway
```

Из Windows (WSL):

```powershell
wsl -e bash -c "systemctl --user restart openclaw-gateway"
```

### 4. Проверить

- В чате с ботом: **`/model list`** — в списке должна быть модель с алиасом **qwen**.
- Переключиться: **`/qwen`** или **`/model qwen`**.
- Отправить сообщение и убедиться, что ответ идёт от выбранной модели.

## (Опционально) Qwen по умолчанию

Чтобы по умолчанию использовался Qwen:

```json
"agents": {
  "defaults": {
    "model": { "primary": "groq/qwen/qwen3-32b" }
  }
}
```

## Если провайдера Groq нет в списке

Если встроенного провайдера `groq` нет, в `~/.openclaw/openclaw.json` в `models.providers` можно добавить кастомный провайдер (ключ по-прежнему только в env):

```json
"models": {
  "mode": "merge",
  "providers": {
    "groq": {
      "baseUrl": "https://api.groq.com/openai/v1",
      "apiKey": "${GROQ_API_KEY}",
      "api": "openai-completions",
      "models": [
        {
          "id": "qwen3-32b",
          "name": "Qwen 3 32B (Groq)",
          "reasoning": true,
          "input": ["text"],
          "contextWindow": 131072,
          "maxTokens": 40960
        }
      ]
    }
  }
}
```

И в `agents.defaults.models`: `"groq/qwen/qwen3-32b": { "alias": "qwen" }`.

## Для Cursor / агентов

В этом репозитории есть **SKILL.md** — скилл для агента с теми же шагами и без секретов. Можно подключить как skill или использовать README как пошаговую инструкцию.

## Ссылки

- [OpenClaw — Model providers](https://docs.openclaw.ai/concepts/model-providers)
- [OpenClaw — Slash commands](https://docs.openclaw.ai/tools/slash-commands) (`/model`, алиасы)
- [Groq — Qwen 3 32B](https://console.groq.com/docs/model/qwen/qwen3-32b)
- [Groq — OpenAI API](https://console.groq.com/docs/openai)
