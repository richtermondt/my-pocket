# my-pocket
Example of working with the Pocket API. See documentation: https://getpocket.com/developer/docs/overview

## Setup Local Environment
### Setting Environment Variables
To use the Pocket API, you must obtain your consumer_key from the Pocket Developer Portal and configure an environment variable named POCKET_CONSUMER_KEY contianing your consumer key
 
## Verify Local Environment

### Create Virtual Environment

In a terminal run the following commands from the root folder of the forked project. 

#### Windows
```
py -m venv .\.venv
```
Or
```
python -m venv .\.venv
```

#### macOS & Linux
```
python -m venv ./.venv
```

Once that completes, also run this command from the same folder.

#### Windows
```
.\.venv\Scripts\activate
```

#### macOS & Linux
```
source .venv/bin/activate
```
### Install Dependencies
Now that you are working in the virtualenv, install the project dependencies with the following command.

```
pip install -r requirements.txt
```

### Python Execution
Note that you will be prompted to complete the Pocket authorization in your browser. Once authorized in your browser, press Enter to continue.

#### MacOS
```
./.venv/bin/python pocket-handler.py
```


#### Windows
```
py pocket-handler.py
```
