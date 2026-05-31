import subprocess
import sys

def run_command( command: list[ str ] ):
    """Helper function to run a command and exit if it fails."""

    print( f"==> Executing: {' '.join( command )}" )

    # Using subprocess.run ensures the script waits for the command to finish.
    # Avoid shell=True to enhance security and cross-platform reliability.
    result = subprocess.run( command )

    # If the command fails (exit code != 0), crash the script immediately.
    # This mimics 'set -e' in Linux shell scripts.
    if result.returncode != 0:
        print( f"❌ Command failed with exit code {result.returncode}" )
        sys.exit( result.returncode )


def main():

    try:
        # 1. Run Alembic database migrations
        print( "==> [Alembic] Checking and running database migrations..." )
        run_command( [ "alembic", "upgrade", "head" ] )
        print( "==> [Alembic] Migrations completed successfully!" )

        # 2. Start the FastAPI application via Uvicorn
        print( "==> [FastAPI] Starting the application..." )
        # sys.executable guarantees the exact same Python interpreter path is utilized.
        fastapi_cmd = [ sys.executable, "-m", "app.main" ]
        if sys.platform != "win32":
            import os

            # # On Linux/Docker, replace the current script process with the FastAPI process.
            # This resolves the 'PID 1' issue, ensuring graceful shutdown (SIGTERM handling).
            os.execvp( fastapi_cmd[ 0 ], fastapi_cmd )
        else:
            # Fallback for Windows environment
            run_command( fastapi_cmd )

    except KeyboardInterrupt:
        # Catch Ctrl+C on Windows to prevent messy stack traces in the console.
        print( "\nServer stopped by user." )
        sys.exit(0)

if __name__ == "__main__":
    main()