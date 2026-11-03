"""Líneas del narrador de "Las reglas del Silbón". Una toma de ElevenLabs por línea: clave -> (etiquetas de entonación, subtítulo).

El subtítulo es lo que sale en pantalla: lo que va entre *asteriscos* se pinta en amarillo (palabra clave). Las etiquetas (eleven_v4)
solo se mandan a la voz. Voz: ElevenLabs DdKbXdRlBmj7Ty7N0FVr. Los archivos van en audio/narrador/<clave>.mp3 y el mapa
texto limpio -> archivo en audio/narrador/lineas.json (lo escribe `python -m historias.silbon.narracion`).
"""
import json
from pathlib import Path

SUSURRO = "[whispers] "
SUAVE = "[softly] "
TENSO = "[nervous] [softly] "

LINEAS = {
    # ---- gancho (0-5 s) ----
    "g_0": (SUSURRO, "Si oyes este *silbido*…"),
    "g_1": (SUAVE, "alguien en tu casa *no amanece*."),
    # ---- llegas al hato ----
    "l_0": (SUAVE, "Imagina que la *noche* te alcanza en los llanos."),
    "l_1": (SUAVE, "Un viejo llanero te jala del brazo."),
    # ---- el letrero ----
    "r_0": (SUAVE, "Adentro, un letrero con *cuatro reglas*."),
    # ---- las reglas ----
    "r1_0": (SUAVE, "Regla uno: si el silbido suena *cerca*, está lejos."),
    "r1_1": (SUSURRO, "Si suena *lejos*… ya está aquí."),
    "r2_0": (SUAVE, "Regla dos: nadie bebe *aguardiente* de noche."),
    "r3_0": (SUAVE, "Regla tres: los *perros* nunca se callan."),
    "r4_0": (SUAVE, "Regla cuatro: si caen *huesos* junto a la puerta…"),
    "r4_1": (SUSURRO, "cuéntalos en *voz alta*."),
    # ---- cuatro horas después ----
    "t_0": (SUAVE, "Cuatro horas después, Ramiro *destapa* su botella."),
    "t_1": (SUAVE, "Los perros ladran. Alguien los manda a *callar*."),
    # ---- el silencio y el silbido ----
    "s_0": (SUSURRO, "*Silencio*."),
    "s_1": (SUAVE, "El silbido suena *cerca*. Todos sonríen."),
    "s_2": (TENSO, "Pero ahora suena… *lejísimos*."),
    # ---- la puerta ----
    "p_0": (SUSURRO, "Algo se sienta junto a la *puerta*."),
    "p_1": (SUSURRO, "Un saco cae… y empieza a *contar huesos*."),
    # ---- tú ----
    "o_0": (SUSURRO, "Solo tú estás *despierto*."),
    "o_1": (TENSO, "Si cuentas en voz alta, sabrá que lo *oyes*."),
    "o_2": (SUSURRO, "Si callas… alguien no *amanece*."),
    # ---- cierre ----
    "c_0": (SUAVE, "¿Cuentas los huesos… o te *callas*?"),
    "c_1": (SUAVE, "Comenta *1* para contar, o *2* para callar."),
}


def limpio(texto):
    """Subtítulo sin marcas de color: es la clave con la que el motor busca la toma de audio."""
    return texto.replace("*", "")


def prompt(clave):
    tags, texto = LINEAS[clave]
    return tags + limpio(texto)


def escribir_mapa():
    """Escribe audio/narrador/lineas.json con las tomas que ya están descargadas."""
    carpeta = Path(__file__).parent / "audio" / "narrador"
    mapa = {}
    for clave in LINEAS:
        if (carpeta / f"{clave}.mp3").exists():
            mapa[limpio(LINEAS[clave][1])] = {"archivo": f"{clave}.mp3", "prompt": prompt(clave)}
    (carpeta / "lineas.json").write_text(json.dumps(mapa, ensure_ascii=False, indent=1))
    faltan = [c for c in LINEAS if not (carpeta / f"{c}.mp3").exists()]
    print(f"{len(mapa)} tomas mapeadas; faltan: {faltan or 'ninguna'}")


if __name__ == "__main__":
    escribir_mapa()
