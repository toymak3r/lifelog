# LifeLog

Welcome to LifeLog, a personal journaling and life tracking application.

## Features

- **Daily Journals**: Record your thoughts and experiences every day.
- **Mood Tracking**: Keep track of your mood and identify patterns over time.
- **Goal Setting**: Set and track your personal goals.
- **Reminders**: Get reminders for important tasks and events.
- **Commuting Register**: Track your daily commutes.
- **Biometrics Register**: Keep track of your biometric data.
- **To-Do Lists**: Manage your tasks and to-do lists.
- **Podcast Management**: Manage your podcast subscriptions.

## Installation

To install LifeLog, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/toymak3r/lifelog.git
    ```
2. Navigate to the project directory:
    ```bash
    cd lifelog
    ```
3. Set up the virtual environment:
    ```bash
    python -m venv .env
    source .env/bin/activate
    ```
4. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

To start the application, run:
```bash
./run.sh
```

## Configuration

The configuration is managed by the `Config` class in [core/config.py](core/config.py). The configuration file is stored in the user's home directory under `.loglife/config.json`. If the configuration file does not exist, a default configuration is created using the template file `templates/config.template.json`.

## Logging

The module uses the `logging` library to log warnings and errors. Logs are generated when the user directory does not exist, when there is an error loading the configuration file, and when there is an error creating or saving the configuration file.

## Contributing

We welcome contributions! Please read our [contributing guidelines](CONTRIBUTING.md) for more details.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or feedback, please contact us at support@lifelog.com.
