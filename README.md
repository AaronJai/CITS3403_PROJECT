# CITS3403 Project: EcoTrack

### Description

The Environmental Impact Tracker allows users to log their daily activities and track their carbon footprint. By inputting various activities such as energy use, transportation choices, and shopping habits, the system calculates the environmental impact and provides personalized suggestions for reducing it.

### Members

| UWA ID   | Name             | GitHub Username                                     |
| -------- | ---------------- | --------------------------------------------------- |
| 23861827 | Mei Lin Ke       | [LXM-007](https://github.com/LXM-007)               |
| 23683717 | Salman Nikakhter | [samlam691](https://github.com/samlam691)           |
| 23074324 | Hazel Wang       | [HazelWangHuiZi](https://github.com/HazelWangHuiZi) |
| 22884212 | Aaron Tan        | [AaronJai](https://github.com/AaronJai)             |

### development notes (edit later)

when writing tailwind styles and refactoring reusable classes, use:

```
npx @tailwindcss/cli -i ./app/static/css/styles.css -o ./app/static/css/output.css --watch
```

- CLI automatically rebuilds `output.css` whenever we add styles to `styles.css` (happens because of the --watch flag)
- if you accidentally cancel or close it, just re-run it
