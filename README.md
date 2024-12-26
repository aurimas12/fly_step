# Slint Rust Template

A template for a Rust application that's using [Slint](https://slint.rs/) for the user interface.

## About

This template helps you get started developing a Rust application with Slint as toolkit
for the user interface. It demonstrates the integration between the `.slint` UI markup and
Rust code, how to react to callbacks, get and set properties, and use basic widgets.

## Usage

1. Install Rust by following its [getting-started guide](https://www.rust-lang.org/learn/get-started).
   Once this is done, you should have the `rustc` compiler and the `cargo` build system installed in your `PATH`.
2. Download and extract the [ZIP archive of this repository](https://github.com/slint-ui/slint-rust-template/archive/refs/heads/main.zip).
3. Rename the extracted directory and change into it:
    ```
    mv slint-rust-template-main my-project
    cd my-project
    ```
4. Build with `cargo`:
    ```
    cargo build
    ```
5. Run the application binary:
    ```
    cargo run
    ```

We recommend using an IDE for development, along with our [LSP-based IDE integration for `.slint` files](https://github.com/slint-ui/slint/blob/master/tools/lsp/README.md). You can also load this project directly in [Visual Studio Code](https://code.visualstudio.com) and install our [Slint extension](https://marketplace.visualstudio.com/items?itemName=Slint.slint).

## Next Steps

We hope that this template helps you get started, and that you enjoy exploring making user interfaces with Slint. To learn more
about the Slint APIs and the `.slint` markup language, check out our [online documentation](https://slint.dev/docs).

Don't forget to edit this readme to replace it by yours, and edit the `name =` field in `Cargo.toml` to match the name of your
project.

# How to run app
    Overview
This project is designed to find and display cheap one-way flights using Python.

    Project Information
Display Details run:
make info

This command displays:
Main project folder name.
Python and Pip versions.
Installed dependencies.
Virtual environment path.
Main application entry point.

    Help
To see all available commands, run:
make help

    Requirements
Python 3.12 (or compatible version installed).

    Setup Instructions
1. Clone the Repository
git clone <repository-url>
cd <repository-folder>
2. Create and Setup Virtual Environment run:
make venv - create a virtual environment named fs_env.
make setup - install dependencies listed in requirements.txt
or
make all - single action to instal virtual venv and Install dependencies

    Running the Application run:
make run
