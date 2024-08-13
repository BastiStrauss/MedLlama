# Medical Llama - A medical Q&A Bot
This app is a fine-tuned Llama 3 powered chatbot that can be accessed by a webinterface. It is built to better answer medical inquiries. Always check answers for their correctness.

## Prerequists 
Make sure Docker Desktop and Docker Compose is downloaded on your machine and running.

[Docker](https://www.docker.com/)

## Running the application
The application can be executed with running a cli script. This will start the Docker container. The script needs to be made executable once.
### Making the scipt executable

```bash 
chmod +x start.sh
```
### Starting the app

```bash 
./start.sh
```

### Closing the app
The webinterface can just be closed. To addtiontally shutdown the Docker container the cli can be used.

```bash 
docker-compose down
```

## Copyright
This work is done by Sebastian Strauß for a Bachelor Thesis at the University of Muenster. It is provided under the MIT license.

[GitHub](https://github.com/BastiStrauss)

