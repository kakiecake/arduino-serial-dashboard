# Requirements

- *python*
- *pipenv* for dependency managment
- *node* and *npm* (pnpm or yarn) for *tailwindcss* to work

# Installation

```bash
# Installs python dependencies
pipenv install
# Install tailwindcss and prettier locally (may be installed globally if needed)
npm install
```

# Development

To run a python server use *uvicorn*

```bash
uvicorn main:app --reload
```

For tailwindcss to work use npm scripts

```bash
npx tailwind:watch
```

# Building and running

To build the app first compile tailwind to css, then run the app using uvicorn

```bash
npx tailwind:build
uvicorn main:app
```
