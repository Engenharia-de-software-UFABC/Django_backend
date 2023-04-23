import re


def dia_horario_regex(texto, nome_professor):
    regex = r"([a-zA-Z]+)\sdas\s(\d{2}:\d{2}\sàs\s\d{2}:\d{2}),\s*sala\s*([A-Z]-\d+-\d+)\s*,\s*([a-zA-Z ]+)"

    matches = re.findall(regex, texto)

    result = []
    for match in matches:
        result.append({
            "dia_semana": match[0],
            "horario": match[1],
            "sala": match[2],
            "tipo_recorrencia": match[3].strip(),
            "professor": nome_professor
        })

    return result
