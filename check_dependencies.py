#!/usr/bin/env python3
"""
depsafe - Python Package Dependency Checker
Fetches and displays dependency information for Python packages from PyPI.
"""

import sys
import requests
from typing import Optional


def check_package_dependencies(package_name: str, version: Optional[str] = None) -> None:
    """
    Check and display dependencies for a Python package from PyPI.
    
    Args:
        package_name: Name of the package to check
        version: Specific version to check (optional, defaults to latest)
    """
    try:
        # Build PyPI API URL
        if version:
            url = f'https://pypi.org/pypi/{package_name}/{version}/json'
        else:
            url = f'https://pypi.org/pypi/{package_name}/json'
        
        print(f"Fetching package information for '{package_name}'...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        info = data['info']
        
        # Display package information
        print("\n" + "=" * 60)
        print(f"Package: {info['name']}=={info['version']}")
        print("=" * 60)
        
        # Python version requirement
        python_req = info.get('requires_python', 'Not specified')
        print(f"\nPython Required: {python_req}")
        
        # Dependencies
        requires_dist = info.get('requires_dist')
        if requires_dist:
            print(f"\nDependencies ({len(requires_dist)} total):")
            for dep in requires_dist:
                # Remove extra markers for cleaner display
                dep_clean = dep.split(';')[0].strip()
                print(f"  - {dep_clean}")
                
                # Show extras/markers if present
                if ';' in dep:
                    marker = dep.split(';', 1)[1].strip()
                    print(f"    (when: {marker})")
        else:
            print("\nDependencies: None")
        
        print("\n" + "=" * 60)
        
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print(f"\n❌ Error: Package '{package_name}' not found on PyPI.")
            if version:
                print(f"   Version '{version}' may not exist. Try without specifying a version.")
        else:
            print(f"\n❌ HTTP Error: {e}")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Error fetching package information: {e}")
        sys.exit(1)
    except KeyError as e:
        print(f"\n❌ Error parsing package data: {e}")
        sys.exit(1)


def main():
    """Main entry point for the script."""
    if len(sys.argv) < 2:
        print("Usage: python check_dependencies.py <package-name> [version]")
        print("\nExamples:")
        print("  python check_dependencies.py requests")
        print("  python check_dependencies.py requests 2.28.0")
        sys.exit(1)
    
    package_name = sys.argv[1]
    version = sys.argv[2] if len(sys.argv) > 2 else None
    
    check_package_dependencies(package_name, version)


if __name__ == '__main__':
    main()