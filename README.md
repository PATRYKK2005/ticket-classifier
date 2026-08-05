# Ticket Classifier

Prosta Azure Function w Pythonie do automatycznej klasyfikacji ticketów IT. Na podstawie słów kluczowych w treści ticketu przypisuje go do odpowiedniej kategorii i zwraca gotowy runbook z krokami działania.

## Wymagania

- Python 3.10+
- Azure Functions Core Tools v4
- pip

## Jak uruchomić lokalnie

1. Sklonuj repozytorium:
```bash
git clone https://github.com/PATRYKK2005/ticket-classifier
cd ticket-classifier
```

2. Stwórz plik konfiguracyjny na podstawie przykładu:
```bash
cp local.settings.json.example local.settings.json
```

3. Zainstaluj zależności:
```bash
pip install -r requirements.txt
```

4. Uruchom funkcję:
```bash
func start
```

Funkcja będzie dostępna pod `http://localhost:7071/api/classify`.

## Przykładowe zapytania

Problem z siecią:
```bash
curl -X POST http://localhost:7071/api/classify \
  -H "Content-Type: application/json" \
  -d '{"ticket": "serwer nie odpowiada na pingi, problem z siecią"}'
```

Problem z połączeniem:
```bash
curl -X POST http://localhost:7071/api/classify \
  -H "Content-Type: application/json" \
  -d '{"ticket": "nie mogę się połączyć przez SSH, connection refused"}'
```

Problem z aplikacją:
```bash
curl -X POST http://localhost:7071/api/classify \
  -H "Content-Type: application/json" \
  -d '{"ticket": "aplikacja zwraca error 500, problem z API"}'
```

Niesklasyfikowany ticket:
```bash
curl -X POST http://localhost:7071/api/classify \
  -H "Content-Type: application/json" \
  -d '{"ticket": "coś nie działa"}'
```

## Przykładowa odpowiedź

```json
{
  "ticket": "serwer nie odpowiada na pingi, problem z siecią",
  "category": "network",
  "priority": "high",
  "runbook": "1. Sprawdź połączenie sieciowe\n2. Zweryfikuj konfigurację DNS\n3. Sprawdź reguły firewalla\n4. Przetestuj routing przez traceroute",
  "message": "Ticket zakwalifikowany jako: NETWORK"
}
```

## Kategorie ticketów

| Kategoria | Priorytet | Opis                                             |
|-----------|-----------|--------------------------------------------------|
| `network` | high | Problemy z siecią, DNS, firewallem, routingiem   |
| `server` | high | Problemy z zasobami serwera, procesami, serwisami |
| `connectivity` | medium | Problemy z połączeniem SSH, VPN, portami         |
| `application` | medium | Błędy aplikacji, API, deploymenty                |
| `other` | medium | Niesklasyfikowane     |
