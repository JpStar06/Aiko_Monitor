# AikoMonitor

Monitor independente do AikoBot.

## Arquitetura

AikoBot -> POST /heartbeat -> AikoMonitor -> Discord API

O AikoMonitor não depende do Gateway do Discord para monitorar o AikoBot.

## 1. Variáveis de ambiente

Configure:

- MONITOR_TOKEN
- DISCORD_BOT_TOKEN
- STATUS_CHANNEL_ID
- CHECK_INTERVAL
- OFFLINE_AFTER

Não coloque tokens no Git.

## 2. Discord

O bot usado em DISCORD_BOT_TOKEN precisa ter permissão para enviar mensagens no canal definido em STATUS_CHANNEL_ID.

## 3. Discloud

O projeto usa:

TYPE=site
MAIN=app/main.py
ID=aiko-monitor

A aplicação escuta em 0.0.0.0:8080.

A URL final será semelhante a:

https://aiko-monitor.discloud.app

O heartbeat fica em:

POST /heartbeat

## 4. Teste local

Instale:

pip install -r requirements.txt

Execute:

uvicorn app.main:app --host 0.0.0.0 --port 8080

Teste:

GET http://localhost:8080/health

Heartbeat:

POST http://localhost:8080/heartbeat

Header:

Authorization: Bearer SEU_MONITOR_TOKEN

## 5. Integração com o AikoBot

No AikoBot, envie um POST para:

https://aiko-monitor.discloud.app/heartbeat

com:

Authorization: Bearer SEU_MONITOR_TOKEN

O ideal é enviar a cada 30 segundos.

## Observação

A primeira versão usa SQLite para manter o último heartbeat e o histórico básico de eventos. Isso é suficiente para um monitor pequeno e evita depender do banco principal do AikoBot.
