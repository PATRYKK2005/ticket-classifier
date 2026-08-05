import azure.functions as func
import datetime
import json
import logging

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

CATEGORIES = {
    "network": {
        "keywords": ["sieć", "network", "dns", "firewall", "routing", "vlan", "ping", "packet", "bandwidth", "latency"],
        "runbook": "1. Sprawdź połączenie sieciowe\n2. Zweryfikuj konfigurację DNS\n3. Sprawdź reguły firewalla\n4. Przetestuj routing przez traceroute"
    },
    "server": {
        "keywords": ["serwer", "server", "cpu", "ram", "memory", "disk", "dysk", "crash", "reboot", "restart", "service", "proces"],
        "runbook": "1. Sprawdź zasoby serwera (CPU/RAM/dysk)\n2. Przejrzyj logi systemowe\n3. Sprawdź status serwisów\n4. Zrestartuj problematyczny serwis"
    },
    "connectivity": {
        "keywords": ["połączenie", "connection", "timeout", "refused", "unreachable", "vpn", "ssh", "port", "socket"],
        "runbook": "1. Sprawdź czy port jest otwarty\n2. Zweryfikuj konfigurację VPN\n3. Sprawdź firewall po obu stronach\n4. Przetestuj połączenie przez telnet/nc"
    },
    "application": {
        "keywords": ["aplikacja", "app", "błąd", "error", "exception", "crash", "deploy", "api", "endpoint", "response"],
        "runbook": "1. Sprawdź logi aplikacji\n2. Zweryfikuj ostatnie deploymenty\n3. Sprawdź dostępność zależności (baza, cache)\n4. Przetestuj endpoint przez curl"
    }
}

def classify_ticket(text: str) -> tuple[str, str]:
    text_lower = text.lower()
    scores = {}

    for category, data in CATEGORIES.items():
        score = sum(1 for keyword in data["keywords"] if keyword in text_lower)
        scores[category] = score

    best_category = max(scores, key=scores.get)

    if scores[best_category] == 0:
        return "other", "1. Zbierz więcej informacji o problemie\n2. Sprawdź logi systemowe\n3. Skontaktuj się z zespołem L2"

    return best_category, CATEGORIES[best_category]["runbook"]


@app.route(route="classify", methods=["POST"])
def classify_ticket_http(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Otrzymano ticket do klasyfikacji")

    try:
        body = req.get_json()
    except ValueError:
        return func.HttpResponse(
            json.dumps({"error": "Nieprawidłowy format JSON"}),
            status_code=400,
            mimetype="application/json"
        )

    ticket_text = body.get("ticket", "")

    if not ticket_text:
        return func.HttpResponse(
            json.dumps({"error": "Pole 'ticket' jest wymagane"}),
            status_code=400,
            mimetype="application/json"
        )

    category, runbook = classify_ticket(ticket_text)

    response = {
        "ticket": ticket_text,
        "category": category,
        "priority": "high" if category in ["server", "network"] else "medium",
        "runbook": runbook,
        "message": f"Ticket zakwalifikowany jako: {category.upper()}"
    }

    return func.HttpResponse(
        json.dumps(response, ensure_ascii=False),
        status_code=200,
        mimetype="application/json"
    )
