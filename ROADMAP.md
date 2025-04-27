# Kernreaktor Project Roadmap

---

## Overview

Kernreaktor is a distributed, lightweight orchestration system designed to manage Proxmox clusters and similar virtualised environments.  
It provides dynamic node load balancing, intelligent action execution, and future support for multi-cluster scaling.

The project is built using containerised components from the ground up, ensuring portability, scalability, and ease of deployment.

---

## Version Roadmap

### v0.1.0 – Core Communication Working

- Daemon container sends telemetry (system load, VM statistics) to the MQTT Broker.
- Backend container receives telemetry and saves it into MariaDB.
- Backend sends basic action commands to the Daemon:
  - Shutdown node (sleep mode)
  - Wake node (Wake-on-LAN or other mechanisms)
  - Migrate VM or LXC
  - Scale VM or LXC (CPU/RAM adjustments)
- Daemon container executes native Proxmox shell commands where applicable.
- For non-Proxmox nodes, the Daemon executes prepared local shell scripts.
- Docker Compose setup (Backend, Database, MQTT Broker, Daemon).
- Load Testing Simulation Script (simulating 2048 nodes).
- Internal system tests for stability.

---

### v0.2.0 – Storage Optimisation and Telemetry Improvements

- Add optional InfluxDB container for scalable telemetry storage.
- Separate telemetry data from user authentication and actions data.
- Basic Grafana dashboard container (optional) for telemetry visualisation.
- Introduce telemetry querying endpoints in the Backend API.

---

### v0.3.0 – First Decision Engine

- Backend analyses telemetry data (CPU usage, memory load, disk I/O).
- Backend makes dynamic decisions:
  - Move overloaded VMs to less loaded nodes.
  - Shutdown underutilised nodes to save power.
  - Wake nodes when cluster capacity is under pressure.
- Basic strategy framework implemented (thresholds, escalation rules).
- Actions are triggered automatically without human intervention.

---

### v0.4.0 – Daemon Auto-Replication

- Daemon containers monitor their own workload and telemetry queue sizes.
- When overloaded, a Daemon requests the spawning of a sibling instance.
- Nodes are dynamically split between Daemon containers to balance load.
- Node ownership tracking and dynamic rebalancing.

---

### v1.0.0 – Public Release: Homelab and Small Enterprise Ready

- Fully containerised deployment via Docker Compose.
- Hardened error handling and operational safety measures.
- Secure Daemon container operation (timeouts, command sandboxing).
- Multi-cluster support finalised and tested.
- First public community release.

---

## Development Branching Strategy

- `feature/*` → Individual features developed in isolation.
- `dev` → Feature branches merged here for integration and testing.
- `main` → Only stable, production-quality versions are merged here.
- Tags (e.g., `v0.1.0`, `v0.2.0`) are created on the `main` branch after successful releases.

---

## Notes

- v0.1.0 focuses purely on establishing reliable telemetry flow and executing defined system actions.
- The intelligent Decision Engine will be introduced in v0.3.0 once the system has matured.
- Non-Proxmox platforms will be supported via administrator-defined shell scripts, executed locally inside the Daemon container.

---

# Final Summary

> “Kernreaktor is built to first observe, then act, then scale — ensuring each phase of capability is proven before advancing to the next, with all components containerised for maximum flexibility.”
