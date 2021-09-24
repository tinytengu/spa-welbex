# Flask RESTful backend

## Usage
> These instructions are intended for development usage.
> For production configure it by yourself for your production environment
0. `(Optional)` Create Python environment
    ```bash
    python3 -m venv env
    ```
1. Install the project requirements
    ```bash
    pip install -r requirements.txt
    ```
2. Configure environment variables
    1. Create `.env` file
    2. Fill out as following
        ```bash
        DB_HOSTNAME=<YOUR_VALUE>
        DB_USERNAME=<YOUR_VALUE>
        DB_PASSWORD=<YOUR_VALUE>
        DB_DATABASE=<YOUR_VALUE>
        ```