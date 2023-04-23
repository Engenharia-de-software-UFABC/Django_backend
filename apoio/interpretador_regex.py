import re


def dia_horario_regex(texto):
    regex = r"([a-zA-Z]+)\sdas\s(\d{2}:\d{2}\sàs\s\d{2}:\d{2}),\s([a-zA-Z ]+)"

    matches = re.findall(regex, texto)

    result = []
    for match in matches:
        result.append({
            "dia_semana": match[0],
            "horario": match[1],
            "tipo_recorrencia": match[2].strip()
        })

    return result
