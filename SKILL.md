---
name: openclaw-qwen-groq
description: Add Groq Qwen 3 32B as an allowed model in OpenClaw with alias /qwen. Use when installing or enabling the Qwen model on another machine, or when the user asks to add /qwen or Groq Qwen to OpenClaw. No secrets in this skill; user supplies GROQ_API_KEY.
---

# OpenClaw: добавить модель Qwen (Groq) и алиас /qwen

## Когда использовать

- Пользователь просит подключить Qwen, Groq Qwen 3 32B или команду `/qwen` в OpenClaw.
- Нужно на другой машине сделать Qwen разрешённой моделью.
- Инвокация: «добавь qwen в openclaw», «установи /qwen», «подключи Groq Qwen к боту».

## Предусловия

- OpenClaw установлен (gateway запускается как `openclaw gateway` или сервис `openclaw-gateway`).
- Конфиг: `~/.openclaw/openclaw.json` (или `$OPENCLAW_STATE_DIR/openclaw.json`).
- Переменные окружения для gateway задаются в `EnvironmentFile` сервиса (например `~/clawd/.env`) или в `[Service] Environment=`.
- У пользователя есть API-ключ Groq (получить: [console.groq.com](https://console.groq.com) → API Keys). **В скилле ключ не хранить и не вставлять.**

## Шаги (без секретов)

### 1. Убедиться, что провайдер Groq доступен

OpenClaw по умолчанию поддерживает провайдер `groq` (встроенный каталог). Модель в API Groq: **`qwen/qwen3-32b`** (в OpenClaw часто отображается как `groq/qwen3-32b` — см. шаг 2). Документация Groq: [Qwen 3 32B](https://console.groq.com/docs/model/qwen/qwen3-32b), [OpenAI-совместимый API](https://console.groq.com/docs/openai) (base URL: `https://api.groq.com/openai/v1`). Если провайдера нет, его добавляют через `models.providers` (см. раздел «Кастомный провайдер» ниже).

### 2. Добавить модель и алиас в конфиг

В `~/.openclaw/openclaw.json`:

- В **`agents.defaults.models`** добавить запись для модели Groq Qwen с алиасом `qwen`, чтобы в чате работала команда **`/qwen`** (и выбор модели по имени «qwen»):

```json
{
  "agents": {
    "defaults": {
      "models": {
        "groq/qwen3-32b": { "alias": "qwen" }
      }
    }
  }
}
```

Если секция `agents.defaults.models` уже есть — добавить только ключ `"groq/qwen3-32b"` с `"alias": "qwen"`, не затирая остальные модели.

- Проверить, что в конфиге нет опечаток: идентификатор модели у Groq — `qwen/qwen3-32b`; в OpenClaw провайдер часто называется `groq`, то есть ссылка на модель: **`groq/qwen3-32b`**. Если в твоей версии OpenClaw в списке моделей отображается иначе (например `groq/qwen/qwen3-32b`), использовать тот идентификатор, который возвращает `openclaw models list`.

### 3. Задать API-ключ Groq (только у пользователя)

Ключ **не** должен лежать в репозитории или в скилле. Варианты:

- **Рекомендуется:** в файле, откуда подхватывается окружение для gateway (например `~/clawd/.env` или `EnvironmentFile` в unit openclaw-gateway), добавить строку:
  - `GROQ_API_KEY=<ключ_пользователя>`
- Или экспорт в оболочке перед запуском: `export GROQ_API_KEY=...`
- Ключ взять в [Groq Console → API Keys](https://console.groq.com/keys).

После добавления ключа gateway нужно перезапустить (шаг 5).

### 4. (Опционально) Сделать Qwen моделью по умолчанию

Если нужно, чтобы по умолчанию использовался Qwen, в `openclaw.json` задать:

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "groq/qwen3-32b"
      }
    }
  }
}
```

Иначе оставить текущий `primary` и переключаться на Qwen через `/qwen` или `/model qwen`.

### 5. Перезапуск gateway

- **Сервис (systemd):**  
  `systemctl --user restart openclaw-gateway`  
  (при необходимости: `wsl -e bash -c "systemctl --user restart openclaw-gateway"`).
- **Ручной запуск:** перезапустить процесс `openclaw gateway --port ...`.

После перезапуска в логах должно быть что-то вроде `[gateway] agent model: groq/qwen3-32b` (если default — Qwen) или модель по умолчанию; при этом в списке моделей должен быть `qwen`.

### 6. Проверка

- В чате с ботом: отправить **`/model list`** и убедиться, что в списке есть модель с алиасом **qwen** (или `groq/qwen3-32b`).
- Переключиться на Qwen: **`/qwen`** или **`/model qwen`** (если в твоей версии OpenClaw алиас из `agents.defaults.models` регистрируется как slash-команда).
- Отправить тестовое сообщение и убедиться, что ответ идёт от выбранной модели.

## Кастомный провайдер (если встроенного Groq нет)

Если в `openclaw models list` нет `groq` или нужен явный кастомный провайдер:

1. В `~/.openclaw/openclaw.json` в `models.providers` добавить:

```json
{
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
}
```

2. Идентификатор модели тогда будет **`groq/qwen3-32b`** (провайдер + id). В `agents.defaults.models` по-прежнему задать `"groq/qwen3-32b": { "alias": "qwen" }`.
3. Ключ по-прежнему задавать только через окружение: `GROQ_API_KEY` (в `.env` или `Environment`), в конфиге использовать подстановку `${GROQ_API_KEY}` или не указывать `apiKey` в провайдере, если OpenClaw подхватывает ключ из env по имени провайдера.

## Ссылки

- OpenClaw: [Model providers](https://docs.openclaw.ai/concepts/model-providers), [Slash commands](https://docs.openclaw.ai/tools/slash-commands) (`/model`, алиасы из `agents.defaults.models`).
- Groq: [Qwen 3 32B](https://console.groq.com/docs/model/qwen/qwen3-32b), [OpenAI API](https://console.groq.com/docs/openai).

## Краткий чеклист (на другой машине)

1. Получить API-ключ Groq в [console.groq.com](https://console.groq.com/keys).
2. Добавить в конфиг OpenClaw в `agents.defaults.models`: `"groq/qwen3-32b": { "alias": "qwen" }`.
3. Задать `GROQ_API_KEY` в окружении gateway (например в `.env`), без коммита ключа в репозиторий.
4. Перезапустить gateway.
5. Проверить: `/model list`, затем `/qwen` или `/model qwen`.
