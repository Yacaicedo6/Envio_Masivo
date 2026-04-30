# -*- coding: utf-8 -*-

import csv
import time
import urllib.parse
import webbrowser
from pathlib import Path

# ===== EMOJIS SEGUROS (NO SE ROMPEN POR CODIFICACIÓN) =====
CAL = "\U0001F4C5"    # 📅
CLOCK = "\U0001F560"  # 🕠
PIN = "\U0001F4CD"    # 📍

# ===== MENSAJE =====
MENSAJE = f"""Buen día, mucho gusto. Mi nombre es Yan Caicedo, de la Secretaría de Cultura.

Me permito escribirle para confirmar el taller del día de hoy, que hace parte de la Ruta de Gestión Cultural Comunitaria:

Taller 2
: Gestión de Públicos Comunitarios.
Objetivo: Diseñar acciones para fortalecer el compromiso comunitario con las creaciones artísticas y los eventos culturales de su entorno social.

{CAL} Jueves 19 de febrero
{CLOCK} Hora: 5:30 p. m. a 8:00 p. m.
{PIN} Lugar: Teatro La Unión, Comuna 16
Cra. 41H #38–80, Unión de Vivienda Popular

Quedamos atentos a su asistencia. Cualquier inquietud, no dude en comunicarse.
¡Muchas gracias!

Además, lo invitamos a unirse al Grupo de WhatsApp de la Ruta, donde compartiremos información relevante y estaremos en contacto directo:
https://chat.whatsapp.com/E42UT5WLHx6JXGGxowT7OP?mode=gi_t"""

# ===== CONFIGURACIÓN =====
TAM_TANDA = 15          # 15 pestañas por tanda
PAUSA_SEGUNDOS = 240    # 4 min entre tandas
ABRIR_AUTOMATICO = True # False si solo quieres el HTML


def solo_digitos(s: str) -> str:
    return "".join(ch for ch in str(s) if ch.isdigit())


def normalizar_numero(raw: str):
    d = solo_digitos(raw)

    # Si es móvil Colombia en 10 dígitos (3xxxxxxxxx)
    if len(d) == 10 and d.startswith("3"):
        return d

    # Si viene como 57 + 10 dígitos
    if len(d) == 12 and d.startswith("57") and d[2] == "3":
        return d[2:]

    return None


def cargar_numeros(csv_path: Path):
    validos, invalidos = [], []

    # Fallback de encoding para Windows
    encodings = ["utf-8-sig", "utf-8", "cp1252", "latin-1"]

    for enc in encodings:
        try:
            with csv_path.open("r", encoding=enc, newline="") as f:
                reader = csv.DictReader(f)

                if "numero" not in (reader.fieldnames or []):
                    raise ValueError("El CSV debe tener una columna llamada 'numero'.")

                for row in reader:
                    raw = row["numero"]
                    n = normalizar_numero(raw)

                    if n:
                        validos.append(n)
                    else:
                        invalidos.append(str(raw))

            break
        except UnicodeDecodeError:
            continue

    # Eliminar duplicados manteniendo orden
    seen = set()
    out = []
    for n in validos:
        if n not in seen:
            seen.add(n)
            out.append(n)

    return out, invalidos


def construir_links(numeros):
    # Encode robusto: UTF-8 + sin caracteres "safe"
    encoded = urllib.parse.quote(MENSAJE, safe="", encoding="utf-8", errors="strict")

    # Ir directo a WhatsApp Web (evita la pantalla de wa.me que daña los emojis)
    return [(n, f"https://web.whatsapp.com/send?phone=57{n}&text={encoded}") for n in numeros]



def generar_html(links, out_html: Path):
    html = [
        "<html><head><meta charset='utf-8'><title>Links WhatsApp</title></head><body>",
        "<h2>Links para enviar por WhatsApp</h2>",
        "<p>Abre cada enlace y presiona <b>Enviar</b> en WhatsApp.</p>",
        "<ol>",
    ]

    for n, url in links:
        html.append(f"<li><a href='{url}' target='_blank'>57{n}</a></li>")

    html += ["</ol></body></html>"]

    out_html.write_text("\n".join(html), encoding="utf-8")


def abrir_en_tandas(links, tam_tanda, pausa_s):
    total = len(links)

    print("\n⚠️ No uses el mouse mientras corre el proceso.")
    print("⚠️ Presiona CTRL + C para detener en cualquier momento.\n")

    for i, (_, url) in enumerate(links, start=1):

        print(f"\nAbriendo {i} de {total}")
        webbrowser.open(url)

        # Espera a que cargue WhatsApp Web
        time.sleep(10)

        input("👉 Presiona ENTER después de enviar el mensaje...")

        # Pequeña pausa antes del siguiente
        time.sleep(2)

        # Pausa adicional cada X mensajes (control anti-bloqueo)
        if i % tam_tanda == 0 and i < total:
            print(f"\n⏸ Pausa preventiva de {pausa_s} segundos...")
            time.sleep(pausa_s)


def main():
    csv_path = Path("numeros.csv")
    out_html = Path("links_whatsapp.html")

    if not csv_path.exists():
        raise FileNotFoundError("No encuentro 'numeros.csv' en esta carpeta.")

    numeros, invalidos = cargar_numeros(csv_path)
    links = construir_links(numeros)

    generar_html(links, out_html)

    print(f"✅ Generé {out_html} con {len(links)} links.")

    if invalidos:
        print(" Números ignorados por formato inválido:", ", ".join(invalidos))

    if ABRIR_AUTOMATICO:
        abrir_en_tandas(links, TAM_TANDA, PAUSA_SEGUNDOS)
        print("\n✅ Listo: en cada chat solo presiona Enviar.")


if __name__ == "__main__":
    main()
