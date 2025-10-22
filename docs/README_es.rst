README - RiskOptima Engine
==========================

|license| |python| |rust| |docker|

.. |license| image:: https://img.shields.io/badge/License-MIT-blue.svg
   :target: https://opensource.org/licenses/MIT
   :alt: Licencia MIT

.. |python| image:: https://img.shields.io/badge/Python-3.9+-blue.svg
   :target: https://www.python.org/
   :alt: Python 3.9+

.. |rust| image:: https://img.shields.io/badge/Rust-2021-orange.svg
   :target: https://www.rust-lang.org/
   :alt: Rust 2021

.. |docker| image:: https://img.shields.io/badge/Docker-Supported-blue.svg
   :target: https://www.docker.com/
   :alt: Docker

**RiskOptima Engine** es una herramienta cuantitativa avanzada de análisis y gestión de riesgos diseñada específicamente para traders de MetaTrader 5. El sistema proporciona capacidades avanzadas de modelado de riesgos incluyendo optimización del Criterio de Kelly, dimensionamiento de posiciones Óptimo F y simulación Monte Carlo para evaluación de desafíos de firmas propietarias de trading.

🚀 **Características Principales**
----------------------------------

🔬 **Análisis de Rendimiento Avanzado**
   - Cálculo completo de métricas estadísticas de trading
   - Análisis de curvas de capital con indicadores de riesgo
   - Identificación de mejores y peores operaciones

📊 **Modelos de Riesgo Cuantitativos**
   - **Criterio de Kelly**: Optimización de tamaño de posición con multiplicadores fraccionarios
   - **Óptimo F**: Algoritmo de Ralph Vince para crecimiento geométrico máximo
   - **Simulación Monte Carlo**: Evaluación probabilística de desafíos de prop firms

🔗 **Integración en Tiempo Real con MT5**
   - Monitoreo de cuenta en vivo (balance, equity, margen)
   - Sincronización automática de datos de trading
   - Conexión IPC segura sin transmisión externa de datos

🖥️ **Interfaz Web Moderna**
   - Interfaz Streamlit intuitiva con navegación por pestañas
   - Visualizaciones interactivas con Plotly
   - Carga de archivos con validación en tiempo real

⚡ **Rendimiento de Alto Nivel**
   - Núcleo computacional en Rust para máxima velocidad
   - Procesamiento paralelo con Rayon
   - Arquitectura de memoria eficiente

📈 **Reportes y Exportación**
   - Reportes PDF profesionales
   - Exportación CSV para análisis externos
   - Visualizaciones de alta calidad

🛡️ **Seguridad y Privacidad**
   - Procesamiento completamente local
   - Sin transmisión de datos externos
   - Encriptación de datos sensibles

🏗️ **Arquitectura Técnica**
---------------------------

El sistema utiliza una arquitectura de tres capas:

1. **Capa Frontend**: Interfaz web Streamlit para interacción del usuario
2. **Capa Backend**: API FastAPI con procesamiento asíncrono
3. **Núcleo Cuantitativo**: Biblioteca Rust para cálculos de alto rendimiento

.. code-block:: text

   Usuario → Frontend (Streamlit) → Backend (FastAPI) → Núcleo (Rust) → MT5 (IPC)

📋 **Requisitos del Sistema**
------------------------------

**Sistema Operativo**
   - Windows 10/11 (64-bit) - requerido para MT5
   - Linux/macOS - posible con Wine (experimental)

**Hardware Mínimo**
   - Procesador: Quad-core 2.5GHz
   - Memoria RAM: 8GB
   - Almacenamiento: 10GB espacio libre
   - Pantalla: 1920x1080 resolución mínima

**Software Requerido**
   - Python 3.9 o superior
   - Rust 1.70 o superior
   - MetaTrader 5 Terminal
   - Git (para instalación desde código fuente)

🔧 **Instalación Rápida**
-------------------------

1. **Clonar el repositorio:**

   .. code-block:: bash

      git clone https://github.com/MamuiPortafoliosCO/kelly-risk-managment.git
      cd kelly-risk-managment

2. **Instalar dependencias:**

   .. code-block:: bash

      # Instalar uv si no está disponible
      pip install uv

      # Instalar dependencias del proyecto
      uv sync

3. **Construir extensión Rust:**

   .. code-block:: bash

      # Construir la extensión Python-Rust
      uv run maturin develop

4. **Ejecutar la aplicación:**

   .. code-block:: bash

      # Opción 1: Ejecutar todo el stack
      uv run risk-optima-engine full

      # Opción 2: Ejecutar componentes individuales
      uv run risk-optima-engine backend  # API en http://localhost:8000
      uv run risk-optima-engine frontend # UI en http://localhost:8501

📖 **Primeros Pasos**
---------------------

1. **Acceder a la interfaz web** en http://localhost:8501
2. **Cargar datos de trading** desde archivos CSV/XML de MT5
3. **Analizar rendimiento** con métricas clave y curvas de capital
4. **Optimizar riesgo** usando simulaciones Monte Carlo
5. **Monitorear en tiempo real** conectándose a MT5

🎯 **Casos de Uso**
-------------------

**Para Traders Individuales**
   - Análisis de rendimiento histórico de estrategias
   - Optimización de tamaño de posición por operación
   - Evaluación de riesgo de drawdown máximo

**Para Desafíos de Prop Firms**
   - Simulación de probabilidad de aprobación
   - Optimización de parámetros de riesgo
   - Análisis de escenarios "qué pasaría si"

**Para Gestores de Carteras**
   - Análisis de riesgo de cartera
   - Optimización de asignación de capital
   - Reportes de rendimiento estandarizados

📚 **Documentación**
--------------------

- :doc:`installation` - Guía completa de instalación
- :doc:`quickstart` - Tutorial paso a paso
- :doc:`user_guide` - Guía del usuario completa
- :doc:`api_reference` - Referencia de API REST
- :doc:`developer_guide` - Guía para desarrolladores
- :doc:`troubleshooting` - Solución de problemas comunes

🧪 **Ejemplos y Datos de Prueba**
----------------------------------

El repositorio incluye datos de ejemplo para testing:

- ``example_mt5_data.csv`` - Archivo CSV de ejemplo de MT5
- Scripts de ejemplo en ``examples/``
- Tests unitarios en ``tests/``

🤝 **Contribuir**
-----------------

¡Las contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (``git checkout -b feature/AmazingFeature``)
3. Commit tus cambios (``git commit -m 'Add some AmazingFeature'``)
4. Push a la rama (``git push origin feature/AmazingFeature``)
5. Abre un Pull Request

Ver :doc:`contributing` para más detalles.

📄 **Licencia**
---------------

Este proyecto está bajo la Licencia MIT - ver el archivo :doc:`license` para más detalles.

🙋 **Soporte**
--------------

- **Documentación**: https://riskoptima-engine.readthedocs.io/
- **Issues**: https://github.com/MamuiPortafoliosCO/kelly-risk-managment/issues
- **Discusiones**: https://github.com/MamuiPortafoliosCO/kelly-risk-managment/discussions

📊 **Estado del Proyecto**
--------------------------

.. list-table:: Estado de Características
   :header-rows: 1
   :widths: 30 20 50

   * - Característica
     - Estado
     - Notas
   * - Análisis de Trading
     - ✅ Completo
     - Métricas completas, curvas de capital
   * - Criterio de Kelly
     - ✅ Completo
     - Con multiplicadores fraccionarios
   * - Óptimo F
     - ✅ Completo
     - Optimización de crecimiento geométrico
   * - Simulación Monte Carlo
     - ✅ Completo
     - Bootstrap con 1000+ simulaciones
   * - Integración MT5
     - ✅ Completo
     - Conexión IPC en tiempo real
   * - Interfaz Web
     - ✅ Completo
     - Streamlit con visualizaciones
   * - API REST
     - ✅ Completo
     - Documentación OpenAPI
   * - Docker
     - ✅ Completo
     - Despliegue contenerizado
   * - Documentación
     - ✅ Completo
     - Read the Docs completo
   * - Tests
     - 🚧 En Progreso
     - Cobertura básica implementada

🚀 **Roadmap**
---------------

**Versión 1.2.0** (Próxima)
   - Integración de Machine Learning
   - Análisis de portafolio multi-activo
   - Backtesting avanzado

**Versión 2.0.0** (Futuro)
   - Soporte multiplataforma (Linux/macOS)
   - Arquitectura de plugins
   - Interfaz móvil

---

**RiskOptima Engine** - Potenciando el Trading con Análisis Cuantitativo Avanzado