## Installation

```bash
git clone https://github.com/bird-exchange/worker.git
```

## Running

### One-time action (if not poetry)

```bash
pip install poetry
poetry config virtualenvs.in-project true
```

### Install dependecies

```bash
poetry init
poetry install
```

### Configure environment

Use `.env.default` to create `.env`

### Start application
```bash
make app.run
```
