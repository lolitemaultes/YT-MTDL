#!/usr/bin/env python3

import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox,
                           QProgressBar, QTextEdit, QFileDialog, QSpinBox, 
                           QCheckBox, QTabWidget, QGroupBox, QMessageBox,
                           QScrollArea, QGridLayout, QStatusBar)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSize, QTimer
from PyQt6.QtGui import QIcon, QFont, QColor, QPixmap, QPalette
import yt_dlp
import concurrent.futures
import threading
import json
import requests
from pathlib import Path

def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class CustomStyle:
    @staticmethod
    def apply_dark_theme(app):
        app.setStyle("Fusion")
        
        # Dark theme color palette
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.ColorRole.Window, QColor(28, 28, 28))
        dark_palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ColorRole.Base, QColor(35, 35, 35))
        dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(42, 42, 42))
        dark_palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ColorRole.ToolTipText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ColorRole.Text, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ColorRole.Button, QColor(45, 45, 45))
        dark_palette.setColor(QPalette.ColorRole.ButtonText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 0))
        dark_palette.setColor(QPalette.ColorRole.Link, QColor(66, 133, 244))
        dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(66, 133, 244))
        dark_palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
        
        app.setPalette(dark_palette)
        
        # Enhanced stylesheet with modern, clean design
        app.setStyleSheet("""
            QMainWindow {
                background-color: #1c1c1c;
            }
            
            QWidget {
                margin: 0;
                padding: 0;
            }
            
            QGroupBox {
                border: 1px solid #3d3d3d;
                border-radius: 8px;
                margin-top: 1.5em;
                padding: 15px;
                background-color: #2a2a2a;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 5px;
                color: #ffffff;
                font-weight: bold;
            }
            
            QPushButton {
                background-color: #2fd492;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
                min-width: 100px;
                margin: 2px;
            }
            
            QPushButton:hover {
                background-color: #25a270;
            }
            
            QPushButton:pressed {
                background-color: #1c8159;
            }
            
            QPushButton:disabled {
                background-color: #383838;
                color: #888888;
            }
            
            QLineEdit {
                padding: 8px;
                border-radius: 6px;
                border: 1px solid #3d3d3d;
                background-color: #333333;
                color: white;
                selection-background-color: #4285f4;
                margin: 2px;
            }
            
            QLineEdit:focus {
                border: 1px solid #4285f4;
            }
            
            QTextEdit {
                padding: 8px;
                border-radius: 6px;
                border: 1px solid #3d3d3d;
                background-color: #333333;
                color: white;
                selection-background-color: #4285f4;
                margin: 2px;
            }
            
            QProgressBar {
                border: none;
                border-radius: 4px;
                background-color: #333333;
                height: 20px;
                text-align: center;
                margin: 2px;
            }
            
            QProgressBar::chunk {
                border-radius: 4px;
                background-color: #4285f4;
            }
            
            QTabWidget::pane {
                border: 1px solid #3d3d3d;
                border-radius: 8px;
                top: -1px;
                background-color: #2a2a2a;
            }
            
            QTabBar::tab {
                background-color: #333333;
                color: white;
                padding: 10px 20px;
                margin: 2px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
            }
            
            QTabBar::tab:selected {
                background-color: #4285f4;
            }
            
            QTabBar::tab:hover:!selected {
                background-color: #3d3d3d;
            }
            
            QComboBox {
                padding: 6px;
                border-radius: 6px;
                border: 1px solid #3d3d3d;
                background-color: #333333;
                color: white;
                min-width: 100px;
            }
            
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid white;
                margin-right: 5px;
            }
            
            QSpinBox {
                padding: 6px;
                border-radius: 6px;
                border: 1px solid #3d3d3d;
                background-color: #333333;
                color: white;
                min-width: 80px;
            }
            
            QCheckBox {
                color: white;
                spacing: 5px;
            }
            
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border-radius: 4px;
                border: 1px solid #3d3d3d;
                background-color: #333333;
            }
            
            QCheckBox::indicator:checked {
                background-color: #4285f4;
            }
            
            #logo_container {
                margin: 20px;
                padding: 10px;
                background-color: transparent;
            }
            
            /* New scroll area styles start here */
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            
            QScrollBar:vertical {
                border: none;
                background-color: #2a2a2a;
                width: 12px;
                margin: 0;
            }
            
            QScrollBar::handle:vertical {
                background-color: #4d4d4d;
                border-radius: 6px;
                min-height: 24px;
                margin: 2px;
            }
            
            QScrollBar::handle:vertical:hover {
                background-color: #5d5d5d;
            }
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
            
            QScrollArea > QWidget > QWidget {
                background-color: #1c1c1c;
            }
            /* New scroll area styles end here */
            
            QStatusBar {
                background-color: #252525;
                color: white;
                border-top: 1px solid #3d3d3d;
            }
            
            QStatusBar QLabel {
                padding: 3px 6px;
            }
        """)

class DownloadWorker(QThread):
    progress = pyqtSignal(dict)
    finished = pyqtSignal(bool)
    error = pyqtSignal(str)
    status_update = pyqtSignal(str)

    def __init__(self, url, options):
        super().__init__()
        self.url = url
        self.options = options
        self.is_cancelled = False
        self.chunk_size = 8192

    def run(self):
        try:
            thread_count = int(self.options.get('thread_count', 3))
            self.status_update.emit(f"Initializing download with {thread_count} threads...")

            ydl_opts = {
                'format': self.options.get('format', 'bestvideo+bestaudio/best'),
                'outtmpl': self.options.get('outtmpl', '%(title)s.%(ext)s'),
                'writesubtitles': self.options.get('writesubtitles', False),
                'noplaylist': self.options.get('noplaylist', True),
                'progress_hooks': [self._progress_hook],
                'concurrent_fragment_downloads': thread_count,
                'merge_output_format': 'mp4',
            }

            if 'ratelimit' in self.options:
                ydl_opts['ratelimit'] = self.options['ratelimit']

            if 'proxy' in self.options:
                ydl_opts['proxy'] = self.options['proxy']

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                self.status_update.emit("Starting download...")
                ydl.download([self.url])
                
            self.finished.emit(True)

        except Exception as e:
            self.error.emit(str(e))
            self.finished.emit(False)

    def _progress_hook(self, d):
        if d['status'] == 'downloading':
            total = d.get('total_bytes', 0)
            if total == 0:
                total = d.get('total_bytes_estimate', 0)
            
            downloaded = d.get('downloaded_bytes', 0)
            
            if total > 0:
                progress = {
                    'downloaded': downloaded,
                    'total': total,
                    'filename': d.get('filename', 'Unknown'),
                    'speed': d.get('speed', 0),
                    'eta': d.get('eta', 0)
                }
                self.progress.emit(progress)
                
                if 'speed' in d and d['speed']:
                    speed = d['speed'] / 1024 / 1024  # Convert to MB/s
                    status = f"Downloading at {speed:.1f} MB/s"
                    if d.get('eta'):
                        status += f" (ETA: {d['eta']} seconds)"
                    self.status_update.emit(status)
        
        elif d['status'] == 'finished':
            self.status_update.emit(f"Finished downloading {d.get('filename', 'file')}")

    def cancel(self):
        self.is_cancelled = True

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Initialize window properties
        self.setWindowTitle("YouTube Multi-Threaded Downloader")
        self.setMinimumSize(800, 700)
        
        # Initialize variables
        self.worker = None
        self.pending_urls = []
        self.current_url_index = 0
        
        # Create UI
        self.init_ui()
        
        # Set up status bar
        self.statusBar().showMessage("Ready")
        
        # Load saved settings
        self.load_settings()
        
        # Update UI state
        self.update_status_bar()

    def init_ui(self):
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Create scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        main_layout.addWidget(scroll)

        # Create container for scrollable content
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(20, 10, 20, 10)
        layout.setSpacing(15)

        # Logo container
        logo_container = QWidget()
        logo_container.setObjectName("logo_container")
        logo_container.setMinimumHeight(100)
        logo_layout = QHBoxLayout(logo_container)
        logo_layout.setContentsMargins(0, 10, 0, 10)
        
        logo_label = QLabel()
        try:
            # Get absolute path and verify file exists
            logo_path = get_resource_path("Resources/yt-mtdl/yt-mtdl.png")
            print(f"Attempting to load logo from: {logo_path}")
            if not os.path.exists(logo_path):
                print(f"Logo file not found at: {logo_path}")
                raise FileNotFoundError(f"Logo file not found at: {logo_path}")

            # Load the image and check if it's valid
            logo_pixmap = QPixmap(logo_path)
            if logo_pixmap.isNull():
                print("Failed to load logo: QPixmap is null")
                raise Exception("Failed to load logo: QPixmap is null")

            print(f"Logo loaded successfully. Original size: {logo_pixmap.width()}x{logo_pixmap.height()}")
            
            # Calculate scaling
            window_width = self.width()
            target_width = min(int(window_width * 0.8), 800)
            target_height = int(target_width * (700/1920))
            
            print(f"Scaling logo to: {target_width}x{target_height}")
            
            scaled_pixmap = logo_pixmap.scaled(
                target_width,
                target_height,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            
            print(f"Scaled size: {scaled_pixmap.width()}x{scaled_pixmap.height()}")
            
            logo_label.setPixmap(scaled_pixmap)
            logo_container.setFixedHeight(target_height + 20)
            print("Logo set to label successfully")
            
        except Exception as e:
            print(f"Error loading logo: {str(e)}")
            print(f"Current working directory: {os.getcwd()}")
            logo_label.setText("YT-MTDL")
            logo_label.setStyleSheet("font-size: 32px; font-weight: bold; color: #4285f4;")
        
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_layout.addStretch()
        logo_layout.addWidget(logo_label)
        logo_layout.addStretch()
        
        layout.addWidget(logo_container)

        # Create tabs
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)

        # Download tab
        download_tab = QWidget()
        download_layout = QVBoxLayout(download_tab)
        download_layout.setSpacing(15)
        self.tab_widget.addTab(download_tab, "Download")

        # URL input group
        url_group = QGroupBox("Video URL")
        url_layout = QVBoxLayout()
        url_layout.setSpacing(10)
        
        url_input_layout = QHBoxLayout()
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter YouTube URL here or import from text file")
        url_input_layout.addWidget(self.url_input)
        
        import_btn = QPushButton("Import URLs")
        import_btn.clicked.connect(self.import_urls)
        import_btn.setFixedWidth(120)
        url_input_layout.addWidget(import_btn)
        
        url_layout.addLayout(url_input_layout)
        
        # URL list
        self.url_list = QTextEdit()
        self.url_list.setPlaceholderText("Imported URLs will appear here")
        self.url_list.setMaximumHeight(100)
        self.url_list.setReadOnly(True)
        url_layout.addWidget(self.url_list)
        
        url_group.setLayout(url_layout)
        download_layout.addWidget(url_group)

        # Options group
        options_group = QGroupBox("Download Options")
        options_layout = QGridLayout()
        options_layout.setSpacing(10)
        
        # Format selection
        options_layout.addWidget(QLabel("Format:"), 0, 0)
        self.format_combo = QComboBox()
        self.format_combo.addItems(["Best Quality", "Video Only", "Audio Only"])
        options_layout.addWidget(self.format_combo, 0, 1)
        
        # Quality selection
        options_layout.addWidget(QLabel("Quality:"), 0, 2)
        self.quality_combo = QComboBox()
        self.quality_combo.addItems(["1080p", "720p", "480p", "360p", "Auto"])
        options_layout.addWidget(self.quality_combo, 0, 3)
        
        # Checkboxes
        self.subtitle_check = QCheckBox("Download Subtitles")
        self.playlist_check = QCheckBox("Download Playlist")
        options_layout.addWidget(self.subtitle_check, 1, 0, 1, 2)
        options_layout.addWidget(self.playlist_check, 1, 2, 1, 2)
        
        options_group.setLayout(options_layout)
        download_layout.addWidget(options_group)

        # Output directory group
        output_group = QGroupBox("Output Directory")
        output_layout = QHBoxLayout()
        output_layout.setSpacing(10)
        
        self.output_path = QLineEdit()
        self.output_path.setText(str(Path.home() / "Downloads"))
        output_layout.addWidget(self.output_path)
        
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self.browse_output)
        browse_btn.setFixedWidth(100)
        output_layout.addWidget(browse_btn)
        
        output_group.setLayout(output_layout)
        download_layout.addWidget(output_group)

        # Progress group
        progress_group = QGroupBox("Download Progress")
        progress_layout = QVBoxLayout()
        progress_layout.setSpacing(10)
        
        self.progress_bar = QProgressBar()
        progress_layout.addWidget(self.progress_bar)
        
        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        self.status_text.setMaximumHeight(100)
        progress_layout.addWidget(self.status_text)
        
        progress_group.setLayout(progress_layout)
        download_layout.addWidget(progress_group)

        # Control buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self.clear_data)
        self.clear_btn.setFixedSize(120, 35)
        button_layout.addWidget(self.clear_btn)
        
        self.download_btn = QPushButton("Download")
        self.download_btn.clicked.connect(self.start_download)
        self.download_btn.setFixedSize(120, 35)
        button_layout.addWidget(self.download_btn)
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.cancel_download)
        self.cancel_btn.setEnabled(False)
        self.cancel_btn.setFixedSize(120, 35)
        button_layout.addWidget(self.cancel_btn)
        
        download_layout.addLayout(button_layout)

        # Settings tab
        settings_tab = QWidget()
        settings_layout = QVBoxLayout(settings_tab)
        settings_layout.setSpacing(15)
        self.tab_widget.addTab(settings_tab, "Settings")
        
        # Add settings controls
        self.create_settings_tab(settings_layout)
        
        # Set the scroll area's widget
        scroll.setWidget(container)

    def create_settings_tab(self, layout):
        # Download settings
        download_group = QGroupBox("Download Settings")
        download_layout = QGridLayout()
        download_layout.setSpacing(10)
        
        # Thread settings
        download_layout.addWidget(QLabel("Download Threads:"), 0, 0)
        self.thread_spin = QSpinBox()
        self.thread_spin.setRange(1, 32)
        self.thread_spin.setValue(16)
        self.thread_spin.setToolTip("Higher values may improve download speed")
        download_layout.addWidget(self.thread_spin, 0, 1)
        
        # Rate limit settings
        download_layout.addWidget(QLabel("Speed Limit (KB/s):"), 1, 0)
        self.rate_limit = QSpinBox()
        self.rate_limit.setRange(0, 100000)
        self.rate_limit.setValue(0)
        self.rate_limit.setSpecialValueText("No Limit")
        self.rate_limit.setToolTip("0 means no speed limit")
        download_layout.addWidget(self.rate_limit, 1, 1)
        
        download_group.setLayout(download_layout)
        layout.addWidget(download_group)
        
        # Proxy settings
        proxy_group = QGroupBox("Proxy Settings")
        proxy_layout = QVBoxLayout()
        proxy_layout.setSpacing(10)
        
        self.use_proxy = QCheckBox("Use Proxy")
        proxy_layout.addWidget(self.use_proxy)
        
        proxy_input_layout = QHBoxLayout()
        self.proxy_input = QLineEdit()
        self.proxy_input.setPlaceholderText("http://proxy:port")
        proxy_input_layout.addWidget(self.proxy_input)
        proxy_layout.addLayout(proxy_input_layout)
        
        proxy_group.setLayout(proxy_layout)
        layout.addWidget(proxy_group)
        
        # Save button
        save_layout = QHBoxLayout()
        save_layout.addStretch()
        
        save_btn = QPushButton("Save Settings")
        save_btn.clicked.connect(self.save_settings)
        save_layout.addWidget(save_btn)
        
        layout.addLayout(save_layout)
        layout.addStretch()
        
    def handle_resize(self, event):
        """Handle window resize events to scale the logo appropriately"""
        try:
            # Find all QLabels in the window
            labels = self.findChildren(QLabel)
            # Find the one inside logo_container
            logo_label = None
            for label in labels:
                if label.parent() and label.parent().objectName() == "logo_container":
                    logo_label = label
                    break
            
            if logo_label:
                # Get the window width
                window_width = self.width()
                # Calculate the desired width (80% of window width)
                target_width = min(int(window_width * 0.8), 800)  # Cap at 800px
                # Calculate height based on aspect ratio (1920:700)
                target_height = int(target_width * (700/1920))

                # Load and scale the logo
                logo_pixmap = QPixmap(get_resource_path("Resources/yt-mtdl/yt-mtdl.png"))
                scaled_pixmap = logo_pixmap.scaled(
                    target_width,
                    target_height,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                logo_label.setPixmap(scaled_pixmap)
                
                # Adjust container height to match logo height plus padding
                if logo_label.parent():
                    logo_label.parent().setFixedHeight(target_height + 20)  # 10px padding top and bottom
        
        except Exception as e:
            print(f"Error resizing logo: {e}")
        
        # Call the original resize event
        super().resizeEvent(event)

    def browse_output(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if directory:
            self.output_path.setText(directory)

    def import_urls(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select URL List File",
            "",
            "Text Files (*.txt);;All Files (*.*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    urls = [line.strip() for line in f if line.strip()]
                
                if urls:
                    self.url_list.clear()
                    self.url_list.append(f"Found {len(urls)} URLs:")
                    for url in urls:
                        self.url_list.append(url)
                    
                    self.pending_urls = urls
                    self.current_url_index = 0
                    
                    self.url_input.setText("Multiple URLs imported")
                    QMessageBox.information(self, "Import Successful", f"Successfully imported {len(urls)} URLs")
                else:
                    QMessageBox.warning(self, "Import Failed", "No valid URLs found in the file")
            
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to import URLs: {str(e)}")

    def start_download(self):
        if hasattr(self, 'pending_urls') and self.pending_urls:
            self.start_bulk_download()
        else:
            self.start_single_download()

    def start_bulk_download(self):
        if self.current_url_index >= len(self.pending_urls):
            QMessageBox.information(self, "Complete", "All downloads completed!")
            self.progress_bar.setFormat("%p%")
            return
        
        url = self.pending_urls[self.current_url_index]
        self.status_text.append(f"\nStarting download {self.current_url_index + 1} of {len(self.pending_urls)}")
        self.status_text.append(f"URL: {url}")
        
        self.progress_bar.setFormat(f"%p% (File {self.current_url_index + 1}/{len(self.pending_urls)})")
        
        options = self._get_download_options()
        self.start_worker(url, options)

    def start_single_download(self):
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Error", "Please enter a URL")
            return
        
        options = self._get_download_options()
        self.start_worker(url, options)

    def _get_download_options(self):
        format_option = self.format_combo.currentText()
        quality = self.quality_combo.currentText()
        
        if format_option == "Best Quality":
            if quality == "Auto":
                format_str = "bestvideo+bestaudio/best"
            else:
                height = quality[:-1]
                format_str = f"bestvideo[height<={height}]+bestaudio/best[height<={height}]"
        elif format_option == "Video Only":
            if quality == "Auto":
                format_str = "bestvideo"
            else:
                height = quality[:-1]
                format_str = f"bestvideo[height<={height}]"
        else:  # Audio Only
            format_str = "bestaudio"
        
        options = {
            'format': format_str,
            'outtmpl': os.path.join(self.output_path.text(), '%(title)s.%(ext)s'),
            'writesubtitles': self.subtitle_check.isChecked(),
            'noplaylist': not self.playlist_check.isChecked(),
            'thread_count': self.thread_spin.value()
        }
        
        if self.use_proxy.isChecked() and self.proxy_input.text().strip():
            options['proxy'] = self.proxy_input.text().strip()
        
        if self.rate_limit.value() > 0:
            options['ratelimit'] = self.rate_limit.value() * 1024
        
        return options

    def start_worker(self, url, options):
        self.worker = DownloadWorker(url, options)
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.download_finished)
        self.worker.error.connect(self.download_error)
        self.worker.status_update.connect(self.update_status)
        self.worker.start()
        
        self.download_btn.setEnabled(False)
        self.cancel_btn.setEnabled(True)
        self.progress_bar.setValue(0)
        self.status_text.clear()
        self.status_text.append("Starting download...")

    def cancel_download(self):
        if self.worker:
            self.worker.cancel()
            self.status_text.append("Cancelling download...")
            self.cancel_btn.setEnabled(False)

    def clear_data(self):
        self.url_input.clear()
        self.url_list.clear()
        self.progress_bar.setValue(0)
        self.status_text.clear()
        if hasattr(self, 'pending_urls'):
            delattr(self, 'pending_urls')
        if hasattr(self, 'current_url_index'):
            delattr(self, 'current_url_index')
        self.url_list.setPlaceholderText("Imported URLs will appear here")

    def update_progress(self, progress):
        if progress['total'] > 0:
            percentage = (progress['downloaded'] / progress['total']) * 100
            
            self.progress_bar.setValue(int(percentage))
            
            if hasattr(self, 'pending_urls'):
                self.progress_bar.setFormat(f"{percentage:.1f}% (File {self.current_url_index + 1}/{len(self.pending_urls)})")
            else:
                self.progress_bar.setFormat(f"{percentage:.1f}%")
            
            speed = progress.get('speed', 0) / 1024 / 1024  # Convert to MB/s
            eta = progress.get('eta', 0)
            
            status = (f"Downloading {os.path.basename(progress['filename'])}: "
                     f"{progress['downloaded'] / 1024 / 1024:.1f}MB / "
                     f"{progress['total'] / 1024 / 1024:.1f}MB")
            
            if speed > 0:
                status += f" ({speed:.1f} MB/s)"
            if eta > 0:
                status += f" [ETA: {eta}s]"
            
            self.status_text.append(status)

    def update_status(self, message):
        self.status_text.append(message)
        self.status_text.verticalScrollBar().setValue(
            self.status_text.verticalScrollBar().maximum()
        )

    def download_finished(self, success):
        if success:
            if hasattr(self, 'pending_urls'):
                self.current_url_index += 1
                QTimer.singleShot(2000, self.start_bulk_download)
            else:
                self.download_btn.setEnabled(True)
                self.cancel_btn.setEnabled(False)
                self.status_text.append("Download completed successfully!")
                QMessageBox.information(self, "Success", "Download completed successfully!")
        
        self.progress_bar.setValue(100)
        self.update_status_bar()

    def download_error(self, error_msg):
        self.status_text.append(f"Error: {error_msg}")
        self.download_btn.setEnabled(True)
        self.cancel_btn.setEnabled(False)
        self.progress_bar.setValue(0)
        QMessageBox.critical(self, "Error", f"Download failed: {error_msg}")
        
        if hasattr(self, 'pending_urls'):
            self.current_url_index += 1
            QTimer.singleShot(2000, self.start_bulk_download)

    def update_status_bar(self):
        if not hasattr(self, 'status_label'):
            self.status_label = QLabel()
            self.statusBar().addPermanentWidget(self.status_label)
        
        if self.worker and self.worker.isRunning():
            self.status_label.setText("Status: Downloading")
        else:
            self.status_label.setText("Status: Ready")

    def save_settings(self):
        settings = {
            'output_dir': self.output_path.text(),
            'use_proxy': self.use_proxy.isChecked(),
            'proxy_url': self.proxy_input.text(),
            'rate_limit': self.rate_limit.value(),
            'thread_count': self.thread_spin.value(),
            'format': self.format_combo.currentText(),
            'quality': self.quality_combo.currentText(),
            'subtitles': self.subtitle_check.isChecked(),
            'playlist': self.playlist_check.isChecked(),
        }
        
        try:
            settings_path = os.path.join(os.path.expanduser('~'), '.ytdl_settings.json')
            with open(settings_path, 'w') as f:
                json.dump(settings, f, indent=4)
            self.status_text.append("Settings saved successfully!")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to save settings: {str(e)}")

    def load_settings(self):
        try:
            settings_path = os.path.join(os.path.expanduser('~'), '.ytdl_settings.json')
            if os.path.exists(settings_path):
                with open(settings_path, 'r') as f:
                    settings = json.load(f)
                
                if 'output_dir' in settings:
                    self.output_path.setText(settings['output_dir'])
                if 'use_proxy' in settings:
                    self.use_proxy.setChecked(settings['use_proxy'])
                if 'proxy_url' in settings:
                    self.proxy_input.setText(settings['proxy_url'])
                if 'rate_limit' in settings:
                    self.rate_limit.setValue(settings['rate_limit'])
                if 'thread_count' in settings:
                    self.thread_spin.setValue(settings['thread_count'])
                if 'format' in settings:
                    index = self.format_combo.findText(settings['format'])
                    if index >= 0:
                        self.format_combo.setCurrentIndex(index)
                if 'quality' in settings:
                    index = self.quality_combo.findText(settings['quality'])
                    if index >= 0:
                        self.quality_combo.setCurrentIndex(index)
                if 'subtitles' in settings:
                    self.subtitle_check.setChecked(settings['subtitles'])
                if 'playlist' in settings:
                    self.playlist_check.setChecked(settings['playlist'])
        except Exception as e:
            self.status_text.append(f"Note: Using default settings ({str(e)})")

    def closeEvent(self, event):
        if self.worker and self.worker.isRunning():
            reply = QMessageBox.question(
                self,
                "Confirm Exit",
                "A download is in progress. Are you sure you want to exit?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self.worker.cancel()
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

def main():
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
        
    app = QApplication(sys.argv)
    
    # Apply dark theme
    CustomStyle.apply_dark_theme(app)
    
    # Create and show the main window
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()