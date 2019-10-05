### A simple api for the OlivettiClub project @ Olivetti Hack Trento '19

Install the required dependencies:

```bash
pip install flask pony geocoder requests
```

Run it locally:

```bash
flask run
```

Simulate a standard flow:

```bash
./local_flow.sh
```

Populate the database with example data:
```bash
./seed.sh
```

#### Customization

It is possible to enable the experimental AI engine by
setting the `AI_ENABLED` flag to True in `app.py`, and setting
the URL of the AI server with the `AI_URL` constant in `ai_utils.py`.

