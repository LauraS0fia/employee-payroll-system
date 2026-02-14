from app.services.payroll import calcular_nomina

resultado = calcular_nomina(
    sueldo_base=2000000,
    dias=30,
    horas_extra=10
)

print(resultado)