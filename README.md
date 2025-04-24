# Kernreaktor Worker

> [!IMPORTANT]
> The Kernreaktor Worker is the local executable belonging to the Kernreaktor Repo. [github.com/Arian-Ott/kernreaktor](https://github.com/Arian-Ott/kernreaktor).

## What is `Kernreaktor Worker`?

The Kernreaktor Worker is a small compiled Python program which acts as a secure, local automation agent in a Proxmox-based cluster environment. It enables centralised orchestration and monitoring by communicating with both internal Proxmox APIs and external control services.

The Worker is intentionally designed to be:

- 🔐 **Security-focused** – never stores unencrypted secrets on disk
- 📦 **Minimal** – no dependencies beyond a compiled executable and a config file
- 🚀 **Portable** – runs on any Linux system without a Python runtime

## Architecture

During the development of [kernreaktor](https://github.com/Arian-Ott/kernreaktor) I quickly discorvered a major attack vector which has to me mitigated in early stages.

Any agent with the ability to monitor and control a Proxmox cluster must be treated as a high-value target and secured accordingly.

This section explains the thought process behind this architecture.



### Hypothetical Setup

Imagine a typical Proxmox setup with three nodes:
- Node A and Node B are always online.
- Node C is normally powered off and only activated via Wake-on-LAN.

A single node (e.g. Node A) runs the Kernreaktor Worker, which:
- Periodically collects system load and health data from all nodes
- Sends this data to the Kernreaktor API (hosted locally)
- May later execute migration or scheduling tasks based on API responses

### Local Network Setup

The Kernreaktor API runs inside a Linux container (LXC) on the Proxmox cluster.
For clarity, we refer to this LXC as the “Kernreaktor Container”.

Importantly:

- The Kernreaktor Container has no internet access
- It is behind the DMZ, accessible only from within the trusted Proxmox LAN

```txt
[Internet]
   │
   ▼
[Router] <---> [Proxmox Cluster]
                     ├── Node A (Worker)
                     ├── Node B
                        └── Kernreaktor Container (LXC)
                     └── Node C (offline, WoL)
```


Because the Kernreaktor API is isolated from the internet, it is:

- Protected from external attacks
- Not reachable via public interfaces
- Considered part of the trusted internal infrastructure

This makes it a trusted backend service, safe from typical web-facing API vulnerabilities, and suitable for receiving direct control signals from the internal Worker process.

### Scenario: Kernreaktor API Hosted Externally

In this setup, the **Kernreaktor API** is hosted on a **remote server accessible via the internet**, instead of being located within the Proxmox cluster. This enables cloud-based orchestration and monitoring — but it also introduces a critical security concern:
>[!CAUTION]
>**If an attacker can intercept or forge communication with the API, they could gain control over the entire Proxmox cluster.**
>
>At this stage attackers can comporomise **in the worst case** the entire home network including all proxmox services which can be a risk when work devices share the same network.

---

#### Security Challenge

**Why is this dangerous?**

Because the API has the authority to:

- Trigger VM or LXC migrations
- Power on/off Proxmox nodes
- Influence the internal load-balancing and scheduling logic

A breach in API security could result in:

- Unauthorised infrastructure control
- Downtime or denial of service
- Potential data exposure or loss
- Compromise of internal networks (which can be used by adversaries for designing new attacks)

#### Mitigation Strategy

To address this, a multi-layered **zero-trust** security model is implemented:

##### 1. Outbound-Only Communication

- The **Worker always initiates the connection**
- The API **never pushes commands** to the Worker
- No incoming ports need to be open on Proxmox nodes
- Prevents exposure of internal services to the public

##### 2. Elliptic Curve Encryption (ECIES)

- Sensitive payloads are encrypted at the application level before transit
- Uses **Curve25519** or equivalent
- The API’s public key is pre-shared with each Worker
- The Worker encrypts each message using **ECIES** before transmission

##### 3. Unique Keypair Per Worker

- Every Worker has its own **private/public keypair**
- Keys are stored only on the Worker node
- API uses public keys to verify authenticity
- Prevents impersonation and MITM attacks

##### 4. Data Anonymisation

- Information is anonymised before being stored in the API database
- Hostnames, IP addresses, and node identifiers are hashed or pseudonymised
- Makes the database useless to attackers even if breached

#####  5. JWT Authentication with Expiry

- Workers authenticate using **JWTs**
- Tokens are:
  - Signed using `HS512` or `ES256`
  - Short-lived (e.g., valid for 5–10 minutes)
- Ensures stateless, time-bound access control

##### 6. Redis-Based Session Control

- Session and token validation is managed using **Redis**
- Tokens and challenge responses are stored with short TTLs
- Prevents reuse of expired or intercepted credentials

##### 7. Rate Limiting and Abuse Detection

- API requests are rate-limited per Worker
- Repeated invalid attempts result in:
- Protects against brute-force and denial-of-service attacks


### Why so much work?

Adversaries may have a huge interest in infiltrating the Kernreaktor API since it manages an entire Proxmox cluster. In a home lab scenario this is **partially** neglectable, as there are not mission critical systems running. 

## 💡 Note on VMWare to Proxmox Migration Trends

In recent times, with changes to VMware’s licensing model, more and more users across various online forums and communities have reported migrating entire server infrastructures from VMware to Proxmox.

While I cannot personally verify the full extent or impact of VMware’s licensing changes, nor do I claim that one hypervisor is inherently better than another, I found the following resources relevant and informative:

- 📄 [QLOS Blog: Changes in VMware Licensing – Is it Time to Migrate to Proxmox?](https://qlos.com/en/changes-in-vmware-licensing-is-it-time-to-migrate-to-proxmox)
- 🧵 [Reddit Sysadmin Discussion – Migrating from VMware to Proxmox](https://www.reddit.com/r/sysadmin/comments/1j3lbgj/to_those_who_successfully_migrated_vmware_to/?utm_source=chatgpt.com&rdt=56706)
- 📰 [CIO.com: VMware Licensing and Pricing Hikes – What Options Do You Have?](https://www.cio.com/article/2513389/vmware-licensing-and-pricing-hikes-what-options-do-you-have.html)

---

> _This project started as a personal homelab experiment. It's not intended as a universal solution or an endorsement of any specific platform. My focus is on creating a lightweight, secure setup that allows me to sleep well at night — knowing that basic infrastructure security has been thoughtfully addressed._

---
