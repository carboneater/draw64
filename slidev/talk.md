---
hideInToc: true
title: O11y 101 w/ OTel
---

# Observability 101

## Avec OpenTelemetry!

---
hideInToc: true
---

<Toc />

---
layout: two-cols-header
---

# Draw64: Une belle démo
::left::
<Center>
```mermaid
flowchart TD

U([Utilisateur]) <--> S[Server] <--> DB[(DB)]
```
</Center>
::right::
<ul>
    <v-click><li>High-Availability</li></v-click>
    <v-click><li>Auto-Scaling</li></v-click>
    <v-click><li>Rolling Releases</li></v-click>
    <v-click><li>Continuous Deployment</li></v-click>
</ul>

::bottom::

<v-click><center>Bref, c'est _lourd_ à gérer</center></v-click>

---
level: 3
---

# Monitoring: Healthchecks

<Center>
```mermaid
flowchart TD

U([Utilisateur]) <--> S[Server] <--> DB[(DB)]
H([HealthChecks]) -.-> S & DB
```
</Center>

---
level: 2
---

# High-Availability?

<Center>
```mermaid
flowchart TD

U([Utilisateur]) <--> LB[Load Balancer] <-.-> S1[Server 1] & S2[Server 2] <-.-> DB[(DB)]
```

(Le cluster de DB non-unique est laissé en exercice au lecteur)
</Center>

---
level: 3
---

# HA: Monitoring

<Center>
```mermaid
flowchart TD

U([Utilisateur]) x--x LB[Load Balancer] x--x S1[Server 1] & S2[Server 2] x--x DB[(DB)]
H([Healthchecks]) -.-> LB & S1 & S2 & DB
```
</Center>

---
layout: two-cols-header
level: 2
---

# Healthchecks

<Center>On a seulement des healthchecks</Center>

::left::

## Healthchecks

Est-ce que mon service est fonctionnel?

::right::

## Monitoring

**Comment** va mon service?

---
layout: two-cols-header
---

# Observabité

::left::
## Signaux communs

- Métriques
- Logs
- Traces

::right::
## Moins communs

- Erreurs
- Profiling
- Real User Monitoring (RUM)
- ...

---
layout: section
---

# OpenTelemetry

---

# OpenTelemetry: Un peu d'histoire

<center><img src="https://miro.medium.com/v2/resize:fit:1330/format:webp/1*Olh4hJc_m4ZkU43I8t7s5w.png"/></center>

<center>Source: https://medium.com/opentracing/merging-opentracing-and-opencensus-f0fe9c7ca6f0</center>

---

# OpenTelemetry: Un Standard Unique?

<center><img src="https://imgs.xkcd.com/comics/standards.png"/></center>

<center>Source: XKCD, https://xkcd.com/927/</center>

---

# OpenTelemetry

<center><img src="https://camo.githubusercontent.com/d0abb415b6f5ccb9f1c9df324ceddec0094cb97a0f79b7a62d3b6d9ac4282d67/68747470733a2f2f6f70656e74656c656d657472792e696f2f696d672f6c6f676f732f6f70656e74656c656d657472792d686f72697a6f6e74616c2d636f6c6f722e737667"/></center>

<center>Source: OpenTelemetry, https://github.com/open-telemetry</center>

---

# OpenTelemetry
- ...
- IO/s

::right::

## Service

- Nombre de requêtes
- durée des requêtes
- Nombre d'erreurs
- ...

---
level: 2
---

# Centraliser les métriques

---

# Instrumentation Automatique: Trouver les packages existats

```sh
uv add --dev opentelemetry-bootstrap
```
```sh
opentelemetry-bootstrap
```

> opentelemetry-instrumentation-asyncio==0.49b2  
> opentelemetry-instrumentation-dbapi==0.49b2  
> opentelemetry-instrumentation-logging==0.49b2  
> opentelemetry-instrumentation-sqlite3==0.49b2  
> opentelemetry-instrumentation-threading==0.49b2  
> opentelemetry-instrumentation-urllib==0.49b2  
> opentelemetry-instrumentation-wsgi==0.49b2  
> opentelemetry-instrumentation-asgi==0.49b2  
> opentelemetry-instrumentation-fastapi==0.49b2  
> opentelemetry-instrumentation-httpx==0.49b2  
> opentelemetry-instrumentation-jinja2==0.49b2  
> opentelemetry-instrumentation-starlette==0.49b2  
> opentelemetry-instrumentation-system-metrics==0.49b2  
> opentelemetry-instrumentation-tortoiseorm==0.49b2

---

# Instrumentation Automatique: Installation

```sh
uv add opentelemetry-instrumentation-asyncio opentelemetry-instrumentation-dbapi \
opentelemetry-instrumentation-logging opentelemetry-instrumentation-sqlite3 \
opentelemetry-instrumentation-threading opentelemetry-instrumentation-urllib \
opentelemetry-instrumentation-wsgi opentelemetry-instrumentation-asgi \
opentelemetry-instrumentation-fastapi opentelemetry-instrumentation-httpx \
opentelemetry-instrumentation-jinja2 opentelemetry-instrumentation-starlette \
opentelemetry-instrumentation-system-metrics opentelemetry-instrumentation-tortoiseorm
```

---

# Instrumentation Automatique: Exécution

```sh
OTEL_SERVICE_NAME=draw64 \
OTEL_TRACES_EXPORTER=console \
OTEL_METRICS_EXPORTER=prometheus \
opentelemetry-instrument fastapi run draw64/app.py
```

---

# Instrumentation automatique: Système

```sh
uv add opentelemetry-instrumentation-system-metrics
```

```python {*|5|6}
from opentelemetry.metrics import set_meter_provider
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import ConsoleMetricExporter, PeriodicExportingMetricReader

set_meter_provider(MeterProvider(PeriodicExportingMetricReader(ConsoleMetricExporter())))
SystemMetricsInstrumentor().instrument()
```


---
level: 2
---

# Instrumentation - Métriques - Exportation

```sh
uv add opentelemetry-exporter-prometheus
```

```diff
+from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.metrics import set_meter_provider
from opentelemetry.sdk.metrics import MeterProvider
-from opentelemetry.sdk.metrics.export import ConsoleMetricExporter, PeriodicExportingMetricReader
+from opentelemetry.sdk.resources import SERVICE_NAME, Resource
+from prometheus_client import start_http_server

+set_meter_provider(
+    MeterProvider(
+        metric_readers=[PrometheusMetricReader()],
+        resource=Resource(
+            attributes={
+                SERVICE_NAME: "Draw64",
+            }
+        ),
+    )
+)
-set_meter_provider(MeterProvider(PeriodicExportingMetricReader(ConsoleMetricExporter())))
SystemMetricsInstrumentor().instrument()

# ...

+start_http_server(port=9464)
```

---

# Instrumentation automatique: FastAPI

```sh
uv add opentelemetry-instrumentation-fastapi
```

```python {*|2,8}
from fastapi import FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
# ...

app = FastAPI()
# ...

FastAPIInstrumentor.instrument_app(app)
```