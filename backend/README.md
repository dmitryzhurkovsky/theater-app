# Theater-app Backend part

## Local development

### Install dependencies

```shell
cd backend/
poetry shell
poetry install
```

### Install pre-commit hooks

```shell
poetry run pre-commit install
poetry run pre-commit autoupdate
pre-commit install
```

## Docker development

### Preparations
1. Copy `.env.example` file to `.env.dev` and fill it with your environment variables or ask backend devs to share this
file with you.
2. Run `make build` command from `backend` folder. This will create docker image for backend part of the app.

### Running

From `backend` folder run `make up` command. It will up 3 containers: `theater_db`, `theater_api`, `theater_migration`. \
`theater_migration` container will run migrations for database and then shut down.


## Migrations
To generate new migration from `backend` folder run `make migrate` command - it will generate new migration file in
`backend/migrations/versions` folder.

> [!WARNING] \
> **IMPORTANT**: after generate migration please adjust it by yourself since sometimes alembic creates wrong ones!

Once migration is created and adjusted to apply it to database just run `make up` command and `theater_migration` container
will apply new migration to you database.

If you want to manually **upgrade** or **downgrade** migration run `make upgrade` ot `make downgrade` commands from `backend`
folder. Make sure that `theater_db` container is running!
