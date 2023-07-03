# File Operations API
- Based on `Python 3.8.10` and `pip 20.0.2`

## Features
- Implements three endpoints:
    - Search Files
    - Download Files
    - Move and Rename files
- Configurable base folder where the endpoints will look for files
- Error and Edge Case handling
- Separation of settings files according to environment
- Unit tests
- Dockerized
- Formatted using PEP 8 standard
- Contains a test folder with other test folders and files for easy manual testing

## How to run
- Recommended to use the Docker way due to ease of use and more error-prone experience. It can also be restarted in order to reset testing folder structure.
- The assumption is that the name of the folder where the project files are located is called "fileoperations"

### Standard way

This was developed on Ubuntu Linux and the following steps describe how to run this on that platform. 
```
1. sudo apt-get update
2. sudo apt-get install python3-venv
3. cd /fileoperations
4. pip install -r requirements.txt
5. cp fileoperations/settings/select_sample.py fileoperations/settings/select.py
6. cp fileoperations/settings/secrets_sample.json fileoperations/settings/secrets.json
7. python manage.py migrate
8. python manage.py runserver

```
It will run on port 8000, but if there is a need to specify a custom port, the following command can be executed:
```
python manage.py runserver 0.0.0.0:<CUSTOM_PORT_NUMBER>
```

### Docker way

1. Install `Docker` on your platform
2. Run `cd /fileoperations`
3. Run `docker build -t file-operations .`
4. Run `docker run -p 8000:8000 file-operations` (First port number is where the app will be accessed on local machine, and second is the one configured in the Dockerfile. This means that first port number can be changed if needed, but the second one should stay as it is.)

## How to use

- Recommended to use auto-generated docs page, which is available on http://localhost:8000/fileoperations/docs/. All endpoints can be tested there.
- Description of endpoints:
  - **GET** http://localhost:8000/fileoperations/search-files/?wildcard=WILDCARD
    -  Returns an array of files and folders
    -  Optional query param called "wildcard" accepts various patterns for file search. For example, "*.txt" will search for only files that end in ".txt" extension.
  - **GET** http://localhost:8000/fileoperations/download-files/?wildcard=WILDCARD
    -  Allows download of the files and folders
    -  Optional query param called "wildcard" accepts various patterns for file search
  - **POST** http://localhost:8000/fileoperations/move-file/
    -  Moves and renames files
    -  Accepts a body in the JSON format
    ```
    {
  		"source_path": "string", // must be a valid path to a file
  		"destination_path": "string" // can be any path, but must end in a file name
	}
    ```