# depsafe

A Python package dependency validator that helps you catch compatibility conflicts before they break your environment. Inspect package dependencies from PyPI and test them in an isolated Docker environment against your target Python version and existing packages.

## The Problem

Python projects often require multiple third-party packages, each with their own dependencies. When you add new packages to your project, you risk creating version conflicts with existing dependencies. For example, a new package might require a newer version of a library that conflicts with another package in your environment.

These dependency conflicts can cause your application to fail in subtle or non-obvious ways, and troubleshooting them in a production environment can be difficult and time-consuming. Installing incompatible packages can break your existing setup, requiring you to roll back changes or spend time resolving conflicts.

This utility solves the problem by allowing you to test your package dependencies in a local Docker environment _before_ you install them in your actual project. This helps you catch and resolve conflicts early in the development process, saving time and preventing potential breakage.

## Features

- Check the dependencies of any Python package from PyPI.
- Build a Docker image with a `requirements.txt` file to test compatibility with any Python version.
- Identify version conflicts before they break your environment.
- Test your dependencies in an isolated environment.

## Getting Started

### Prerequisites

- Docker installed on your local machine.
- Python 3.6 or higher.

### Usage

#### 1. Check Package Dependencies

You can use the `check_dependencies.py` script to inspect the dependencies of a package before adding it to your `requirements.txt`.

Run the script with the package name:
```sh
python check_dependencies.py <package-name> [version]
```

**Examples:**

```sh
# Check latest version
python check_dependencies.py requests

# Check specific version
python check_dependencies.py requests 2.28.0
```

**Example Output:**

```
Package: requests==2.31.0
Python Required: >=3.7

Dependencies:
  - charset-normalizer (<4,>=2)
  - idna (<4,>=2.5)
  - urllib3 (<3,>=1.21.1)
  - certifi (>=2017.4.17)
```

This shows you all the dependencies and their version constraints for the specified package.

#### 2. Test Compatibility with Your Environment

1.  Add your desired packages to `requirements.txt`. It is **highly recommended** to pin the versions of your dependencies to ensure reproducible builds.
    ```
    # requirements.txt
    requests==2.31.0
    numpy==1.24.0
    pandas==2.0.0
    ```

2.  Build the Docker image. This will install the packages from `requirements.txt` and check for conflicts.
    ```sh
    docker build --build-arg PYTHON_VERSION=3.11 -t depsafe .
    ```
    
    You can specify different Python versions (e.g., `3.8`, `3.9`, `3.10`, `3.11`, `3.12`):
    ```sh
    docker build --build-arg PYTHON_VERSION=3.9 -t depsafe .
    ```
    
    If you want to test against a custom base image (e.g., your production image):
    ```sh
    docker build --build-arg BASE_IMAGE=your-custom-image:tag -t depsafe .
    ```

3.  Analyze the build output.

    -   **Successful Build:** If the Docker build completes successfully, your packages are compatible with each other and the Python version.
    -   **Failed Build:** If the build fails, the output will show the dependency conflicts that need to be resolved.

    **Example of a Failed Build:**

    ```
    package-a 1.2.0 has requirement cryptography>=38.0.3, but you have cryptography 36.0.2.
    ERROR: After October 2020 you may experience errors when installing or updating packages.
    executor failed running [/bin/sh -c bash installer.sh]: exit code: 1
    ```

    This error indicates that `package-a` requires `cryptography>=38.0.3`, but an older version (`36.0.2`) is present. To fix this, you would need to adjust the versions in your `requirements.txt` to satisfy all dependencies.

## Contributing

Contributions are welcome! Please read our [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute to this project.

## Use Cases

- **Pre-deployment Testing:** Validate packages before deploying to production.
- **Python Version Migration:** Test if your dependencies work with a newer Python version.
- **Dependency Updates:** Check if updating a package will break your existing dependencies.
- **New Package Addition:** Verify a new package is compatible with your current stack.
- **CI/CD Integration:** Add dependency validation to your continuous integration pipeline.

## Code of Conduct

Please note that this project is released with a [Contributor Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.