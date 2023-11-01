# Teams Attendance List Analyzer (TALA) API

## [Try it out 🚀](http://tala.lparolari.xyz/)

Enjoy.

## Introduction

This project exposes REST API as a service for the Teams attendance list
analyzer model.


* If you are interested in the ML model, please visit
  [ms-teams-attendance-list-analyzer](https://github.com/lparolari/ms-teams-attendance-list-analyzer):
  a Jupyter notebook with researches on the best attendance lists analyzer
  model.


* If you are looking for frontend code, visit
  [tala-frontend](https://github.com/lparolari/tala-frontend).

## Development

1. Create a Python 3.8 virtualenv

```bash
python3 -m venv venv
source bin/venv/activate
```

2. Install requirements

```bash
pip install -r requirements.txt
```

3. Run the backend

```bash
python server.py
```

You can now see the server up and running at [`http://localhost:5000/`](http://localhost:5000/).

## Release

Build an image and push it to Dockerhub.

```
docker build lparolari/tala:tala-backend-latest -f deploy/Dockerfile .
docker push lparolari/tala:tala-backend-latest
```

## API

### GET `/`

Dummy reply, should return `{"hello": "world"}` if server status is ok.

#### Example

```bash
$ curl http://localhost:5000

127.0.0.1 - - [20/Aug/2022 13:54:09] "GET / HTTP/1.1" 200 -
{"hello":"world"}
```

### POST `/anomalies`

Return a list of outliers for each attendance list provided.

#### Input

**Headers**

* `Content-Type: multipart/form-data`

**Query params**

* `analysis_type`, can be either `Left` or `Joined`. If not set, `Left` is used.

**Form parts**

* `file[]`, a list of files where each file must be a well-formed MS Teams 
  attendance list (see below).

#### Output

A list of outliers for each attendance list provided.

#### Example

```bash
$ curl -X post -F "file[]=@demo/test.csv" http://localhost:5000/anomalies

[
   {
      "estimated_robust_location":"29/03/2021 12:46:31",
      "filename":"test.csv",
      "outliers":[
         {
            "delta":"-2:40",
            "participant":"Nakia Sporer"
         },
         {
            "delta":"00:42",
            "participant":"Leonor Bernhard"
         },
         {
            "delta":"01:05",
            "participant":"Dustin Pacocha"
         }
      ]
   }
]
```

## MS Teams Attendance List

You can download attendance lists from MS Teams, follow [official
instructions](https://support.microsoft.com/en-us/office/view-and-download-meeting-attendance-reports-in-teams-ae7cf170-530c-47d3-84c1-3aedac74d310).

A valid MS Teams Attendance List must adhere to the following rule. 

* It is a CSV file delimited by tabs

* It has 3 columns:
  * `Full Name`, the participant name
  * `User Action`, the action user performed during the meeting
  * `Timestamp`, date and time of action performed by user

* `User Action`'s values must be either `Left` or `Joined`

* `Timestamp` is formatted like `3/29/2021, 12:01:32 PM`

Note that a user may have more that 2 rows in the attendance list, mainly
because of disconnections during meeting.

## Author

Luca Parolari

## License

MIT
