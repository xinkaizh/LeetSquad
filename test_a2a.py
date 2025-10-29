"""
Test launcher script for A2A communication.

Run this after starting the servers with start_a2a_servers.py
"""

import asyncio
import sys
from pathlib import Path

# Add src directory to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from a2a_service.test_a2a_communication import main


if __name__ == "__main__":
    print("=" * 80)
    print("LeetSquad A2A Communication Test Suite")
    print("=" * 80)
    print("\nEnsure the servers are running before proceeding:")
    print("  python start_a2a_servers.py")
    print("=" * 80)
    print()

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
        sys.exit(0)
