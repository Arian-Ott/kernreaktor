# CONTRIBUTING to Kernreaktor

First off, thank you for considering contributing to Kernreaktor.  
Your support helps build a better, smarter cluster orchestration system for everyone.

---

## How to Contribute

**1. Fork the Repository**
Click on the "Fork" button at the top of the repository page.

Create a `virtual env`

```sh
python3 -m venv venv
```

on unix:

```sh
source venv/bin/activate
```

on windows:

```powershell

.\venv\Scripts\Activate.ps1
```

If things go south on windows try following things:


For windows make sure you have the **Visual Studio C++ Build tools** installed.
[Link to MS build tools](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2019)

Also make sure you have rust installed. Since some python libraries are written in rust (e.g. `ruff`), it is required.


**example `.env`**

```conf
# MariaDB configuration
MYSQL_USER=reaktor
MYSQL_PASSWORD=reaktor
MYSQL_ROOT_PASSWORD=root
MYSQL_DATABASE=reaktor
DB_HOST=127.0.0.1 # use "maria" if using docker-compose
DB_PORT=3306
# API configuration
SECRET_KEY=504ebe0a0971fb84d1dc5f02b29412f8ad090c2300272c7d32a601278a6b86ff50238a5641cf7b0cbf15cb05ad5705133f224282949fc7497cd81064b0ae537a
DOCKER=1 # if DOCKER=1 and DEBUG=0, the API will run in a docker container and overwrite the env variables with the docker-compose parameters
DEBUG=0
API_PORT=52345
# MQTT configuration
MQTT_BROKER="mqtt" # use "mqtt" if using docker-compose
```

You can generate a secret using 

```bash
openssl rand -hex 32
```

**2. Clone Your Fork Locally**
Run the following commands:

```bash
git clone https://github.com/your-username/kernreaktor.git  
cd kernreaktor
```

**3. Create a New Branch**  
Always branch off from dev:

```bash
git checkout dev  
git checkout -b feature/your-feature-name
```


**Use meaningful branch names like:**

- feature/mqtt-improvements  
- feature/decision-engine  
- bugfix/telemetry-timeout

**4. Make Your Changes**

- Keep your code clean and modular.  
- Follow the existing code structure and conventions.  
- Write clear and descriptive commit messages.

**5. Test Your Changes**
Please test your changes locally before submitting a pull request:  

- Run unit tests where applicable.  
- Manually test using Docker Compose setup (backend, broker, database, daemon).

**6. Submit a Pull Request**

- Base branch: ``dev`` 
- Compare branch: ``feature/your-feature-name``

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

## Folder Structure

```
.
├── api
│   ├── config 
│   ├── crud 
│   ├── keys
│   ├── models
│   ├── routes
│   ├── schemas
│   └── services
├── docs
│   └── assets
├── mosquitto
│   └── config
└── tests

```
| folder | usage |
|--------|--------|
|api|equivalent to the `/src` folder|
|config | contains `__init__.py` with all the pydantic settings. It ensures that the `.env` file is correct and a large set of environment variables is predetermined |
| crud | All sqlalchemy crud operations. This is used to just interact with the db. |
| keys | Hate it or love it. I personally hate it and an alternative needs to be found. (Maybe you have an idea :) ) Stores the kernreaktor public and private keypair. This is not very secure (i know) but its the fastest thing I could think of before tweaking around with storing two keyfiles |
|models | all sqlalchemy models. |
|routes | All API routes of the FastAPI instance. Each new "file" has an own API prefix. E.g. the user API has `/users` as prefix |
| schemas | All pydantic schemas |
| services | business logic behind the models. It provides the **logic** of the crud operations and basic services used in the project |
|docs | I hope this is self explanatory |
| docs/assets | same as docs |
| mosquitto/config | The configuration for the docker mosquitto service. Inside there, you must specify a `mosquitto.conf` in order to run the MQTT container. |
| tests | Unit tests (where applicaple). It is generally good practice to have tests. We use `pytest` at the time of this writing |



## Thank You <3

"Kernreaktor is built on collaboration and innovation.  
Your contributions, no matter how small, drive the project forward."
