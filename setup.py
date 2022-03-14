"""Package configuration."""
import setuptools

setuptools.setup(
    author="Jonathan Bowman",
    description="Configure a vanilla Fedora system.",
    entry_points={"console_scripts": ["update-go=shaper.golang:go_update"]},
    name="shaper",
    py_modules=["shaper"],
    version="0.1.0",
)
