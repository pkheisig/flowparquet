#!/bin/bash
# Install requirements first: pip install -r requirements.txt
# Install pyinstaller: pip install pyinstaller

rm -rf build dist
pyinstaller --noconfirm --onedir --windowed --name "FlowParquet" \
    --add-data "converter.py:." \
    --hidden-import "pandas" \
    --hidden-import "pyarrow" \
    --hidden-import "flowio" \
    --hidden-import "tkinterdnd2" \
    --collect-all "customtkinter" \
    --collect-all "tkinterdnd2" \
    --exclude-module "PyQt5" \
    --exclude-module "PyQt6" \
    --exclude-module "tensorflow" \
    --exclude-module "torch" \
    --exclude-module "keras" \
    --exclude-module "tensorboard" \
    --icon "FlowParquet.icns" \
    main.py

# Optional: Convert to DMG (requires create-dmg)
# create-dmg dist/FlowParquet.app