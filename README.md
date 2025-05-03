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

## Setup Instructions

Follow these steps to set up the EcoTrack application:

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd CITS3403_PROJECT
   ```

2. **Create and activate a virtual environment:**
   ```
   # Windows
   python -m venv .venv
   .venv\Scripts\activate
   
   # Mac/Linux
   python -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Configure Environment variables**
   Set up a new file named ```.env``` in the root of the project and add the following content:
   ```bash
   FLASK_SECRET_KEY=""
   ```

5. **Initialize the database:**
   ```
   flask db upgrade
   ```

6. **Run the application:**
   ```
   flask run
   ```

7. **Access the application:**
   Open a web browser and go to `http://127.0.0.1:5000/`

## Database Management

If you need to make changes to the database models:

1. Update the models in `app/models.py`
2. Run migrations:
   ```
   flask db migrate -m "Description of changes"
   flask db upgrade
   ```

To check database version history:
```
flask db history
```

To downgrade to a previous version:
```
flask db downgrade
```

## Styling

### Using TailwindCSS

Install Tailwind CSS

```bash
npm install tailwindcss @tailwindcss/cli
```

Run the CLI tool to scan your source files for classes and build your CSS.

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

**Note:** For development, it is recommended to have two terminals open:

1. One for running the Flask server.
2. One for running the Tailwind CLI.


## Development

- The application uses SQLite for development
- Database file is stored in `app/app.db`
- Use `flask shell` to interact directly with the database
