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
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Configure Environment variables**
   
   Set up a new file named ```.env``` in the root directory of the project and add the following content:
   ```bash
   FLASK_SECRET_KEY=<your_key>

   MAIL_SERVER=smtp.example.com
   MAIL_PORT=587
   MAIL_USE_TLS=true
   MAIL_USERNAME=<your_email>
   MAIL_PASSWORD=<your_app_password>
   MAIL_DEFAULT_SENDER=EcoTrack <noreply@ecotrack.com>
   ```
   
   For security, you can create an "App Password" with your mail provider rather than your real password.

   After succesful setup, your ```.env``` file may look like:
   ```bash
   FLASK_SECRET_KEY=i_love_matcha

   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=true
   MAIL_USERNAME=test.example1@gmail.com
   MAIL_PASSWORD=abcd efgh hijk lmno
   MAIL_DEFAULT_SENDER=EcoTrack <noreply@ecotrack.com>
   ```

   Useful links for information on setting up app passwords:
   - [Gmail](https://support.google.com/accounts/answer/185833?hl=en)
   - [Outlook](https://support.microsoft.com/en-au/account-billing/how-to-get-and-use-app-passwords-5896ed9b-4263-e681-128a-a6f2979a7944)
   - [Yahoo](https://help.yahoo.com/kb/SLN15241.html?guccounter=1&guce_referrer=aHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS8&guce_referrer_sig=AQAAACM6bF-WHqshDR69KZBDLQXCaURxkoojDvEOdpxqmLNu-VsfTnqC2d8In7b1vGPgnT_v_3-fEPBZ1ZSmboFUxD1K8g88dhKGp1vcoDlnPtWLzTKu9IkAOQ2dd6s802EEOEhZHSSwQxW7bcIWU5ycr3HeO5KsT7WqYJiLHFHgzEN6)
   - [Apple](https://support.apple.com/en-au/102654)

5. **Initialise the database:**
   ```
   flask db upgrade
   ```

6. **Run the application:**
   ```
   flask run
   or, to open in debug mode:
   python EcoTrack.py
   ```
   - _Note: You may need to use ```python3``` or a different command depending on how Python is installed on your system._

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

## Styling - TailwindCSS

1. Install Tailwind CSS

```bash
npm install tailwindcss @tailwindcss/cli
```

2. Run the CLI tool to scan your source files for classes and build your CSS.

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
