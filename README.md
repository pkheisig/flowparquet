# 🌊 FlowParquet

**FlowParquet** is a modern, user-friendly desktop application designed to convert **Flow Cytometry Data (FCS)** and other tabular formats (**CSV, XLS, XLSX**) into high-performance **Parquet** files.

Built with Python and CustomTkinter, it offers a sleek dark-mode interface with drag-and-drop functionality, making data preparation for analysis pipelines faster and easier.

## ✨ Features

- **📁 Multi-Format Support**: Converts `.fcs`, `.csv`, `.xls`, and `.xlsx` files.
- **🖐️ Drag & Drop**: Easily add files or folders by dragging them into the application.
- **🏷️ Intelligent Parsing**:
  - Automatically extracts marker names (e.g., "CD4") from FCS files instead of channel names (e.g., "FL1-H").
  - Option to toggle between Marker Names and Channel Names.
- **🆔 Sample Tracking**: Optional automatic "SampleID" column generation based on filenames.
- **💾 Compression Options**: Choose between **Snappy** (fast), **Gzip** (small size), or **None**.
- **🚀 Batch Processing**: Convert hundreds of files in one go with a progress bar.
- **🌑 Modern UI**: Clean, dark-themed interface powered by CustomTkinter.

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher

### Setup
1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/FlowParquet.git
   cd FlowParquet
   ```

2. **Install dependencies:**
   It is recommended to use a virtual environment.
   ```bash
   pip install -r requirements.txt
   ```
   *Note: You may also need to install `pyinstaller` if you plan to build the executable.*

## 🚀 Usage

1. **Run the application:**
   ```bash
   python main.py
   ```

2. **Add Files:**
   - Drag and drop files/folders into the window.
   - Or use the "Add Files..." / "Add Folder..." buttons.

3. **Configure Options:**
   - **Use Marker Names**: Check this to use easy-to-read marker names (e.g., "CD3") for FCS columns.
   - **Add SampleID Col**: Adds a `SampleID` column with the filename (useful for merging multiple files later).
   - **Compression**: Select your preferred Parquet compression method.

4. **Convert:**
   - Click the green **Convert** button.
   - The status bar and progress bar will show the progress.
   - Converted `.parquet` files are saved in the **same directory** as the original files.

## 📦 Building Executables

You can package FlowParquet as a standalone application for macOS or Windows using `PyInstaller`.

### macOS
Run the build script:
```bash
chmod +x build_mac.sh
./build_mac.sh
```
The app will be located in the `dist/FlowParquet.app` folder.

### Windows
Run the batch file:
```cmd
build_windows.bat
```
The executable will be located in the `dist/FlowParquet/` folder.

## 💻 Tech Stack

- **GUI**: [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) & [TkinterDnD2](https://github.com/pmgagne/tkinterdnd2)
- **Data Processing**: [Pandas](https://pandas.pydata.org/) & [PyArrow](https://arrow.apache.org/docs/python/)
- **FCS Parsing**: [FlowIO](https://github.com/whitews/flowio)

---
*Happy Flow Cytometry Analysis!* 🧬📊
