"""
Main entry point for RiskOptima Engine
Provides command-line interface to run different components
"""

import argparse
import sys
import subprocess
import os
from pathlib import Path

def run_backend(host: str = "127.0.0.1", port: int = 8000):
    """Run the FastAPI backend server"""
    print(f"Starting RiskOptima Engine Backend on {host}:{port}")
    print("Press Ctrl+C to stop")

    # Import here to avoid circular imports
    from .backend import run_backend as _run_backend
    _run_backend(host, port)

def run_frontend():
    """Run the Streamlit frontend"""
    print("Starting RiskOptima Engine Frontend")
    print("Press Ctrl+C to stop")

    # Run streamlit
    frontend_path = Path(__file__).parent / "frontend.py"
    cmd = [sys.executable, "-m", "streamlit", "run", str(frontend_path), "--server.port", "8501"]
    subprocess.run(cmd)

def run_full_stack(host: str = "127.0.0.1", backend_port: int = 8000):
    """Run both backend and frontend"""
    import threading
    import time

    print("Starting RiskOptima Engine (Full Stack)")
    print(f"Backend: http://{host}:{backend_port}")
    print("Frontend: http://localhost:8501")
    print("Press Ctrl+C to stop all services")

    # Start backend in a thread
    backend_thread = threading.Thread(
        target=run_backend,
        args=(host, backend_port),
        daemon=True
    )
    backend_thread.start()

    # Give backend time to start
    time.sleep(2)

    # Run frontend in main thread
    run_frontend()

def build_rust():
    """Build the Rust extension"""
    print("Building Rust extension...")
    os.chdir(Path(__file__).parent.parent.parent)
    result = subprocess.run(["maturin", "develop"], capture_output=True, text=True)

    if result.returncode == 0:
        print("✅ Rust extension built successfully")
    else:
        print("❌ Rust build failed:")
        print(result.stderr)
        sys.exit(1)

def setup_environment():
    """Set up the development environment"""
    print("Setting up RiskOptima Engine environment...")

    # Build Rust extension
    build_rust()

    # Install Python dependencies
    print("Installing Python dependencies...")
    os.chdir(Path(__file__).parent.parent.parent)
    result = subprocess.run(["uv", "sync"], capture_output=True, text=True)

    if result.returncode == 0:
        print("✅ Environment setup completed")
    else:
        print("❌ Environment setup failed:")
        print(result.stderr)
        sys.exit(1)

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="RiskOptima Engine - Quantitative Risk Analysis Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  risk-optima-engine setup          # Set up development environment
  risk-optima-engine backend        # Run backend API server
  risk-optima-engine frontend       # Run Streamlit frontend
  risk-optima-engine full           # Run both backend and frontend
  risk-optima-engine build          # Build Rust extension
        """
    )

    parser.add_argument(
        "command",
        choices=["setup", "backend", "frontend", "full", "build"],
        help="Command to run"
    )

    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host for backend server (default: 127.0.0.1)"
    )

    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port for backend server (default: 8000)"
    )

    args = parser.parse_args()

    try:
        if args.command == "setup":
            setup_environment()
        elif args.command == "backend":
            run_backend(args.host, args.port)
        elif args.command == "frontend":
            run_frontend()
        elif args.command == "full":
            run_full_stack(args.host, args.port)
        elif args.command == "build":
            build_rust()

    except KeyboardInterrupt:
        print("\nShutting down...")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()