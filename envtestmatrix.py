import sys

def run(env):
    if env == 'dev':
        print("Running in Development mode")
    elif env == 'test':
        print("Running in Testing mode")
    elif env == 'prod':
        print("Running in Production mode")
    else:
        print("Unknown environment")

if __name__ == "__main__":
    environment = sys.argv[1] if len(sys.argv) > 1 else 'dev'
    run(environment)
