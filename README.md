# DeviceProblemNotificationService


### Technology stack

- Python 3.10
- Fastapi
- SqlAlchemy

### Project description

### Run project

In your system must be installed poetry (it's package manager like pip)

```poetry install```

Next time you need start ./dpns/main.py

### Db migrations by alembic

Make  migration:

```alembic revision --autogenerate -m 'migration_name'```

Upgrade migration

```alembic upgrade head```


### Generation changelog

create new git tag
```git tag v0.1.0```

push tags
```git push origin --tags```

generate changelog
```git cliff --config cliff.toml --output CHANGELOG.md```