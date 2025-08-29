import subprocess
import time

def wait_for_postgres(host, max_retries=5, delay=5):
    retries = 0
    while retries < max_retries:
        try:
            result = subprocess.run(
                ["pg_isready", "-h", host], check=True, capture_output=True, text=True
            )
            if "accepting connections" in result.stdout:
                print("Successdully connected to PostgreSQL!")
                return True
        except subprocess.CalledProcessError as e:
            print(f"Error connecting to PsostgreSQL: {e}")
            retries += 1
            print(f"Retrying in {delay} seconds... (Attemp {retries}/{max_retries})")
            time.sleep(delay)
    print("Failed to connect to PostgreSQL after multiple attempts.")
    return False

if not wait_for_postgres(host="source_postgres"):
    exit(1)

print("Starting ELT script...")

source_config = {
    'dbname': 'source_db',
    'user': 'postgres',
    'password': 'secret',
    'host': 'source_postgres'
}

destination_config = {
    'dbname': 'destination_db',
    'user': 'postgres',
    'password': 'secret',
    'host': 'destination_postgres'
}

# Use pg_dump to dump the source database to a SQL file
dump_command = [
    'pg_dump',
    '-h', source_config['host'],
    '-U', source_config['user'],
    '-d', source_config['dbname'],
    '-f', 'data_dump.sql',
    '-w' # do not prompt for password
]

# Set the PGPASSWORD environment variable to avoid password prompt
subprocess_env = dict(PGPASSWORD=source_config['password'])

# execute the dump command
subprocess.run(dump_command, env=subprocess_env, check=True)

# Use psql to load the dumped SQL file 
load_command = [
    'psql',
    '-h', destination_config['host'],
    '-U', destination_config['user'],
    '-d', destination_config['dbname'],
    '-a', '-f', 'data_dump.sql',
]
subprocess_env = dict(PGPASSWORD=destination_config['password'])
subprocess.run(load_command, env=subprocess_env, check=True)
print('Ending ELT script...')
