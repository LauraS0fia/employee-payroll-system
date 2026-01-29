class Constantes:
    """clase para almacenar todas las constantes (valores que no cambian)"""
    SMLV = 1423500
    auxilio_transporte = 200000
    hSemanales = 46/6

    #porcentajes para horas extras
    eDiurnas = 1.25
    eNocturnas = 1.75
    eDiaFestivas = 2
    eNochFestivas = 2.5

    #porcentajes de aportes
    porcentajeSaludEmpleado = 0.04
    porcentajePensionEmpleado = 0.04
    porcentajeSaludEmpleador = 0.085
    porcentajePensionEmpleador= 0.12

    #porcentajes parafiscales
    porcentajeCaja = 0.04
    porcentajeICBF = 0.03
    porcentajeSENA = 0.02

    #porcentajes prestaciones sociales
    porcentajeCesantias = 0.0833
    porcentajeInteresesCesantias = 0.01
    porcentajePrima = 0.0833
    porcentajeVacaciones = 0.0417

    #niveles de riesgo arl
    arlPorcentajes = {
        1: 0.0052,
        2: 0.0104,
        3: 0.0244,
        4: 0.0435,
        5: 0.0696
    }

class Empleado:
    """clase que representa al empleado y los datos de este en nomina """
    
    def __init__(self):
        self.nombre = ""
        self.sueldoBasico = 0
        self.diasTrabajados = 0
        self.sueldo = 0
        self.horasExtras = 0
        self.auxilioTransporte = 0
        self.total_devengado = 0
        self.salud = 0
        self.pension = 0
        self.total_deducciones = 0
        self.neto_pagar = 0
        self.nivel_riesgo = 0
        self.arl_valor = 0
        self.parafiscales = (0, 0, 0) # (caja, icbf, sena)

    def almacenarDatos(self, datos_empleado):
        """Recolectar todos los datos del empleado"""
        self.nombre = datos_empleado['nombre']
        self.sueldoBasico = float(datos_empleado['sueldo_basico'])
        self.diasTrabajados = int(datos_empleado['dias_trabajados'])
        self.nivel_riesgo = int(datos_empleado['nivel_riesgo'])
        
        # Calcular horas extras si existen
        self.horasExtras = 0
        if 'hed' in datos_empleado and datos_empleado['hed'] > 0:
            self._calcularHoraExtra('diurna', datos_empleado['hed'])
        if 'hen' in datos_empleado and datos_empleado['hen'] > 0:
            self._calcularHoraExtra('nocturna', datos_empleado['hen'])
        if 'hedf' in datos_empleado and datos_empleado['hedf'] > 0:
            self._calcularHoraExtra('diurna_festiva', datos_empleado['hedf'])
        if 'henf' in datos_empleado and datos_empleado['henf'] > 0:
            self._calcularHoraExtra('nocturna_festiva', datos_empleado['henf'])
        
        self._calcularSueldo()
        self._asignarAuxilioTransporte()
        self._calcularDeducciones()
        self._calcularNetoPagar()
        self._calcularArl()
        self._calcularParafiscales()
        return self

    def _calcularSueldo(self):
        """Calcula el sueldo dependiendo el basico y cuantos días trabajo"""
        self.sueldo = (self.sueldoBasico / 30) * self.diasTrabajados

    def _calcularHoraExtra(self, tipo, cantidad):
        """Calcula el valor de las horas extras según tipo"""
        valorHora = (self.sueldoBasico / 30) / Constantes.hSemanales
        
        if tipo == 'diurna':
            valor_he = valorHora * cantidad * Constantes.eDiurnas
        elif tipo == 'nocturna':
            valor_he = valorHora * cantidad * Constantes.eNocturnas
        elif tipo == 'diurna_festiva':
            valor_he = valorHora * cantidad * Constantes.eDiaFestivas
        elif tipo == 'nocturna_festiva':
            valor_he = valorHora * cantidad * Constantes.eNochFestivas
        
        self.horasExtras += valor_he

    def _asignarAuxilioTransporte(self):
        """asignar el auxilio de transporte dependiendo el sueldo basico"""
        if self.sueldoBasico < Constantes.SMLV * 2:
            self.auxilioTransporte = Constantes.auxilio_transporte
        else:
            self.auxilioTransporte = 0

    def _calcularDeducciones(self):
        """calcula deducciones de salud y pension (4% cada una)"""
        self.total_devengado = self.sueldo + self.horasExtras + self.auxilioTransporte
        base_deducciones = self.total_devengado - self.auxilioTransporte
        self.salud = base_deducciones * Constantes.porcentajeSaludEmpleado
        self.pension = base_deducciones * Constantes.porcentajePensionEmpleado
        self.total_deducciones = self.salud + self.pension

    def _calcularNetoPagar(self):
        """calcula el neto a pagar restando las deducciones al total devengado"""
        self.neto_pagar = self.total_devengado - self.total_deducciones

    def _calcularArl(self):
        """calcula el valor de la arl dependiendo el nivel de riesgo"""
        porcentaje_arl = Constantes.arlPorcentajes.get(self.nivel_riesgo, 0)
        base_aporte = self.total_devengado - self.auxilioTransporte
        self.arl_valor = base_aporte * porcentaje_arl

    def _calcularParafiscales(self):
        """calcular los aportes parafiscales solo si el empleado gana mas de 10 smlv"""
        base = self.total_devengado - self.auxilioTransporte
        if self.sueldoBasico >= Constantes.SMLV * 10:
            caja = base * Constantes.porcentajeCaja
            icbf = base * Constantes.porcentajeICBF
            sena = base * Constantes.porcentajeSENA
            self.parafiscales = (caja, icbf, sena)
        else:
            self.parafiscales = (0, 0, 0)

    def to_dict(self):
        """convierte los datos del empleado en un diccionario"""
        return {
            "Nombre": self.nombre,
            "Sueldo": self.sueldo,
            "Auxilio": self.auxilioTransporte,
            "Horas Extras": self.horasExtras,
            "Devengado": self.total_devengado,
            "Salud": self.salud,
            "Pensión": self.pension,
            "Total Deducciones": self.total_deducciones,
            "Neto": self.neto_pagar,
        }

class SistemaNomina:
    """clase principal para manejar el sistema de la nomina (los totales de todo)"""
    
    def __init__(self):
        self.empleados = [] #array para almacenar los empleados
        self.arl_acumulado = {
            nivel: {"porcentaje": Constantes.arlPorcentajes[nivel], "valor": 0}
            for nivel in range(1, 6)
        }
        self.total_sueldo = 0
        self.total_auxilio = 0
        self.total_horas = 0
        self.total_devengado = 0
        self.total_salud = 0
        self.total_pension = 0
        self.total_deducciones = 0
        self.total_neto = 0

    def registrar_empleado(self, datos_empleado):
        """Registra la información de un empleado"""
        empleado = Empleado().almacenarDatos(datos_empleado)
        
        # Acumular ARL por nivel
        self.arl_acumulado[empleado.nivel_riesgo]["valor"] += empleado.arl_valor
        
        # Guardar empleado
        self.empleados.append(empleado)
        return empleado

    def generar_reporte_nomina(self):
        """genera el reporte de la nomina con los totales"""
        # Reiniciar totales
        self.total_sueldo = 0
        self.total_auxilio = 0
        self.total_horas = 0
        self.total_devengado = 0
        self.total_salud = 0
        self.total_pension = 0
        self.total_deducciones = 0
        self.total_neto = 0
        
        reporte = []
        
        for emp in self.empleados:
            datos = emp.to_dict()
            reporte.append(datos)
            
            # Acumular los totales
            self.total_sueldo += datos['Sueldo']
            self.total_auxilio += datos['Auxilio']
            self.total_horas += datos['Horas Extras']
            self.total_devengado += datos['Devengado']
            self.total_salud += datos['Salud']
            self.total_pension += datos['Pensión']
            self.total_deducciones += datos['Total Deducciones']
            self.total_neto += datos['Neto']
        
        return reporte

    def calcular_aportes_empleador(self):
        """Calcula los aportes del empleador"""
        base_aporte_total = self.total_devengado - self.total_auxilio
        
        # Salud
        salud_4 = base_aporte_total * Constantes.porcentajeSaludEmpleador
        
        # Pension
        pension_12 = base_aporte_total * Constantes.porcentajePensionEmpleador
        pension_4 = base_aporte_total * Constantes.porcentajePensionEmpleado
        pension_16 = pension_12 + pension_4
        
        # ARL
        total_arl = sum(v['valor'] for v in self.arl_acumulado.values())
        
        total_aportes_empleador = salud_4 + pension_12 + total_arl
        
        return {
            'base_aporte_total': base_aporte_total,
            'salud_empleador': salud_4,
            'pension_empleador': pension_12,
            'total_arl': total_arl,
            'total_aportes_empleador': total_aportes_empleador
        }

    def _calcularParafiscales(self):
        """Calcula los aportes parafiscales"""
        total_caja = sum(emp.parafiscales[0] for emp in self.empleados)
        total_icbf = sum(emp.parafiscales[1] for emp in self.empleados)
        total_sena = sum(emp.parafiscales[2] for emp in self.empleados)
        total_parafiscales = total_caja + total_icbf + total_sena
        
        return {
            'total_caja': total_caja,
            'total_icbf': total_icbf,
            'total_sena': total_sena,
            'total_parafiscales': total_parafiscales
        }

    def _calcularPrestacionesSociales(self, base_aporte_total):
        """Calcula las provisiones para prestaciones sociales"""
        cesantias = base_aporte_total * Constantes.porcentajeCesantias
        intereses_cesantias = cesantias * Constantes.porcentajeInteresesCesantias
        prima = base_aporte_total * Constantes.porcentajePrima
        
        # Vacaciones se calculan sobre el promedio del salario básico
        salario_promedio = sum(emp.sueldoBasico for emp in self.empleados) / len(self.empleados)
        vacaciones = salario_promedio * Constantes.porcentajeVacaciones
        
        total_provisiones = cesantias + intereses_cesantias + prima + vacaciones
        
        return {
            'cesantias': cesantias,
            'intereses_cesantias': intereses_cesantias,
            'prima': prima,
            'vacaciones': vacaciones,
            'total_provisiones': total_provisiones
        }