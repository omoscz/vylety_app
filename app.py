import datetime

import streamlit as st
from google import genai
from google.genai import types
from google.genai import errors

import config

st.set_page_config(page_title="Výlety App", page_icon="🏞️", layout="centered")


MODELY = ["gemini-2.5-flash-lite", "gemini-2.5-flash"]


def generuj_z_ai(prompt):
    if "GEMINI_KEY" not in st.secrets:
        st.error("V Secrets chybí proměnná GEMINI_KEY!")
        return None

    klient = genai.Client(api_key=st.secrets["GEMINI_KEY"])
    nastaveni = types.GenerateContentConfig(
        tools=[types.Tool(google_search=types.GoogleSearch())]
    )
    for model in MODELY:
        try:
            return klient.models.generate_content(model=model, contents=prompt, config=nastaveni)
        except errors.APIError as e:
            if e.code == 403:
                st.error("⚠️ API klíč je neplatný. Zkontroluj nastavení Secrets.")
                return None
            else:
                st.warning(f"⚠️ Přepínám na záložní model... [{e.code}]")

    st.error("❌ Všechny modely selhaly. Zkus to prosím za chvíli.")
    return None


def ziskej_zdroje(response):
    zdroje = []
    try:
        for cand in response.candidates:
            gm = getattr(cand, "grounding_metadata", None)
            if gm and gm.grounding_chunks:
                for ch in gm.grounding_chunks:
                    if ch.web and ch.web.uri:
                        zdroje.append((ch.web.title or ch.web.uri, ch.web.uri))
    except Exception:
        pass
    # Odstraníme duplicity při zachování pořadí
    videno = set()
    unikatni = []
    for titul, url in zdroje:
        if url not in videno:
            videno.add(url)
            unikatni.append((titul, url))
    return unikatni


def zobraz_vysledek(vysledek):
    if not vysledek:
        return
    st.markdown(vysledek["text"])
    if vysledek["zdroje"]:
        with st.expander("🔗 Ověřené zdroje z vyhledávání"):
            for titul, url in vysledek["zdroje"]:
                st.markdown(f"- [{titul}]({url})")


def uloz_vysledek(klic, response):
    if response:
        st.session_state[klic] = {
            "text": response.text,
            "zdroje": ziskej_zdroje(response),
        }


def vyber_seznam(polozky):
    return ", ".join(polozky) if polozky else "libovolné"


def formatuj_datum(rozsah):
    if isinstance(rozsah, (tuple, list)):
        if len(rozsah) == 2:
            return f"od {rozsah[0].strftime('%d.%m.%Y')} do {rozsah[1].strftime('%d.%m.%Y')}"
        if len(rozsah) == 1:
            return rozsah[0].strftime("%d.%m.%Y")
        return "nezáleží"
    return rozsah.strftime("%d.%m.%Y")


# --- UI ---
st.title("🏞️ Tipy na výlety a akce")
st.write("Vyber parametry a nech si navrhnout výlety, akce nebo restaurace v okolí.")

tab_vylety, tab_akce, tab_popis, tab_jidlo = st.tabs(
    ["🏞️ Výlety", "🎉 Akce", "📝 Podle popisu", "🍽️ Kam na jídlo"]
)

# ==================== VÝLETY ====================
with tab_vylety:
    st.subheader("Co tě láká?")
    vybrane_co = []
    with st.expander("🏷️ Co chceš vidět (nepovinné)"):
        for co in config.VYLETY_CO:
            if st.checkbox(co, key=f"vylet_co_{co}"):
                vybrane_co.append(co)

    vzdalenost = st.selectbox("📍 Dojezd autem", config.VZDALENOSTI, key="vylet_vzdalenost")
    pro_koho = st.selectbox("👥 Pro koho", config.PRO_KOHO, key="vylet_prokoho")
    narocnost = st.selectbox("💪 Náročnost", config.NAROCNOST, key="vylet_narocnost")
    kde = st.selectbox("🌦️ Kde", config.KDE, key="vylet_kde")
    vstupne = st.selectbox("🎟️ Vstupné", config.VSTUPNE, key="vylet_vstupne")

    if st.button("🚀 Navrhnout výlety", type="primary", key="btn_vylety"):
        with st.spinner("Hledám tipy na výlety..."):
            prompt = config.PROMPT_VYLETY.format(
                domov=config.DOMOV,
                co=vyber_seznam(vybrane_co),
                vzdalenost=vzdalenost,
                pro_koho=pro_koho,
                narocnost=narocnost,
                kde=kde,
                vstupne=vstupne,
                format=config._FORMAT_VYLET,
            )
            uloz_vysledek("vylety_vysledek", generuj_z_ai(prompt))

    if "vylety_vysledek" in st.session_state:
        st.write("---")
        zobraz_vysledek(st.session_state["vylety_vysledek"])

# ==================== AKCE ====================
with tab_akce:
    st.subheader("Jaké akce hledáš?")
    vybrane_typy = []
    with st.expander("🏷️ Typ akce (nepovinné)"):
        for typ in config.AKCE_TYPY:
            if st.checkbox(typ, key=f"akce_typ_{typ}"):
                vybrane_typy.append(typ)

    dnes = datetime.date.today()
    rozsah = st.date_input(
        "📅 Termín (jeden den nebo rozsah)",
        value=(dnes, dnes + datetime.timedelta(days=7)),
        key="akce_datum",
    )

    vzdalenost_a = st.selectbox("📍 Dojezd autem", config.VZDALENOSTI, key="akce_vzdalenost")
    pro_koho_a = st.selectbox("👥 Pro koho", config.PRO_KOHO, key="akce_prokoho")
    kde_a = st.selectbox("🌦️ Kde", config.KDE, key="akce_kde")
    vstupne_a = st.selectbox("🎟️ Vstupné", config.VSTUPNE, key="akce_vstupne")

    if st.button("🚀 Najít akce", type="primary", key="btn_akce"):
        with st.spinner("Hledám aktuální akce..."):
            prompt = config.PROMPT_AKCE.format(
                domov=config.DOMOV,
                typ=vyber_seznam(vybrane_typy),
                datum=formatuj_datum(rozsah),
                vzdalenost=vzdalenost_a,
                pro_koho=pro_koho_a,
                kde=kde_a,
                vstupne=vstupne_a,
            )
            uloz_vysledek("akce_vysledek", generuj_z_ai(prompt))

    if "akce_vysledek" in st.session_state:
        st.write("---")
        zobraz_vysledek(st.session_state["akce_vysledek"])

# ==================== PODLE POPISU ====================
with tab_popis:
    st.subheader("Napiš, co hledáš")
    popis = st.text_area(
        "Popiš svůj ideální výlet nebo akci",
        placeholder="Např.: Chci klidný výlet k vodě do hodiny cesty, kde bude občerstvení a dá se tam i projít s kočárkem...",
        height=120,
        key="popis_text",
    )

    if st.button("🚀 Navrhnout tipy", type="primary", key="btn_popis"):
        if not popis.strip():
            st.warning("Napiš prosím, co hledáš!")
        else:
            with st.spinner("Hledám tipy podle popisu..."):
                prompt = config.PROMPT_POPIS.format(
                    domov=config.DOMOV,
                    popis=popis.strip(),
                    format=config._FORMAT_VYLET,
                )
                uloz_vysledek("popis_vysledek", generuj_z_ai(prompt))

    if "popis_vysledek" in st.session_state:
        st.write("---")
        zobraz_vysledek(st.session_state["popis_vysledek"])

# ==================== KAM NA JÍDLO ====================
with tab_jidlo:
    st.subheader("Kde budeš?")
    misto = st.text_input(
        "Místo nebo trasa",
        placeholder="Např.: Humpolec   nebo   ze Zruče nad Sázavou do Humpolce",
        key="jidlo_misto",
    )

    vzdalenost_j = st.selectbox("📍 Dojezd autem", config.JIDLO_VZDALENOSTI, key="jidlo_vzdalenost")
    vybrane_typy_j = []
    with st.expander("🍽️ Typ podniku (nepovinné)"):
        for typ in config.JIDLO_TYPY:
            if st.checkbox(typ, key=f"jidlo_typ_{typ}"):
                vybrane_typy_j.append(typ)
    cena = st.selectbox("💰 Cena", config.JIDLO_CENA, key="jidlo_cena")

    if st.button("🚀 Najít podniky", type="primary", key="btn_jidlo"):
        if not misto.strip():
            st.warning("Napiš prosím, kde budeš!")
        else:
            with st.spinner("Hledám podniky..."):
                prompt = config.PROMPT_JIDLO.format(
                    domov=config.DOMOV,
                    misto=misto.strip(),
                    vzdalenost=vzdalenost_j,
                    typ=vyber_seznam(vybrane_typy_j),
                    cena=cena,
                )
                uloz_vysledek("jidlo_vysledek", generuj_z_ai(prompt))

    if "jidlo_vysledek" in st.session_state:
        st.write("---")
        zobraz_vysledek(st.session_state["jidlo_vysledek"])
