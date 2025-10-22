Guía de Inicio Rápido - RiskOptima Engine
=========================================

Esta guía le ayudará a comenzar con RiskOptima Engine en menos de 15 minutos. Aprenderá a cargar datos, analizar rendimiento y optimizar estrategias de riesgo.

🎯 **Objetivos de Esta Guía**
-----------------------------

Al final de esta guía, podrá:

- ✅ Cargar y analizar datos de trading históricos
- ✅ Calcular métricas clave de rendimiento
- ✅ Optimizar el tamaño de posición usando el Criterio de Kelly
- ✅ Ejecutar simulaciones Monte Carlo para desafíos de prop firms
- ✅ Generar reportes profesionales

⏱️ **Tiempo Estimado**: 15 minutos

🚀 **Paso 1: Iniciar la Aplicación**
-------------------------------------

1. **Abrir terminal y navegar al directorio del proyecto:**

   .. code-block:: bash

      cd risk-optima-engine

2. **Ejecutar la aplicación completa:**

   .. code-block:: bash

      uv run risk-optima-engine full

   Debería ver:

   .. code-block:: text

      Starting RiskOptima Engine (Full Stack)
      Backend: http://localhost:8000
      Frontend: http://localhost:8501
      Press Ctrl+C to stop all services

3. **Abrir su navegador web** y ir a: http://localhost:8501

¡La interfaz web debería cargar mostrando la página principal de RiskOptima Engine!

📊 **Paso 2: Cargar Datos de Trading**
---------------------------------------

1. **Navegar a "Data Upload & Analysis"** en la barra lateral

2. **Preparar archivo de datos:**

   - Use el archivo de ejemplo incluido: ``example_mt5_data.csv``
   - O exporte sus propios datos desde MT5:
     - Abra MT5 → Historial de Cuenta → Exportar → CSV/XML

3. **Cargar el archivo:**

   - Haga clic en "Choose MT5 export file"
   - Seleccione su archivo CSV
   - Seleccione "csv" como formato
   - Haga clic en "Analyze Trades"

4. **Ver resultados iniciales:**

   La aplicación procesará sus datos y mostrará:

   - **Total de operaciones**
   - **Ratio de ganancia**
   - **Factor de ganancia**
   - **Expectativa matemática**
   - **Máximo drawdown**

📈 **Paso 3: Explorar el Análisis de Rendimiento**
---------------------------------------------------

Después de cargar los datos, explore las métricas calculadas:

**Métricas Clave de Rendimiento:**

- **Total Trades**: Número total de operaciones cerradas
- **Win Rate**: Porcentaje de operaciones ganadoras
- **Profit Factor**: Ganancia total / Pérdida total
- **Expectancy**: Valor esperado por operación
- **Max Drawdown**: Mayor caída del capital desde el pico

**Curva de Capital:**

- Visualice cómo creció su capital a lo largo del tiempo
- Identifique períodos de drawdown
- Evalúe la consistencia de su estrategia

🎯 **Paso 4: Optimizar con el Criterio de Kelly**
-------------------------------------------------

1. **Ir a "Challenge Optimizer"** en la barra lateral

2. **Configurar parámetros del desafío:**

   - **Account Size**: Capital inicial (ej: $100,000)
   - **Profit Target**: Meta de ganancia (ej: 10%)
   - **Max Daily Loss**: Pérdida máxima diaria (ej: 5%)
   - **Max Overall Loss**: Pérdida máxima total (ej: 10%)
   - **Min Trading Days**: Días mínimos de trading (ej: 30)

3. **Ejecutar optimización:**

   - Haga clic en "🚀 Run Optimization"
   - Espere a que complete las simulaciones Monte Carlo

4. **Interpretar resultados:**

   - **Recommended Risk Fraction**: Porcentaje óptimo de riesgo por operación
   - **Simulated Pass Rate**: Probabilidad de pasar el desafío
   - **Confidence Interval**: Rango de confianza estadística

⚠️ **Interpretación de Resultados:**

- **Risk Fraction > 2%**: Alto riesgo - considere Kelly fraccionario
- **Risk Fraction < 0.5%**: Muy conservador - progreso lento hacia la meta
- **Pass Rate > 80%**: Buena probabilidad de éxito
- **Pass Rate < 50%**: Revisar estrategia o reducir expectativas

🔬 **Paso 5: Entender las Simulaciones Monte Carlo**
-----------------------------------------------------

RiskOptima Engine usa simulaciones Monte Carlo para:

1. **Remuestreo Bootstrap**: Crea nuevas muestras de sus operaciones históricas
2. **Simulación de Equity**: Aplica operaciones simuladas al capital inicial
3. **Verificación de Reglas**: Chequea cumplimiento de límites de pérdida y ganancia
4. **Cálculo de Probabilidades**: Estima chances de éxito del desafío

**¿Por qué 1000 simulaciones?**

- Proporciona precisión estadística suficiente
- Equilibra tiempo de procesamiento con confiabilidad
- Permite intervalos de confianza significativos

📊 **Paso 6: Generar Reportes**
--------------------------------

1. **Ir a "Reports & Visualizations"** en la barra lateral

2. **Seleccionar tipo de reporte:**

   - **Performance Analysis**: Análisis completo de rendimiento
   - **Risk Optimization**: Resultados de optimización
   - **Comprehensive Analysis**: Todo en un reporte

3. **Configurar exportación:**

   - **Format**: PDF para reportes profesionales, CSV para datos
   - Haga clic en "📄 Generate Report"

4. **Descargar resultados:**

   Los reportes incluyen:
   - Resumen ejecutivo
   - Métricas detalladas
   - Gráficos profesionales
   - Recomendaciones de riesgo

🔗 **Paso 7: Integración con MT5 (Opcional)**
----------------------------------------------

Para monitoreo en tiempo real:

1. **Asegurarse de que MT5 esté ejecutándose**

2. **En la aplicación, hacer clic en "Connect to MT5"** en la barra lateral

3. **Ver métricas en tiempo real:**

   - Balance actual
   - Equity
   - Margen disponible
   - Nivel de margen

4. **Configurar auto-refresh** para actualizaciones continuas

⚡ **Consejos para Mejor Rendimiento**
-------------------------------------

**Optimización de Hardware:**

- **CPU**: Más núcleos = simulaciones más rápidas
- **RAM**: 16GB+ recomendado para datasets grandes
- **SSD**: Almacenamiento rápido mejora tiempos de carga

**Mejores Prácticas de Datos:**

- Use al menos 100 operaciones para análisis significativos
- Incluya diferentes condiciones de mercado
- Evite datos de "curve fitting" excesivo

**Interpretación de Resultados:**

- El Criterio de Kelly es teórico - considere riesgo psicológico
- Las simulaciones Monte Carlo no predicen el futuro
- Use resultados como guía, no como regla absoluta

🧪 **Solución de Problemas Comunes**
------------------------------------

**"Rust extension not available"**

.. code-block:: bash

   # Reconstruir extensión
   uv run maturin develop

**"MT5 connection failed"**

- Asegúrese de que MT5 esté abierto
- Verifique que no haya firewall bloqueando conexiones locales
- Reinicie MT5 y la aplicación

**"Analysis failed"**

- Verifique formato del archivo CSV
- Asegúrese de que las columnas requeridas estén presentes
- Chequee que no haya datos corruptos

📚 **¿Qué Sigue?**
-------------------

Ahora que completó el inicio rápido:

1. **Explore características avanzadas** en la documentación completa
2. **Experimente con diferentes parámetros** de desafío
3. **Compare múltiples estrategias** usando los reportes
4. **Integre con su flujo de trabajo** de trading diario

**Recursos Adicionales:**

- :doc:`user_guide` - Guía completa del usuario
- :doc:`api_reference` - Documentación técnica de API
- :doc:`troubleshooting` - Solución de problemas avanzados

🎉 **¡Felicitaciones!**

Ha completado exitosamente el inicio rápido de RiskOptima Engine. Ahora tiene las herramientas para analizar su trading, optimizar riesgos y maximizar sus chances de éxito en desafíos de prop firms.

¿Preguntas? Visite nuestros `issues en GitHub <https://github.com/MamuiPortafoliosCO/kelly-risk-managment/issues>`_ o la documentación completa.