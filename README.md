# Requirements

- *python*
- *pipenv* for dependency managment
- *node* and *npm* (pnpm or yarn) for *tailwindcss* to work

# Installation

```bash
# Install python dependencies
pipenv install
# Install tailwindcss and prettier locally (may be installed globally if needed)
npm install
```

# Development

## Without Docker

To run a python server use *uvicorn*
```bash
uvicorn main:app --reload
```

For tailwindcss to work use npm scripts

```bash
npx tailwind:watch
```

## With Docker

First build the image using `docker build`

```bash
docker build -t arduino-web:dev -f Dockerfile.dev .
```

Then run the container, mounting `static`, `templates` and `app` folder, so hot reloading can work

```bash
docker run -it \
	-v $PWD/app:/app/app \
	-v $PWD/static:/app/static \
	-v $PWD/templates:/app/templates \
	-p 8000:80
  arduino-web:dev
```


# Building and running in production

## Without docker

To build the app first compile tailwind to css, then run the app using uvicorn

```bash
npx tailwind:build
uvicorn main:app
```

## With docker

First build the image using `docker build`

```bash
docker build -t arduino-web:prod -f Dockerfile .
```

Then compile the CSS with tailwind
```bash
tailwindcss --output static/compiled.css
```

Run the container

```bash
docker run -d -p 8000:80 arduino-web:prod
```
