from flask import Blueprint, request, jsonify
from app.services.payroll import calcular_nomina

payroll_bp = Blueprint("payroll", __name__)

@payroll_bp.route("/calcular", methods=["POST"])
def calcular():
    data = request.get_json()

    nombre = data.get("nombre")
    sueldo = float(data.get("sueldo", 0))
    horas_extras = float(data.get("horas_extras", 0))

    resultado = calcular_nomina(nombre, sueldo, horas_extras)

    return jsonify(resultado)