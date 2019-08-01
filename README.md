# scrapy-boilerplate

This is a boilerblape for new Scrapy projects.

*The project is a WIP, so expect major changes and additions (mostly latter).*

## Features

- Python 3.6+
- [Pipenv](https://github.com/pypa/pipenv) for dependency management
- SQLAlchemy ORM with alembic migrations
- RabbitMQ integrated via [pika](https://github.com/pika/pika/)
- configuration via ENV variables and/or `.env` file
- single file for each class
- code generation scripts for classes: spiders, pipelines, etc. (see [this section](#code-generation))
- [Black](https://github.com/psf/black) to ensure codestyle consistency (see [here](#black))
- Docker-ready (see [here](#docker))
- PM2-ready (see [here](#pm2))

## Installation

To create a new project using this boilerplate, you need to:

1. Clone the repository.
2. Run the installation script: `./install.sh`
3. ???
4. PROFIT!

## Usage

The boilerplate comes with some pre-written classes and helper scripts and functions, which are described in this section.

### Code generation

There is a scrapy command to generate class files and automatically add imports ti `__init__` files. It can be used as follows:

```
scrapy new spider SampleSpider
```

The first argument (`spider`) is a type of class file to be generated, and can be one of the following:

- command
- extension
- item
- middleware
- model
- pipeline
- spider_middleware
- spider

The second argument is class name.

Also for `pipeline` and `spider` class an option `--rabbit` can be used to add RabbitMQ connection code to generated source.


### Docker

The project includes Dockerfiles and docker-compose configuration for running your spiders in containers.

Also, a configuration for default RabbitMQ server is included.

Dockerfiles are located inside the `docker` subdirectory, and the `docker-compose.yml` - at the root of the project. You might want to change the `CMD` of the scrapy container to something more relevant to your project. To do so, edit `docker/scrapy/Dockerfile`.

Docker-compose takes configuration values from ENV. Environment can also be provided by creating a `.env` file at the root of the project (see `.docker_env.example` as a sample). Creating of dotenv for docker is handled in the `install.sh` script by default.

### Black

Black is the uncompromising Python code formatter. It is used in thsi project to ensure code style consistensy in the least intrusive fashion.

Black is included in Pipfile dev-dependencies. A pre-commit hook for running autoformatting is also included, via [pre-commit](https://pre-commit.com) tool. It is installed automatically, if you run `install.sh`. Otherwise, to use it you need to run `pre-commit install` in the root project folder after installing pre-commit itself.

### PM2

This boilerplate contains a sample PM2 config file along with a bash startup script that sets up all the necessary environment to run scrapy with this process manager.

All you need to do, is copy/edit `src/pm2/commands/command_example.sh` and change the `exec` part to the command actually needed to be run, and then create `process.json` ecosystem file (based on `src/pm2/process.example.json`) to start the script.

Then, cd to `src/pm2` and run `pm2 start process.json`.
