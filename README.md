# CITS3403 Project: EcoTrack

## Description

The Environmental Impact Tracker allows users to log their daily activities and track their carbon footprint. By inputting various activities such as energy use, transportation choices, and shopping habits, the system calculates the environmental impact and provides personalized suggestions for reducing it.

## Members

| UWA ID   | Name             | GitHub Username                               |
| -------- | ---------------- | --------------------------------------------- |
| 23861827 | Mei Lin Ke       | [MeiLin99999](https://github.com/MeiLin99999) |
| 23683717 | Salman Nikakhter | [samlam691](https://github.com/samlam691)     |
| 23074324 | Hazel Wang       | [useri4l](https://github.com/useri4l)         |
| 22884212 | Aaron Tan        | [AaronJai](https://github.com/AaronJai)       |

## USAGE

### Using TailwindCSS

when writing tailwind styles and refactoring reusable classes, use:

```bash
npx @tailwindcss/cli -i ./app/static/css/styles.css -o ./app/static/css/output.css --watch
```

- we ADD our classes to `styles.css`, but we link the `output.css` stylesheet
- CLI automatically rebuilds `output.css` whenever we add styles to `styles.css` (happens because of the --watch flag)
- if you accidentally cancel or close it, just re-run it

In case you get Permission denied on Mac, run:

```bash
chmod +x ./node_modules/.bin/tailwindcss
```

---

### Backend (Flask) Setup

#### Virtual Environment

**Windows:**

```bash
py -3 -m venv .venv
.venv\Scripts\activate
```

**Mac/Linux:**

```bash
python3 -m venv .venv
. .venv/bin/activate
```

#### Install Dependencies

currently required: Flask, Flask-WTF, SQLAlchemy

```bash
pip install -r requirements.txt
```

#### Run the Application (in root directory)

```bash
flask run
```

**Note:** For development, it is recommended to have two terminals open:

1. One for running the Flask server.
2. One for running the Tailwind CLI.
