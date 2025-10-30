


# aeneas-docker

[Aeneas](https://www.readbeyond.it/aeneas/) automatically generates a synchronization map between a list of text fragments and an audio file containing the narration of the text. In computer science this task is known as (automatically computing a) forced alignment.

## Running
First download docker and docker-compose.
Second download the code.
Then run the aeneas docker use the following.

```bash
sudo docker-compose up
```

## Usage

Run without arguments to get the usage message:

```bash
 sudo docker-compose run aeneas python3 -m aeneas.tools.execute_task
 sudo docker-compose run aeneas python3 -m aeneas.tools.execute_job

```
You can also get a list of live examples that you can immediately run on your machine thanks to the included files:

```bash
 sudo docker-compose run aeneas python3 -m aeneas.tools.execute_task \
   test.mp3 \
   test1.txt \
   "task_language=eng|os_task_file_format=json|is_text_type=plain" \
   map.json .

```



```bash
 sudo docker-compose run aeneas python3 -m aeneas.tools.execute_task test.mp3 test1.txt "task_language=eng|os_task_file_format=json|is_text_type=plain" map1.json .

```

## Deploying to Heroku

This repository now includes everything required to deploy the Aeneas API to [Heroku](https://www.heroku.com/) using the container registry.

1. Install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli#install-the-heroku-cli) and sign in.
2. Create a new Heroku application:

   ```bash
   heroku create your-app-name
   ```

3. Enable container builds for the application:

   ```bash
   heroku stack:set container -a your-app-name
   ```

4. Push the repository to Heroku. The provided `heroku.yml` instructs Heroku to build from the included `Dockerfile`:

   ```bash
   git push heroku main
   ```

5. Once the build finishes, scale the web process if it is not already running:

   ```bash
   heroku ps:scale web=1 -a your-app-name
   ```

### API endpoints

The container exposes a small Flask API:

* `GET /health` – Health check endpoint.
* `POST /align` – Accepts multipart form-data with `audio` and `text` file uploads and an optional `config` field. It runs `aeneas` inside the container and returns the generated synchronization map.

The application listens on the port defined by the `PORT` environment variable (default `5000`) which is compatible with Heroku's routing stack.

## License
[GNU AFFERO GENERAL PUBLIC LICENSE](https://github.com/oyekamal/aeneas-Docker/blob/main/LICENSE)
