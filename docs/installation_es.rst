Guía de Instalación - RiskOptima Engine
=======================================

Esta guía proporciona instrucciones detalladas para instalar RiskOptima Engine en diferentes plataformas y entornos.

🏗️ **Requisitos Previos**
--------------------------

Antes de instalar RiskOptima Engine, asegúrese de tener los siguientes componentes:

**Software Base**
   - **Python 3.9 o superior**: https://www.python.org/downloads/
   - **Git**: https://git-scm.com/downloads
   - **Rust 1.70 o superior**: https://rustup.rs/

**Para Windows (Requerido para MT5)**
   - **MetaTrader 5 Terminal**: Descárgalo desde tu broker o https://www.metatrader5.com/
   - **Visual Studio Build Tools** (para compilar Rust): https://visualstudio.microsoft.com/visual-cpp-build-tools/
   - **PowerShell** (incluido en Windows moderno)

**Para Linux/macOS (Experimental)**
   - **Wine** (para ejecutar MT5): https://www.winehq.org/
   - **Build tools**: ``build-essential`` (Ubuntu/Debian) o Xcode (macOS)

🔍 **Verificación de Requisitos**
----------------------------------

Ejecute estos comandos para verificar que tiene todo lo necesario:

**Python:**

.. code-block:: bash

   python --version  # Debe ser 3.9 o superior
   pip --version     # Debe estar disponible

**Rust:**

.. code-block:: bash

   rustc --version   # Debe ser 1.70 o superior
   cargo --version   # Debe estar disponible

**Git:**

.. code-block:: bash

   git --version     # Debe estar disponible

🚀 **Instalación Rápida (Recomendado)**
---------------------------------------

Para la mayoría de los usuarios, use este método simplificado:

1. **Clonar el repositorio:**

   .. code-block:: bash

      git clone https://github.com/MamuiPortafoliosCO/kelly-risk-managment.git
      cd kelly-risk-managment

2. **Ejecutar el script de configuración:**

   .. code-block:: powershell

      # En Windows PowerShell
      .\scripts\setup.ps1

   .. code-block:: bash

      # En Linux/macOS
      chmod +x scripts/setup.sh
      ./scripts/setup.sh

3. **Verificar la instalación:**

   .. code-block:: bash

      uv run risk-optima-engine --help

Si todo está correcto, debería ver la ayuda del comando.

🔧 **Instalación Manual Detallada**
------------------------------------

Si prefiere instalar manualmente o tiene problemas con el script automático:

**Paso 1: Instalar UV (Gestor de Dependencias)**

.. code-block:: bash

   # Instalar uv
   pip install uv

   # Verificar instalación
   uv --version

**Paso 2: Clonar y Configurar el Proyecto**

.. code-block:: bash

   # Clonar repositorio
   git clone https://github.com/MamuiPortafoliosCO/kelly-risk-managment.git
   cd kelly-risk-managment

   # Sincronizar dependencias Python
   uv sync

**Paso 3: Construir la Extensión Rust**

.. code-block:: bash

   # Construir extensión Python-Rust
   uv run maturin develop

   # Verificar que se construyó correctamente
   uv run python -c "from risk_optima_engine import calculate_kelly_criterion; print('Rust extension working!')"

**Paso 4: Configurar MT5 (Opcional)**

Para usar las características de integración MT5:

1. Instale MetaTrader 5 desde su broker
2. Asegúrese de que MT5 esté ejecutándose
3. La aplicación detectará automáticamente la instalación

🖥️ **Instalación con Docker**
------------------------------

Para entornos contenerizados o aislamiento completo:

**Construir la Imagen:**

.. code-block:: bash

   # Construir imagen Docker
   docker build -t riskoptima-engine .

**Ejecutar con Docker Compose:**

.. code-block:: bash

   # Ejecutar stack completo
   docker-compose up

**Ejecutar Individualmente:**

.. code-block:: bash

   # Ejecutar solo backend
   docker run -p 8000:8000 riskoptima-engine backend

   # Ejecutar solo frontend
   docker run -p 8501:8501 riskoptima-engine frontend

📁 **Estructura de Archivos Después de la Instalación**
-------------------------------------------------------

Después de una instalación exitosa, debería tener esta estructura:

.. code-block:: text

   risk-optima-engine/
   ├── .venv/                    # Entorno virtual Python (creado por uv)
   ├── target/                   # Archivos de compilación Rust
   ├── src/
   │   ├── lib.rs               # Núcleo cuantitativo en Rust
   │   └── risk_optima_engine/  # Código Python
   │       ├── __init__.py
   │       ├── main.py          # Punto de entrada CLI
   │       ├── backend.py       # API FastAPI
   │       ├── frontend.py      # Interfaz Streamlit
   │       └── mt5_integration.py # Integración MT5
   ├── docs/                    # Documentación
   ├── tests/                   # Tests
   ├── scripts/                 # Scripts de automatización
   ├── pyproject.toml          # Configuración Python
   ├── Cargo.toml              # Configuración Rust
   └── uv.lock                 # Lockfile de dependencias

🔧 **Solución de Problemas de Instalación**
-------------------------------------------

**Problema: "maturin develop" falla**

.. code-block:: bash

   # Asegúrese de tener Visual Studio Build Tools en Windows
   # O build-essential en Linux:
   sudo apt-get install build-essential

   # Reintente:
   uv run maturin develop --release

**Problema: ImportError de la extensión Rust**

.. code-block:: bash

   # Reconstruir extensión
   uv run maturin develop --force

   # Verificar Python path
   uv run python -c "import sys; print(sys.path)"

**Problema: MT5 no se conecta**

- Asegúrese de que MT5 esté ejecutándose
- Verifique que no haya firewall bloqueando conexiones locales
- Intente reiniciar MT5 y la aplicación

**Problema: Puertos ya en uso**

.. code-block:: bash

   # Cambiar puertos si es necesario
   uv run risk-optima-engine backend --port 8001
   uv run risk-optima-engine frontend --server.port 8502

⚡ **Optimizaciones de Rendimiento**
------------------------------------

Para mejores resultados en sistemas potentes:

**Compilación Optimizada:**

.. code-block:: bash

   # Construir con optimizaciones
   uv run maturin develop --release

**Configuración de Memoria:**

.. code-block:: bash

   # Para sistemas con mucha RAM, aumentar límites
   export PYTHON_MAX_MEMORY=8GB  # Ajustar según su sistema

📋 **Verificación Post-Instalación**
-------------------------------------

Ejecute estas pruebas para confirmar que todo funciona:

**Test Básico:**

.. code-block:: bash

   # Probar CLI
   uv run risk-optima-engine --help

   # Probar importación
   uv run python -c "import risk_optima_engine; print('Import successful')"

**Test de Funcionalidad:**

.. code-block:: bash

   # Probar funciones Rust
   uv run python -c "
   from risk_optima_engine import calculate_kelly_criterion, calculate_performance_metrics, Trade
   print('All imports working!')
   "

**Test de MT5 (Opcional):**

.. code-block:: bash

   # Probar conexión MT5
   uv run python -c "
   from risk_optima_engine.mt5_integration import connect_mt5
   success, error = connect_mt5()
   print(f'MT5 Connection: {success}')
   "

🎯 **Próximos Pasos**
---------------------

Después de la instalación exitosa:

1. **Ejecutar la aplicación**: ``uv run risk-optima-engine full``
2. **Acceder a la interfaz**: http://localhost:8501
3. **Cargar datos de ejemplo**: Use ``example_mt5_data.csv``
4. **Leer la documentación**: Ver :doc:`quickstart` para comenzar

📞 **Soporte**
--------------

Si tiene problemas durante la instalación:

- Verifique los :doc:`troubleshooting`
- Abra un issue en GitHub: https://github.com/MamuiPortafoliosCO/kelly-risk-managment/issues
- Incluya la salida completa de error y su configuración del sistema

---

¡Felicitaciones! RiskOptima Engine está ahora instalado y listo para usar.