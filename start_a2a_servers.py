"""
Launcher script to start the A2A servers for LeetSquad.

This script starts both the white agent (LeetCode solver) and green agent (judge)
on ports 8001 and 8002 respectively.
"""

import asyncio
import sys
from pathlib import Path

# Add src directory to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from a2a_service.main_server import main


if __name__ == "__main__":
    print("=" * 80)
    print("LeetSquad A2A Service Launcher")
    print("=" * 80)
    print("\nThis will start both agent servers:")
    print("  - White Agent (LeetCode Solver): http://localhost:8001")
    print("  - Green Agent (Judge/Evaluator): http://localhost:8002")
    print("\nPress Ctrl+C to stop the servers")
    print("=" * 80)
    print()

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nServers stopped by user")
        sys.exit(0)
