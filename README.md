# AikoMonitor

Monitor independente do AikoBot.

## Estrutura

```text
AikoMonitor/
├── main.py                 # entrypoint da Discloud
├── app/
│   ├── __init__.py
│   ├── main.py             # FastAPI
│   ├── database.py
│   └── discord_status.py
├── requirements.txt
├── discloud.config
└── .env.example
```

## Discloud

O `discloud.config` usa `TYPE=site` e `MAIN=main.py`.
O `main.py` inicia Uvicorn em `0.0.0.0:8080` e carrega `app.main:app`.

## Variáveis

Configure no ambiente da Discloud:

- `MONITOR_TOKEN`: segredo compartilhado apenas entre AikoBot e AikoMonitor.
- `DISCORD_BOT_TOKEN`: token do bot Discord que enviará as mensagens.
- `STATUS_CHANNEL_ID`: ID do canal de status.
- `CHECK_INTERVAL`: padrão 30 segundos.
- `OFFLINE_AFTER`: padrão 90 segundos sem heartbeat.
- `DB_PATH`: padrão `data/monitor.db`.

Não coloque tokens no Git.

## Endpoints

- `GET /` — status básico do serviço.
- `GET /health` — health check.
- `POST /heartbeat` — heartbeat autenticado do AikoBot.

O AikoBot deve enviar:

```http
POST /heartbeat
Authorization: Bearer SEU_MONITOR_TOKEN
```

## Integração com o AikoBot

O arquivo `aikobot_integration.py` contém a função de heartbeat. No AikoBot, defina:

```env
MONITOR_URL=https://SEU-ID.discloud.app/heartbeat
MONITOR_TOKEN=mesmo-segredo-do-AikoMonitor
```

E inicie `heartbeat()` como uma `asyncio.Task` durante o startup do bot.
