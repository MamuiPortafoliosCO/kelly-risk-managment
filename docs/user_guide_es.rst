Guía del Usuario - RiskOptima Engine
====================================

Esta guía completa explica todas las características y funcionalidades de RiskOptima Engine, desde conceptos básicos hasta técnicas avanzadas de análisis de riesgo.

📑 **Contenido**
---------------

- :ref:`conceptos-basicos`
- :ref:`carga-datos`
- :ref:`analisis-rendimiento`
- :ref:`optimizacion-kelly`
- :ref:`optimo-f`
- :ref:`simulaciones-monte-carlo`
- :ref:`integracion-mt5`
- :ref:`reportes`
- :ref:`mejores-practicas`

.. _conceptos-basicos:

🧠 **Conceptos Básicos del Análisis de Riesgo**
------------------------------------------------

**Entendiendo el Trading Cuantitativo**

RiskOptima Engine se basa en principios matemáticos probados para analizar y optimizar estrategias de trading. Los conceptos clave incluyen:

**Métricas de Rendimiento Tradicionales:**

- **Win Rate**: Porcentaje de operaciones ganadoras
- **Profit Factor**: Ganancia total ÷ Pérdida total
- **Expectancy**: Valor esperado por operación
- **Max Drawdown**: Mayor caída del capital desde el pico

**Conceptos de Riesgo Avanzados:**

- **Criterio de Kelly**: Método matemático para determinar el tamaño óptimo de posición
- **Óptimo F**: Algoritmo para maximizar el crecimiento geométrico
- **Simulación Monte Carlo**: Modelado probabilístico de escenarios futuros

.. _carga-datos:

📊 **Carga y Validación de Datos**
-----------------------------------

**Formatos Soportados**

RiskOptima Engine acepta datos de trading en dos formatos principales:

**CSV (Recomendado):**

.. code-block:: csv

   Symbol,Type,Volume,Open Price,Close Price,Profit,Commission,Swap
   EURUSD,Buy,0.10,1.0850,1.0900,50.00,0.50,0.00
   GBPUSD,Sell,0.05,1.2750,1.2700,-25.00,0.25,-0.10

**XML (MT5 Nativo):**

.. code-block:: xml

   <Positions>
     <Position>
       <Symbol>EURUSD</Symbol>
       <Type>Buy</Type>
       <Volume>0.10</Volume>
       <OpenPrice>1.0850</OpenPrice>
       <ClosePrice>1.0900</ClosePrice>
       <Profit>50.00</Profit>
       <Commission>0.50</Commission>
       <Swap>0.00</Swap>
     </Position>
   </Positions>

**Campos Requeridos:**

- **Symbol**: Par de divisas o instrumento
- **Type**: "Buy" o "Sell"
- **Volume**: Tamaño de la posición
- **Open Price**: Precio de entrada
- **Close Price**: Precio de salida
- **Profit**: P&L de la operación
- **Commission**: Comisiones (opcional)
- **Swap**: Costo de swap (opcional)

**Validación Automática**

La aplicación valida automáticamente:

- ✅ Tipos de datos correctos
- ✅ Campos requeridos presentes
- ✅ Consistencia de datos (profit vs precios)
- ✅ Valores numéricos válidos
- ❌ Outliers estadísticos
- ❌ Datos faltantes o corruptos

.. _analisis-rendimiento:

📈 **Análisis de Rendimiento Detallado**
-----------------------------------------

**Métricas Calculadas**

**Estadísticas Básicas:**

- **Total Trades**: Número total de operaciones
- **Winning Trades**: Operaciones ganadoras
- **Losing Trades**: Operaciones perdedoras
- **Win Rate**: Winning Trades ÷ Total Trades

**Métricas de Ganancia:**

- **Average Win**: Ganancia promedio de operaciones ganadoras
- **Average Loss**: Pérdida promedio de operaciones perdedoras
- **Win/Loss Ratio**: Average Win ÷ |Average Loss|
- **Profit Factor**: (Win Rate × Average Win) ÷ ((1-Win Rate) × |Average Loss|)

**Métricas de Riesgo:**

- **Largest Win**: Mayor ganancia individual
- **Largest Loss**: Mayor pérdida individual
- **Max Drawdown**: Mayor caída del capital
- **Recovery Factor**: Ganancia total ÷ Max Drawdown

**Métricas Avanzadas:**

- **Expectancy**: (Win Rate × Average Win) - ((1-Win Rate) × |Average Loss|)
- **Sharpe Ratio**: Retorno ajustado por riesgo (cuando disponible)
- **Calmar Ratio**: Retorno ÷ Max Drawdown anualizado

**Interpretación de Resultados**

**Profit Factor:**
- > 1.5: Excelente estrategia
- 1.2-1.5: Buena estrategia
- 1.0-1.2: Estrategia marginal
- < 1.0: Estrategia perdedora

**Expectancy:**
- Positivo: Estrategia rentable a largo plazo
- Negativo: Estrategia no rentable

**Max Drawdown:**
- < 10%: Riesgo bajo
- 10-20%: Riesgo moderado
- > 20%: Alto riesgo

.. _optimizacion-kelly:

🎯 **Optimización con el Criterio de Kelly**
--------------------------------------------

**¿Qué es el Criterio de Kelly?**

El Criterio de Kelly es una fórmula matemática que determina qué porcentaje de su capital debería arriesgar en cada operación para maximizar el crecimiento a largo plazo.

**Fórmula Básica:**

.. math::

   f* = \frac{p - q}{R}

Donde:
- **f*** = Fracción óptima del capital a arriesgar
- **p** = Probabilidad de ganar
- **q** = Probabilidad de perder (1-p)
- **R** = Ratio ganancia/pérdida promedio

**Ejemplo Práctico:**

Si tiene:
- Win Rate: 60% (p = 0.6)
- Win/Loss Ratio: 2.0 (R = 2.0)

Entonces:

.. math::

   f* = \frac{0.6 - 0.4}{2.0} = \frac{0.2}{2.0} = 0.1

**Interpretación:** Debería arriesgar 10% de su capital por operación.

**Kelly Fraccionario**

El Kelly completo puede ser muy agresivo. Se recomienda usar fracciones:

- **Quarter Kelly (0.25x)**: f* × 0.25 - Muy conservador
- **Half Kelly (0.5x)**: f* × 0.5 - Conservador
- **Full Kelly (1.0x)**: f* × 1.0 - Agresivo pero óptimo matemáticamente

**Limitaciones del Kelly:**

- Asume independencia entre operaciones
- No considera riesgo psicológico
- Puede ser demasiado volátil para la mayoría de traders
- No funciona bien con estrategias correlacionadas

.. _optimo-f:

🔬 **Optimización con Óptimo F**
---------------------------------

**¿Qué es Óptimo F?**

Óptimo F es un algoritmo desarrollado por Ralph Vince que encuentra el tamaño de posición que maximiza el crecimiento geométrico de capital, independientemente de la dirección del mercado.

**Concepto de Terminal Wealth Relative (TWR):**

.. math::

   TWR(f) = \prod_{i=1}^{n} (1 + f \times \frac{-trade_i}{largest\_loss})

Donde:
- **f** = Fracción a optimizar
- **trade_i** = Resultado de cada operación
- **largest_loss** = Mayor pérdida histórica

**Ventajas sobre Kelly:**

- No asume dirección del mercado
- Funciona con cualquier distribución de retornos
- Más robusto con estrategias asimétricas
- Menos sensible a outliers

**Cuándo usar Óptimo F vs Kelly:**

- **Use Kelly**: Cuando tiene una estrategia direccional clara con win rate consistente
- **Use Óptimo F**: Cuando tiene una estrategia de "picking tops/bottoms" o mercados volatiles

.. _simulaciones-monte-carlo:

🎲 **Simulaciones Monte Carlo para Desafíos**
----------------------------------------------

**¿Cómo Funcionan las Simulaciones?**

1. **Bootstrap Resampling**: Se crean nuevas muestras de sus operaciones históricas usando muestreo con reemplazo
2. **Simulación de Equity**: Se aplica cada muestra simulada al capital inicial
3. **Verificación de Reglas**: Se chequea cumplimiento de límites del desafío
4. **Cálculo Estadístico**: Se calcula la probabilidad de éxito

**Parámetros del Desafío Típicos:**

- **Account Size**: Capital inicial ($100,000)
- **Profit Target**: Meta de ganancia (10%)
- **Max Daily Loss**: Pérdida máxima diaria (5%)
- **Max Overall Loss**: Pérdida máxima total (10%)
- **Min Trading Days**: Días mínimos de trading (30)

**Interpretación de Resultados:**

**Pass Rate (Tasa de Aprobación):**
- > 80%: Excelentes chances de éxito
- 60-80%: Buenas chances, considere ajustes menores
- 40-60%: Chances moderadas, revise estrategia
- < 40%: Dificultades significativas, reconsiderar enfoque

**Confidence Interval:**
- Rango estrecho: Resultados consistentes
- Rango amplio: Alta variabilidad, resultados menos confiables

**Número Óptimo de Simulaciones:**

- **100**: Resultados preliminares rápidos
- **1,000**: Análisis estándar (recomendado)
- **10,000**: Análisis exhaustivo (más tiempo)

.. _integracion-mt5:

🔗 **Integración en Tiempo Real con MT5**
-------------------------------------------

**Configuración de MT5**

1. **Instalar MT5**: Descargue desde su broker o sitio oficial
2. **Configurar cuenta**: Inicie sesión con sus credenciales
3. **Habilitar API**: Asegúrese de que "Allow automated trading" esté habilitado

**Conexión en RiskOptima Engine**

1. **Iniciar MT5**: La terminal debe estar ejecutándose
2. **Conectar desde la app**: Haga clic en "Connect to MT5" en la barra lateral
3. **Verificar estado**: La conexión se confirma automáticamente

**Datos Disponibles en Tiempo Real**

- **Balance**: Capital actual de la cuenta
- **Equity**: Valor actual incluyendo P&L flotante
- **Margin**: Margen utilizado
- **Free Margin**: Margen disponible
- **Margin Level**: Nivel de margen porcentual

**Solución de Problemas de Conexión**

**Error: "MT5 not found"**
- Asegúrese de que MT5 esté instalado y ejecutándose
- Verifique que la ruta de instalación sea estándar

**Error: "Connection timeout"**
- Reinicie MT5
- Desactive firewall temporalmente
- Verifique que no haya otras aplicaciones usando el puerto

**Error: "DLLs not allowed"**
- En MT5: Tools → Options → Expert Advisors
- Habilite "Allow automated trading"
- Habilite "Allow DLL imports"

.. _reportes:

📋 **Generación de Reportes Profesionales**
---------------------------------------------

**Tipos de Reportes Disponibles**

**1. Performance Analysis Report**
   - Resumen ejecutivo de métricas
   - Análisis detallado de riesgo
   - Curvas de capital con anotaciones
   - Recomendaciones de optimización

**2. Risk Optimization Report**
   - Resultados del Criterio de Kelly
   - Análisis de Óptimo F
   - Simulaciones Monte Carlo detalladas
   - Comparación de escenarios

**3. Comprehensive Analysis Report**
   - Todos los análisis en un documento
   - Visualizaciones completas
   - Recomendaciones ejecutivas
   - Apéndices técnicos

**Formatos de Exportación**

- **PDF**: Reportes profesionales con formato
- **CSV**: Datos crudos para análisis externos
- **PNG/SVG**: Gráficos individuales de alta calidad

**Personalización de Reportes**

- **Plantillas**: Múltiples diseños disponibles
- **Colores**: Temas personalizables
- **Logos**: Soporte para branding personalizado (futuro)
- **Idiomas**: Soporte multi-idioma

.. _mejores-practicas:

✨ **Mejores Prácticas y Consejos Avanzados**
----------------------------------------------

**Preparación de Datos**

- **Mínimo 100 operaciones**: Para análisis estadísticamente significativo
- **Datos limpios**: Remover operaciones manuales o de prueba
- **Período representativo**: Incluir diferentes condiciones de mercado
- **Consistencia**: Usar misma estrategia durante todo el período

**Interpretación de Resultados**

- **Contexto importa**: Los números son guías, no reglas absolutas
- **Riesgo psicológico**: Considere su tolerancia personal al riesgo
- **Validación**: Pruebe estrategias en diferentes mercados/condiciones
- **Actualización**: Re-evalúe periódicamente con nuevos datos

**Optimización de Rendimiento**

- **Hardware**: Más núcleos = simulaciones más rápidas
- **Memoria**: 16GB+ para datasets grandes
- **Almacenamiento**: SSD para carga rápida de datos
- **Paralelización**: Aproveche múltiples núcleos para cálculos

**Gestión de Riesgos**

- **Nunca arriesgue más del 1-2%** por operación (independientemente del Kelly)
- **Considere correlación**: Operaciones no son siempre independientes
- **Tamaño de muestra**: Más datos = resultados más confiables
- **Validación fuera de muestra**: Pruebe con datos no usados en optimización

**Casos de Uso Avanzados**

**Para Traders Prop Firm:**

1. Analice su historial de 6-12 meses
2. Configure parámetros del desafío específico
3. Ejecute múltiples simulaciones con diferentes Kelly fractions
4. Use el percentil 25-50 para estimaciones conservadoras

**Para Gestores de Carteras:**

1. Analice rendimiento histórico completo
2. Compare múltiples estrategias simultáneamente
3. Use Óptimo F para asignación de capital
4. Genere reportes mensuales automatizados

**Para Desarrolladores de Estrategias:**

1. Use la API para integración con sistemas existentes
2. Implemente validación estadística automática
3. Compare backtests con análisis de RiskOptima
4. Automatice reportes de rendimiento

---

**Recursos Adicionales**

- :doc:`api_reference` - Documentación técnica completa
- :doc:`troubleshooting` - Solución de problemas comunes
- :doc:`developer_guide` - Guía para desarrolladores avanzados

¿Necesita ayuda adicional? Visite nuestros `issues en GitHub <https://github.com/MamuiPortafoliosCO/kelly-risk-managment/issues>`_.