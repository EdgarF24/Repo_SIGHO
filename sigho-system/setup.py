"""
SIGHO - Sistema Integrado de Gestión Hotelera
Setup script para instalación del paquete
"""

from setuptools import setup, find_packages

# Leer el archivo README para la descripción larga
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="sigho",
    version="1.0.0",
    author="Equipo SIGHO",
    author_email="info@hotelsigho.com",
    description="Sistema Integrado de Gestión Hotelera",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sigho/sigho-system",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Office/Business",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.12",
    install_requires=[
        # Backend dependencies
        "fastapi>=0.104.1",
        "uvicorn[standard]>=0.24.0",
        "sqlalchemy>=2.0.23",
        "pydantic>=2.5.0",
        "python-jose[cryptography]>=3.3.0",
        "passlib[bcrypt]>=1.7.4",
        "python-multipart>=0.0.6",
        "python-dotenv>=1.0.0",
        # Frontend dependencies
        "customtkinter>=5.2.0",
        "Pillow>=10.1.0",
        "requests>=2.31.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-cov>=4.1.0",
            "black>=23.11.0",
            "flake8>=6.1.0",
            "mypy>=1.7.1",
        ],
    },
    entry_points={
        "console_scripts": [
            "sigho-backend=backend.main:main",
            "sigho-frontend=frontend.main:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
