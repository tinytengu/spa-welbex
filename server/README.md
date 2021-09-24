# Flask RESTful backend

## Usage
> These instructions are intended for development usage.
> For production configure it by yourself for your production environment
0. `(Optional)` Create and activate Python environment
    ```bash
    python3 -m venv env

    # Windows
    env\Scripts\activate

    # *NIX
    source venv/bin/activate
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

## Endpoints
| Endpoint | Method | Description | Arguments
| - | - | - | -
| /items | GET | Get all the items | sort_by, sort_type, sort_value
| /items | POST | Add new items | date, name, amount, distance
| /items/`id` | PUT | Modify item | date, name, amount, distance
| /items/`id` | DELETE | Delete item |
| /items/fill | GET | Fill items list with random data | count