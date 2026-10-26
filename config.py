# config.py

DOMOV = "Dolní Pohleď (okres Kutná Hora, Středočeský kraj)"

VZDALENOSTI = [
    "Nezáleží",
    "do 30 minut",
    "do 1 hodiny",
    "do 1,5 hodiny",
    "do 2 hodin",
    "nad 2 hodiny",
]

PRO_KOHO = [
    "Nezáleží",
    "Rodina s dětmi",
    "Pár",
    "Parta",
    "Se psem",
]

NAROCNOST = [
    "Nezáleží",
    "Nenáročné (procházka)",
    "Střední",
    "Celodenní",
]

KDE = [
    "Nezáleží",
    "Venku",
    "Uvnitř",
]

VSTUPNE = [
    "Nezáleží",
    "Zdarma",
    "Placené",
]

VYLETY_CO = [
    "Příroda (lesy, rozhledny, vodopády)",
    "Hrady a zámky",
    "Památky (kostely, historická města)",
    "Muzea a galerie",
    "Zábavní parky",
    "ZOO / safari / farmy",
    "Jeskyně",
    "Koupání / aquaparky",
    "Naučné stezky",
    "Technické památky",
    "Cyklovýlety",
    "Turistika / hory",
]

AKCE_TYPY = [
    "Pro děti",
    "Koncert / festival",
    "Divadlo",
    "Trhy / jarmark",
    "Výstava",
    "Sport",
    "Gastro akce",
    "Slavnosti / poutě",
    "Workshop / dílny",
]

JIDLO_TYPY = [
    "Česká",
    "Pizzerie / italská",
    "Asijská",
    "Kavárna / cukrárna",
    "Hospoda / pivnice",
    "Fast food",
]

JIDLO_CENA = [
    "Nezáleží",
    "Levné",
    "Střední",
    "Dražší",
]

# Společný formát výstupu (Markdown) používaný ve všech promptech
_FORMAT_VYLET = """Každý tip napiš přesně v tomto formátu (Markdown), oddělený prázdným řádkem:

### Název místa
📍 přibližný dojezd autem · 🏷️ typ · 👥 pro koho · 🎟️ vstupné
Popis ve 2–3 větách — co to je a proč tam vyrazit.
🔗 [Odkaz](https://...)

Vždy uveď reálný, funkční odkaz na oficiální web nebo důvěryhodný zdroj."""

PROMPT_VYLETY = """Jsi zkušený průvodce po výletech v České republice. Uživatel bydlí v obci {domov} a vzdálenosti počítej autem odtud.

Navrhni až 10 tipů na výlet podle těchto parametrů (pokud je u parametru "nezáleží" nebo "libovolné", tím se neomezuj):
- Co chce vidět: {co}
- Maximální dojezd autem: {vzdalenost}
- Pro koho: {pro_koho}
- Náročnost: {narocnost}
- Kde: {kde}
- Vstupné: {vstupne}

Použij Google vyhledávání a navrhuj jen místa, která reálně existují.

{format}"""

PROMPT_AKCE = """Jsi průvodce po kulturních a společenských akcích v České republice. Uživatel bydlí v obci {domov} a vzdálenosti počítej autem odtud.

Pomocí Google vyhledávání najdi aktuální, reálně konající se akce (čerpej např. z Kudy z nudy a dalších zdrojů) podle těchto parametrů (pokud je u parametru "nezáleží", tím se neomezuj):
- Typ akce: {typ}
- Termín: {datum}
- Maximální dojezd autem: {vzdalenost}
- Pro koho: {pro_koho}
- Kde: {kde}
- Vstupné: {vstupne}

Uváděj POUZE reálné a ověřené akce konající se v daném termínu. Raději navrhni méně tipů než vymyslet neexistující akci. Pokud nic nenajdeš, napiš to.

Každou akci napiš přesně v tomto formátu (Markdown), oddělenou prázdným řádkem:

### Název akce
📅 datum · 🏷️ typ · 📍 přibližný dojezd autem · 🎟️ vstupné
Popis ve 2–3 větách — o co jde.
🔗 [Odkaz](https://...)

Vždy uveď reálný, funkční odkaz na stránku akce."""

PROMPT_POPIS = """Jsi zkušený průvodce po výletech a akcích v České republice. Uživatel bydlí v obci {domov} a vzdálenosti počítej autem odtud.

Navrhni až 10 tipů podle tohoto popisu od uživatele:
"{popis}"

Použij Google vyhledávání a navrhuj jen místa a akce, které reálně existují.

{format}"""

PROMPT_JIDLO = """Jsi znalec restaurací a podniků v České republice. Uživatel bydlí v obci {domov}.

Uživatel zadal místo nebo trasu: "{misto}"
Pomocí Google vyhledávání najdi reálné podniky v daném místě nebo po trase podle těchto parametrů (pokud je u parametru "nezáleží", tím se neomezuj):
- Maximální dojezd autem: {vzdalenost}
- Typ podniku: {typ}
- Cenová hladina: {cena}

Navrhuj jen podniky, které reálně existují.

Každý podnik napiš přesně v tomto formátu (Markdown), oddělený prázdným řádkem:

### Název podniku
🍽️ typ kuchyně · 📍 místo / dojezd · 💰 cena
Popis ve 2–3 větách — čím je podnik dobrý.
🔗 [Odkaz](https://...)

Vždy uveď reálný, funkční odkaz (web podniku, menu nebo mapy)."""
