# teams-meeting-attendance-analyzer-api

This project is based on the work done in [WIP](#). There you can find
the Python notebook with all the analysis and reasoning done to
analyze MS Teams attendance lists and find outliers.

This project is intended to provide an API to the Python script in
order to analyze attendance lists from the web.

## Usage

Run with docker

```
docker run --volume "`pwd`:/usr/src/app" -w "/usr/src/app" python:3.6.13-alpine3.13 pip install -r requirements.txt #python csgi.py
```

## API

### Get Attendance List

Input: a meeting attendance list \
Output: a JSON object with the meeting list data

### Get Outliers

Input: a meeting attendance list \
Output: a JSON array with outliers

## Author

Luca Parolari

## License

MIT
