def calcular_nomina(sueldo_base: float, dias: int, horas_extra: int):
    # 1. Auxilio de transporte (solo si sueldo <= 2 SMMLV aprox)
    auxilio = 200000 if sueldo_base <= 2600000 else 0

    # 2. Valor día trabajado
    valor_dia = sueldo_base / 30

    # 3. Total ganado por días
    total_dias = valor_dia * dias

    # 4. Valor hora extra (125%)
    valor_hora = sueldo_base / 240
    total_horas_extra = valor_hora * 1.25 * horas_extra

    # 5. Devengado
    devengado = total_dias + total_horas_extra + auxilio

    # 6. Salud y pensión (4% cada uno)
    salud = devengado * 0.04
    pension = devengado * 0.04

    # 7. Deducciones
    deducciones = salud + pension

    # 8. Neto a pagar
    neto = devengado - deducciones

    return {
        "auxilio": round(auxilio, 2),
        "horas_extras": round(total_horas_extra, 2),
        "devengado": round(devengado, 2),
        "salud": round(salud, 2),
        "pension": round(pension, 2),
        "deducciones": round(deducciones, 2),
        "neto": round(neto, 2),
    }