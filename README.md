# Kernreaktor

**Kernreaktor** _(nuclear reactor, pronounced as_ `[ˈkɛrnʁeˌʔaktoːɐ̯]` _or if you prefer English_ `[ˈkɜːn.riːˌæk.tɔː]`) is an open source project attempting to manage the load of Proxmox nodes. In every Proxmox homelab one encounters the challenge that there are many containers running with low resources but no intelligent coordination between them. These idle LXC containers or underutilized VMs consume baseline system capacity without contributing to meaningful workloads.

Kernreaktor tackles this by introducing centralised logic for dynamic resource management and load-aware orchestration. Its key use case is to monitor the current system state of all connected Proxmox nodes and:

- Limit resources (CPU shares, memory, disk I/O) of containers and VMs that show persistently low load, thereby freeing up system performance for other tasks.

- Detect spikes or workload surges on any instance in real time and respond by automatically migrating the stressed VM or container to a node classified as high performance.

- Apply different strategies based on administrator-defined criteria: e.g., memory pressure, I/O wait, CPU steal time, or queue lengths.

This allows homelab admins to tune their cluster to react like an autonomous power grid — always adapting to where energy (in this case, compute power) is needed most.

## Motivation

With the beginning of my Business Informatics degree, I started building my own homelab. As of today it consists of one MSI Cubi5 with an Intel core i7 (12 CPU cores). It is obvious that having a proxmox setup with **one** node represented by a mini pc is not sufficient for high performance computing tasks. Hence, I bought a used **HPE ProLiant DL360 Gen9** for high performance tasks (e.g. CI/CD automations, intensive calculations and what not).

This beast houses an insane 14-Core Intel Xenon with 2.4 GHz, 32 GB DDR4 RAM and 2x 300 GB HDD which are all cooled by 7 fans and powered by a 500 W power supply (though it uses only 300 W).

For a homelab this setup is definetely overkill. Especially considering the jump from a "little" MSI Cubi5 to a full data centre graded high performance server.

In the past I needed for some projects a high computational power to complete them. A prominent example was my first semester thesis about Retrieval Augmented Generation (RAG) where I built a complete data pipeline including a Vector Database, a Document DB and a massive load of text data (including excerpts of the German common law and the whole ring cycle of Wagner). Just processing and embedding the text files was painful, as the mini PC came at its limits.

With the server I ordered solving those problems will be much easier in the future.

**However there is one <u>_big_</u> limitation**

Electrical power.

Obviously, I can't run this server 24/7 with its 300W power consumption.

I have to design a system which automatically spins up the HP server when needed.
