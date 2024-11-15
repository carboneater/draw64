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

# Observabité

- Métriques
- Logs
- Traces
- ...
- Erreurs

---

# Draw64: Une belle démo

<Center>
```mermaid
flowchart TD

U([Utilisateur]) <--> S[Server] <--> DB[(DB)]
```
</Center>

---
level: 3
---

# Monitoring

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

# OpenTelemetry

---
layout: two-cols-header
---

# Métriques

::left::

## Hôte

- CPU %
- Mémoire utilisée (%)
- Disque (Stockage) utilisé (%)
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

