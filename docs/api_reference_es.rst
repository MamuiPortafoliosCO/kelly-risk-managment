Referencia de API - RiskOptima Engine
=====================================

Esta documentación describe la API REST completa de RiskOptima Engine, incluyendo todos los endpoints, parámetros y respuestas.

🏗️ **Información General de la API**
-------------------------------------

**URL Base:**
``http://localhost:8000/api/v1``

**Autenticación:**
No requerida (aplicación local)

**Formato de Datos:**
JSON para requests/responses

**Rate Limiting:**
100 requests por minuto global

**Versionado:**
API versionada con ``/v1/`` prefix

📋 **Códigos de Estado HTTP**
-----------------------------

- **200 OK**: Solicitud exitosa
- **400 Bad Request**: Datos inválidos o parámetros faltantes
- **404 Not Found**: Recurso no encontrado
- **500 Internal Server Error**: Error del servidor

🔧 **Endpoints de Carga de Datos**
----------------------------------

**POST /upload/trade-history**

Carga y valida archivos de historial de trading de MT5.

**Parámetros:**

.. code-block:: json

   {
     "format": "csv | xml",
     "file": "multipart/form-data file"
   }

**Respuesta Exitosa (200):**

.. code-block:: json

   {
     "file_id": "uuid-string",
     "status": "success",
     "message": "Successfully uploaded 150 trades"
   }

**Errores Comunes:**

- **400**: Formato no soportado o archivo inválido
- **500**: Error de procesamiento del archivo

**GET /upload/status/{file_id}**

Verifica el estado de un archivo cargado.

**Respuesta (200):**

.. code-block:: json

   {
     "status": "ready | processing | failed",
     "progress": 1.0,
     "errors": []
   }

📊 **Endpoints de Análisis**
----------------------------

**POST /analysis/performance**

Calcula métricas completas de rendimiento desde datos de trading.

**Parámetros:**

.. code-block:: json

   {
     "file_id": "uuid-string",
     "parameters": {
       "include_sharpe": true,
       "risk_free_rate": 0.02
     }
   }

**Respuesta Exitosa (200):**

.. code-block:: json

   {
     "kpis": {
       "total_trades": 150,
       "win_probability": 0.62,
       "loss_probability": 0.38,
       "avg_win": 45.50,
       "avg_loss": -28.75,
       "win_loss_ratio": 1.58,
       "profit_factor": 1.85,
       "expectancy": 12.45,
       "max_drawdown": -1250.00,
       "sharpe_ratio": 1.23
     },
     "equity_curve": [10000.0, 10125.5, 10087.2, ...],
     "status": "success"
   }

**POST /analysis/kelly**

Calcula la fracción óptima de Kelly.

**Parámetros:**

.. code-block:: json

   {
     "performance_data": {
       "win_probability": 0.62,
       "win_loss_ratio": 1.58
     },
     "fractional_multiplier": 0.5
   }

**Respuesta Exitosa (200):**

.. code-block:: json

   {
     "optimal_fraction": 0.078,
     "warnings": [
       "Consider using fractional Kelly for reduced volatility"
     ]
   }

**POST /analysis/optimal-f**

Calcula el tamaño óptimo de posición usando Óptimo F.

**Parámetros:**

.. code-block:: json

   {
     "trade_data": [
       {
         "symbol": "EURUSD",
         "trade_type": "Buy",
         "volume": 0.1,
         "open_price": 1.0850,
         "close_price": 1.0900,
         "profit": 50.0,
         "commission": 0.5,
         "swap": 0.0
       }
     ],
     "parameters": {}
   }

**Respuesta Exitosa (200):**

.. code-block:: json

   {
     "optimal_f": 0.025,
     "twr": 1.125,
     "sensitivity": {
       "parameter_variation": 0.01,
       "impact": 0.005
     }
   }

🎯 **Endpoints de Optimización**
---------------------------------

**POST /optimization/challenge**

Ejecuta optimización Monte Carlo para desafíos de prop firms.

**Parámetros:**

.. code-block:: json

   {
     "challenge_params": {
       "account_size": 100000.0,
       "profit_target_percent": 10.0,
       "max_daily_loss_percent": 5.0,
       "max_overall_loss_percent": 10.0,
       "min_trading_days": 30
     },
     "trade_data": [...],  // Array de operaciones
     "simulation_count": 1000
   }

**Respuesta Exitosa (200):**

.. code-block:: json

   {
     "recommended_fraction": 0.015,
     "pass_rate": 0.78,
     "confidence_interval": [0.75, 0.81],
     "status": "success"
   }

**GET /optimization/status/{task_id}**

Verifica el progreso de una tarea de optimización asíncrona.

**Respuesta (200):**

.. code-block:: json

   {
     "status": "running | completed | failed",
     "progress": 0.65,
     "eta": "2 minutes remaining",
     "result": {...}  // Solo si completado
   }

🔗 **Endpoints de MT5**
-----------------------

**POST /mt5/connect**

Establece conexión con terminal MT5.

**Parámetros:**

.. code-block:: json

   {
     "timeout": 30
   }

**Respuesta Exitosa (200):**

.. code-block:: json

   {
     "connected": true,
     "account_info": {
       "balance": 10000.0,
       "equity": 9850.0,
       "margin": 150.0
     }
   }

**GET /mt5/account-info**

Obtiene información actual de la cuenta MT5.

**Respuesta (200):**

.. code-block:: json

   {
     "balance": 10000.0,
     "equity": 9850.0,
     "margin": 150.0,
     "margin_free": 9700.0,
     "margin_level": 657.0,
     "profit": -150.0,
     "leverage": 100,
     "currency": "USD"
   }

**POST /mt5/disconnect**

Desconecta de MT5.

**Respuesta (200):**

.. code-block:: json

   {
     "success": true
   }

📄 **Endpoints de Reportes**
----------------------------

**POST /reports/generate**

Genera reportes de análisis.

**Parámetros:**

.. code-block:: json

   {
     "report_type": "performance_analysis | risk_optimization | comprehensive",
     "data": {...},  // Datos de análisis
     "format": "pdf | csv"
   }

**Respuesta Exitosa (200):**

.. code-block:: json

   {
     "report_id": "uuid-string",
     "download_url": "/api/v1/reports/download/uuid-string",
     "status": "generating"
   }

**GET /reports/download/{report_id}**

Descarga un reporte generado.

**Respuesta (200):**
Archivo PDF o CSV

⚠️ **Manejo de Errores**
-----------------------

**Formato Estándar de Error:**

.. code-block:: json

   {
     "error": {
       "code": "VALIDATION_ERROR | PROCESSING_ERROR | MT5_ERROR",
       "message": "Descripción del error",
       "details": {
         "field": "campo_específico",
         "value": "valor_problemático",
         "suggestion": "cómo_arreglarlo"
       }
     }
   }

**Códigos de Error Comunes:**

- **VALIDATION_ERROR**: Datos inválidos o parámetros faltantes
- **FILE_NOT_FOUND**: Archivo no encontrado o expirado
- **MT5_CONNECTION_ERROR**: Problemas de conexión con MT5
- **PROCESSING_ERROR**: Error interno durante cálculos
- **RATE_LIMIT_EXCEEDED**: Demasiadas solicitudes

🔒 **Consideraciones de Seguridad**
-----------------------------------

**Contexto Local:**
- API diseñada únicamente para uso local
- No implementa autenticación (por diseño)
- Comunicación segura vía localhost

**Validación de Datos:**
- Validación estricta de todos los inputs
- Sanitización de datos de archivos
- Límites de tamaño de archivos y rate limiting

**Privacidad:**
- Ningún dato sale del equipo local
- Archivos temporales eliminados automáticamente
- No logging de datos sensibles

📊 **Ejemplos de Uso con cURL**
-------------------------------

**Cargar archivo de trading:**

.. code-block:: bash

   curl -X POST "http://localhost:8000/api/v1/upload/trade-history" \
        -F "file=@trades.csv" \
        -F "format=csv"

**Analizar rendimiento:**

.. code-block:: bash

   curl -X POST "http://localhost:8000/api/v1/analysis/performance" \
        -H "Content-Type: application/json" \
        -d '{"file_id": "your-file-id"}'

**Optimizar desafío:**

.. code-block:: bash

   curl -X POST "http://localhost:8000/api/v1/optimization/challenge" \
        -H "Content-Type: application/json" \
        -d '{
          "challenge_params": {
            "account_size": 100000,
            "profit_target_percent": 10,
            "max_daily_loss_percent": 5,
            "max_overall_loss_percent": 10,
            "min_trading_days": 30
          },
          "trade_data": [...],
          "simulation_count": 1000
        }'

**Conectar MT5:**

.. code-block:: bash

   curl -X POST "http://localhost:8000/api/v1/mt5/connect" \
        -H "Content-Type: application/json" \
        -d '{"timeout": 30}'

🔧 **Integración Programática**
--------------------------------

**Python con requests:**

.. code-block:: python

   import requests

   # Cargar archivo
   with open('trades.csv', 'rb') as f:
       response = requests.post(
           'http://localhost:8000/api/v1/upload/trade-history',
           files={'file': f},
           data={'format': 'csv'}
       )
       file_id = response.json()['file_id']

   # Analizar rendimiento
   analysis = requests.post(
       'http://localhost:8000/api/v1/analysis/performance',
       json={'file_id': file_id}
   ).json()

**JavaScript/Node.js:**

.. code-block:: javascript

   const axios = require('axios');
   const FormData = require('form-data');
   const fs = require('fs');

   // Cargar archivo
   const form = new FormData();
   form.append('file', fs.createReadStream('trades.csv'));
   form.append('format', 'csv');

   const uploadResponse = await axios.post(
       'http://localhost:8000/api/v1/upload/trade-history',
       form,
       { headers: form.getHeaders() }
   );

   // Analizar
   const analysisResponse = await axios.post(
       'http://localhost:8000/api/v1/analysis/performance',
       { file_id: uploadResponse.data.file_id }
   );

📈 **Monitoreo y Logging**
---------------------------

**Logs de API:**
- Todos los requests/responses se loggean
- Errores incluyen stack traces completos
- Logs rotan automáticamente

**Métricas de Rendimiento:**
- Latencia de respuesta por endpoint
- Tasa de error por endpoint
- Uso de recursos del sistema

**Health Checks:**
- Endpoint ``GET /health`` para verificación de estado
- Verificación automática de componentes críticos

🔄 **Versionado y Compatibilidad**
-----------------------------------

**Versionado Semántico:**
- **MAJOR**: Cambios incompatibles
- **MINOR**: Nuevas características (retrocompatibles)
- **PATCH**: Bug fixes (retrocompatibles)

**Política de Deprecación:**
- Funcionalidades obsoletas se marcan como deprecated
- Periodo de transición de 2 versiones
- Documentación clara de migración

**Compatibilidad:**
- Cliente debe especificar versión de API
- Respuestas incluyen versión del servidor
- Validación estricta de versiones incompatibles

---

**¿Necesita ayuda con la integración?**

- Documentación completa: https://riskoptima-engine.readthedocs.io/
- Ejemplos de código: ``examples/`` directory
- Soporte: https://github.com/MamuiPortafoliosCO/kelly-risk-managment/issues

La API está diseñada para ser intuitiva y completa. Para casos de uso avanzados, considere revisar los ejemplos incluidos en el repositorio.