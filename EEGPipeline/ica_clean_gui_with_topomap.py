
import mne
import numpy as np
import pyedflib
import sys
from PyQt5 import QtWidgets
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class ICAViewer(QtWidgets.QMainWindow):
    def __init__(self, raw, ica):
        super().__init__()
        self.raw = raw
        self.ica = ica
        self.selected_component = None
        self.exclude_list = set()

        self.setWindowTitle("ICA Viewer - EEG Artifact Removal Tool")
        self.setGeometry(100, 100, 1400, 800)

        self.initUI()

    def initUI(self):
        layout = QtWidgets.QHBoxLayout()
        left_layout = QtWidgets.QVBoxLayout()
        right_layout = QtWidgets.QVBoxLayout()

        self.grid_widget = QtWidgets.QWidget()
        self.grid_layout = QtWidgets.QGridLayout()
        self.grid_widget.setLayout(self.grid_layout)
        left_layout.addWidget(QtWidgets.QLabel("ICA Components:"))
        left_layout.addWidget(self.grid_widget)

        self.buttons = []
        for i in range(self.ica.n_components_):
            btn = QtWidgets.QPushButton(f"ICA {i}")
            btn.clicked.connect(lambda _, x=i: self.plot_component(x))
            self.buttons.append(btn)
            self.grid_layout.addWidget(btn, i // 5, i % 5)

        self.fig, self.ax = plt.subplots(2, 2, figsize=(10, 8))
        self.canvas = FigureCanvas(self.fig)
        right_layout.addWidget(self.canvas)

        self.input_field = QtWidgets.QLineEdit()
        self.input_field.setPlaceholderText("Enter ICA components to exclude (e.g., 0,2,5)")
        right_layout.addWidget(self.input_field)

        self.exclude_button = QtWidgets.QPushButton("Apply Exclusion and Export EDF")
        self.exclude_button.clicked.connect(self.apply_and_export)
        right_layout.addWidget(self.exclude_button)

        layout.addLayout(left_layout, 1)
        layout.addLayout(right_layout, 3)

        container = QtWidgets.QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def plot_component(self, index):
        self.selected_component = index
        for axis in self.ax.flatten():
            axis.clear()

        source_data = self.ica.get_sources(self.raw).get_data()[index]
        times = self.raw.times
        self.ax[0, 1].plot(times, source_data)
        self.ax[0, 1].set_title(f"ICA {index} - Time Domain")

        psd = np.abs(np.fft.rfft(source_data))**2
        freqs = np.fft.rfftfreq(len(source_data), 1 / self.raw.info['sfreq'])
        self.ax[1, 1].semilogy(freqs, psd)
        self.ax[1, 1].set_title(f"ICA {index} - Power Spectral Density")

        self.ica.plot_components(picks=[index], axes=self.ax[0, 0], colorbar=False, show=False)
        self.ax[0, 0].set_title(f"ICA {index} - Topomap")
        self.ax[1, 0].axis("off")

        self.canvas.draw()

    def apply_and_export(self):
        text = self.input_field.text()
        self.exclude_list = [int(x.strip()) for x in text.split(",") if x.strip().isdigit()]
        self.ica.exclude = self.exclude_list
        raw_clean = self.ica.apply(self.raw.copy())

        output_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save EDF", "", "EDF files (*.edf)")
        if output_path:
            self.export_to_edf(raw_clean, output_path)
            QtWidgets.QMessageBox.information(self, "Export Complete", f"Cleaned data saved to:\n{output_path}")

    def export_to_edf(self, raw, filename):
        eeg_data, _ = raw.get_data(return_times=True)
        ch_names = raw.ch_names
        sfreq = int(raw.info['sfreq'])
        n_channels, _ = eeg_data.shape

        f = pyedflib.EdfWriter(filename, n_channels=n_channels, file_type=pyedflib.FILETYPE_EDFPLUS)
        channel_info = []
        for ch in ch_names:
            channel_info.append({
                'label': ch,
                'dimension': 'uV',
                'sample_rate': sfreq,
                'physical_min': -32768,
                'physical_max': 32767,
                'digital_min': -32768,
                'digital_max': 32767,
                'transducer': '',
                'prefilter': ''
            })
        f.setSignalHeaders(channel_info)
        scaled_data = eeg_data * 1e6
        scaled_data = np.clip(scaled_data, -32768, 32767).astype(np.int16)
        f.writeSamples(scaled_data)
        f.close()


def launch_gui():
    app = QtWidgets.QApplication(sys.argv)
    bdf_path, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Select BDF File", "", "BDF files (*.bdf)")
    if not bdf_path:
        return

    raw = mne.io.read_raw_bdf(bdf_path, preload=True)
    raw.pick_types(eeg=True)

    montage = mne.channels.make_standard_montage('standard_1020')
    raw.drop_channels([ch for ch in raw.ch_names if ch not in montage.ch_names])
    raw.set_montage(montage)

    raw.notch_filter(50)
    raw.filter(8, 40)
    raw.set_eeg_reference('average')

    ica = mne.preprocessing.ICA(n_components=62, method='fastica', random_state=97, max_iter='auto')
    ica.fit(raw)

    viewer = ICAViewer(raw, ica)
    viewer.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    launch_gui()
