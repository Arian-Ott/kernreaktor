# CONTRIBUTING to Kernreaktor

First off, thank you for considering contributing to Kernreaktor.  
Your support helps build a better, smarter cluster orchestration system for everyone.

---

## How to Contribute

1. Fork the Repository  
Click on the "Fork" button at the top of the repository page.
2. Clone Your Fork Locally  
Run the following commands:  
```bash
git clone https://github.com/your-username/kernreaktor.git  
cd kernreaktor
```
3. Create a New Branch  
Always branch off from dev:
```basb
git checkout dev  
git checkout -b feature/your-feature-name
```
Use meaningful branch names like:  
- feature/mqtt-improvements  
- feature/decision-engine  
- bugfix/telemetry-timeout
4. Make Your Changes  
- Keep your code clean and modular.  
- Follow the existing code structure and conventions.  
- Write clear and descriptive commit messages.
5. Test Your Changes  
Please test your changes locally before submitting a pull request:  
- Run unit tests where applicable.  
- Manually test using Docker Compose setup (backend, broker, database, daemon).
6. Submit a Pull Request  
- Base branch: dev  
- Compare branch: feature/your-feature-name

In your pull request description:  
- Explain what you changed and why.  
- Mention any issues the PR fixes if applicable.  
- Add any additional notes for reviewers.

---
## Contribution Areas

You are welcome to contribute to:  
- Daemon improvements  
- Backend API features  
- MQTT message handling  
- Database schema improvements  
- Telemetry collection optimisation  
- Decision Engine development  
- Documentation enhancements  
- Docker and deployment optimisations  
- Load testing and simulation tools  
- User interface for future versions
- ... and many more 
---

## Development Guidelines

- Keep functions small and focused.  
- Document any public functions or APIs clearly.  
- Use asynchronous code where appropriate, especially for network operations.  
- Be mindful of performance and scalability.  
- Ensure Docker compatibility (container-first design).

---


## Branching Strategy

- feature/* → Feature development  
- bugfix/* → Bug fixes  
- dev → Integration branch for new features and fixes  
- main → Only stable, production-quality code is merged here after releases

All pull requests must target the dev branch.

---

## Thank You <3

"Kernreaktor is built on collaboration and innovation.  
Your contributions, no matter how small, drive the project forward."
