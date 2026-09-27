from datetime import datetime, timezone


def offline_embed(seconds_without_heartbeat: float) -> dict:
    minutes = seconds_without_heartbeat / 60

    return {
        "title": "🔴 AikoBot Offline",
        "description": (
            "O monitor detectou que o AikoBot parou "
            "de enviar heartbeats."
        ),
        "color": 0xFF0000,
        "fields": [
            {
                "name": "⏱️ Tempo sem heartbeat",
                "value": f"**{minutes:.1f} minutos**",
                "inline": True,
            },
            {
                "name": "📡 Status",
                "value": "🔴 Offline",
                "inline": True,
            },
        ],
        "footer": {
            "text": "AikoMonitor"
        },
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def online_embed() -> dict:
    return {
        "title": "🟢 AikoBot Online",
        "description": (
            "O AikoBot voltou a enviar heartbeats normalmente."
        ),
        "color": 0x00FF00,
        "fields": [
            {
                "name": "📡 Status",
                "value": "🟢 Online",
                "inline": True,
            },
        ],
        "footer": {
            "text": "AikoMonitor"
        },
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }