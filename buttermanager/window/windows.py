#!/usr/bin/env python3
#
# -*- coding: utf-8 -*-
#
# Copyright 2018-2019 Eloy García Almadén <eloy.garcia.pca@gmail.com>
#
# This file is part of buttermanager.
#
# This program is free software: you can redistribute it and / or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""This module gathers all the additional windows for displaying information in the application.

"""
import util.settings
import sys
from PyQt5.QtWidgets import QDesktopWidget, QDialog, QMainWindow, QFileDialog
from PyQt5 import uic, QtCore
from PyQt5.QtCore import pyqtSignal, QSize, Qt
from PyQt5.QtGui import QIcon, QTextCursor, QFontMetrics


class InfoWindow(QDialog):
    """Window to display information.

    """
    # Constructor
    def __init__(self, parent, information):
        QDialog.__init__(self, parent)
        # Setting window flags, f.i. this window won't have a close button
        self.setWindowFlags(
            QtCore.Qt.Window |
            QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.WindowTitleHint |
            QtCore.Qt.WindowMinimizeButtonHint |
            QtCore.Qt.WindowStaysOnTopHint
        )
        self.parent = parent

        # Initializing the window
        self.init_ui(information)

    def init_ui(self, information):
        """Initializes the Graphic User Interface.

        """
        # Loading User Interface
        uic.loadUi("ui/InfoWindow.ui", self)

        # Setting the window icon
        self.setWindowIcon(QIcon('images/buttermanager50.png'))

        # Setting maximum and minimum  size for the main window
        self.setMinimumHeight(240)
        self.setMinimumWidth(320)
        self.setMaximumHeight(240)
        self.setMaximumWidth(320)

        # Centering the window
        qt_rectangle = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        qt_rectangle.moveCenter(center_point)
        self.move(qt_rectangle.topLeft())

        # Setting information
        self.label_info.setText(information)


class GeneralInfoWindow(QDialog):
    """Window to display generic information.

    """
    # Constructor
    def __init__(self, parent, information):
        QDialog.__init__(self, parent)
        # Setting window flags, f.i. this window won't have a close button
        self.setWindowFlags(
            QtCore.Qt.Window |
            QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.WindowTitleHint |
            QtCore.Qt.WindowStaysOnTopHint
        )
        self.parent = parent

        # Initializing the window
        self.init_ui(information)

    def init_ui(self, information):
        """Initializes the Graphic User Interface.

        """
        # Loading User Interface
        uic.loadUi("ui/GeneralInfoWindow.ui", self)

        # Setting the window icon
        self.setWindowIcon(QIcon('images/buttermanager50.png'))

        # Setting maximum and minimum  size for the main window
        self.setMinimumHeight(285)
        self.setMinimumWidth(420)
        self.setMaximumHeight(285)
        self.setMaximumWidth(420)

        # Centering the window
        qt_rectangle = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        qt_rectangle.moveCenter(center_point)
        self.move(qt_rectangle.topLeft())

        # Setting information
        self.label_info.setText(information)


class SnapshotWindow(QMainWindow):
    """Window to select a subvolume to take a snapshot.

    """
    # pyqtSignal that will be emitted when this class requires that main
    # window refreshes GUI
    refresh_gui = pyqtSignal()

    # Constructor
    def __init__(self, parent):
        QMainWindow.__init__(self, parent)
        self.parent = parent
        # Logger
        self.__logger = util.utils.Logger(self.__class__.__name__).get()

        # Initializing the window
        self.init_ui()

    def init_ui(self):
        """Initializes the Graphic User Interface.

        """
        # Loading User Interface
        uic.loadUi("ui/SnapshotWindow.ui", self)

        # Setting the window icon
        self.setWindowIcon(QIcon('images/buttermanager50.png'))

        # Setting maximum and minimum  size for the main window
        self.setMinimumHeight(300)
        self.setMinimumWidth(640)
        self.setMaximumHeight(300)
        self.setMaximumWidth(640)

        # Centering the window
        qt_rectangle = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        qt_rectangle.moveCenter(center_point)
        self.move(qt_rectangle.topLeft())

        # Loading GUI components
        self.enable_all_subvolumes()

        # Retrieveing subvolumes
        subvolumes = []
        for subvolume in util.settings.subvolumes:
            subvolumes.append(subvolume)
        self.combobox_subvolumes.addItems(subvolumes)

        # Button events
        self.radiobutton_all_subvolumes.clicked.connect(self.enable_all_subvolumes)
        self.radiobutton_one_subvolume.clicked.connect(self.enable_one_subvolume)
        self.button_ok.clicked.connect(self.take_snapshot)
        self.button_cancel.clicked.connect(self.cancel)

    def enable_all_subvolumes(self):
        """Enables all subvolumes option.

        """
        self.radiobutton_all_subvolumes.setEnabled(True)
        self.radiobutton_all_subvolumes.setChecked(True)
        self.radiobutton_one_subvolume.setEnabled(True)
        self.radiobutton_one_subvolume.setChecked(False)
        self.combobox_subvolumes.setEnabled(False)

    def enable_one_subvolume(self):
        """Enables one subvolume option.

        """
        self.radiobutton_all_subvolumes.setEnabled(True)
        self.radiobutton_all_subvolumes.setChecked(False)
        self.radiobutton_one_subvolume.setEnabled(True)
        self.radiobutton_one_subvolume.setChecked(True)
        self.combobox_subvolumes.setEnabled(True)

    def take_snapshot(self):
        """Takes a snapshot of the selected subvolume.

        """
        if self.radiobutton_all_subvolumes.isChecked():
            for subvolume in util.settings.subvolumes:
                util.settings.subvolumes[subvolume].create_snapshot()
        else:
            subvolume_selected = self.combobox_subvolumes.currentText()
            util.settings.subvolumes[subvolume_selected].create_snapshot()

        # Refreshing GUI
        self.on_refresh_gui()

        # Closes the window
        self.cancel()

    def cancel(self):
        """Closes the window.

        """
        self.close()

    def on_refresh_gui(self):
        """Emits a QT Signal to refresh main window GUI.

        """
        self.refresh_gui.emit()


class SubvolumeWindow(QMainWindow):
    """Window to add a new subvolume to be managed byt the application.

    """
    # pyqtSignal that will be emitted when this class requires that main
    # window refreshes GUI
    refresh_gui = pyqtSignal()

    # Constructor
    def __init__(self, parent):
        QMainWindow.__init__(self, parent)
        self.parent = parent
        # Logger
        self.__logger = util.utils.Logger(self.__class__.__name__).get()

        # Initializing the window
        self.init_ui()

    def init_ui(self):
        """Initializes the Graphic User Interface.

        """
        # Loading User Interface
        uic.loadUi("ui/SubvolumeWindow.ui", self)

        # Setting the window icon
        self.setWindowIcon(QIcon('images/buttermanager50.png'))

        # Setting maximum and minimum  size for the main window
        self.setMinimumHeight(300)
        self.setMinimumWidth(640)
        self.setMaximumHeight(300)
        self.setMaximumWidth(640)

        # Centering the window
        qt_rectangle = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        qt_rectangle.moveCenter(center_point)
        self.move(qt_rectangle.topLeft())

        # Loading icons
        self.button_add_subvolume_orig.setIcon(QIcon('images/open_folder_24px_icon.png'))
        self.button_add_subvolume_orig.setIconSize(QSize(24, 24))
        self.button_add_subvolume_dest.setIcon(QIcon('images/open_folder_24px_icon.png'))
        self.button_add_subvolume_dest.setIconSize(QSize(24, 24))

        # Button events
        self.button_add_subvolume_orig.clicked.connect(self.add_subvolume_orig)
        self.button_add_subvolume_dest.clicked.connect(self.add_subvolume_dest)
        self.button_ok.clicked.connect(self.add_subvolume)
        self.button_cancel.clicked.connect(self.cancel)

    def add_subvolume_orig(self):
        """Adds the origin path for the subvolume to manage.

        """
        # Creating a QFileDialog to select the directory
        # Only directories will be allowed
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.Directory)
        file_dialog.setOption(QFileDialog.ShowDirsOnly, True)

        if file_dialog.exec_():
            self.line_subvolume_origin.setText(file_dialog.selectedFiles()[0])

    def add_subvolume_dest(self):
        """Adds the destination where the snapshot of the subvolume will be stored.

        """
        # Creating a QFileDialog to select the directory
        # Only directories will be allowed
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.Directory)
        file_dialog.setOption(QFileDialog.ShowDirsOnly, True)

        if file_dialog.exec_():
            self.line_subvolume_dest.setText(file_dialog.selectedFiles()[0])

    def add_subvolume(self):
        """Adds a new subvolume to be managed by the application.

        """
        # All the fields must be filled
        origin = self.line_subvolume_origin.text()
        dest = self.line_subvolume_dest.text()
        name = self.line_snapshot_name.text()
        if not origin or not dest or not name:
            info_dialog = GeneralInfoWindow(self, "Please, fill all the fields.")
            info_dialog.show()
        else:
            # Adding a new subvolume
            util.settings.properties_manager.set_subvolume(origin, dest, name)

            # Refreshing GUI
            self.on_refresh_gui()

            # Closes the window
            self.cancel()

    def cancel(self):
        """Closes the window.

        """
        self.close()

    def on_refresh_gui(self):
        """Emits a QT Signal to refresh main window GUI.

        """
        self.refresh_gui.emit()


class UpdatesWindow(QMainWindow):
    """Window to check new updates and start the upgrading process.

    """
    # pyqtSignal that will be emitted when this class requires to upgrade
    # the system with snapshots
    upgrade_system = pyqtSignal()

    # pyqtSignal that will be emitted when this class requires to upgrade
    # the system without snapshots
    upgrade_system_without_snanpshots = pyqtSignal()

    # Constructor
    def __init__(self, parent, command_line_text):
        """ Constructor.

        Arguments:
            command_line_text (list(:obj:`str`)): Packages obtained from command line to be updated. One per line.
        """
        QMainWindow.__init__(self, parent)
        self.parent = parent

        # UI elements
        self.__ui_elements = []

        # Logger
        self.__logger = util.utils.Logger(self.__class__.__name__).get()

        # Command line text
        self.__command_line_text = command_line_text

        # Initializing the window
        self.init_ui()

    def init_ui(self):
        """Initializes the Graphic User Interface.

        """
        # Loading User Interface
        uic.loadUi("ui/UpdatesWindow.ui", self)

        # Setting the window icon
        self.setWindowIcon(QIcon('images/buttermanager50.png'))

        # Adjusting font scale
        # UI elements
        self.__ui_elements = [self.button_upgrade_system, self.button_cancel,
                              self.button_upgrade_system_without_snapshots, self.label_updates, self.text_edit_console]
        util.utils.scale_fonts(self.__ui_elements)
        # Tooltips
        self.setStyleSheet(" QToolTip{font: " + str(util.settings.base_font_size) + "pt}")

        # Setting maximum and minimum  size for the main window
        self.setMinimumHeight(442)
        self.setMinimumWidth(767)
        self.setMaximumHeight(442)
        self.setMaximumWidth(767)

        # Centering the window
        qt_rectangle = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        qt_rectangle.moveCenter(center_point)
        self.move(qt_rectangle.topLeft())

        # Displaying packages to be updated
        for line in self.__command_line_text.split("\n"):
            self.text_edit_console.moveCursor(QTextCursor.End)
            self.text_edit_console.insertHtml(line + '<br>')
            self.text_edit_console.moveCursor(QTextCursor.End)

        # Hiding upgrade button with snapshots if there is no subvolume defined
        if len(util.settings.subvolumes) == 0:
            self.button_upgrade_system.hide()

        # Button events
        self.button_upgrade_system.clicked.connect(self.full_system_upgrade)
        self.button_upgrade_system_without_snapshots.clicked.connect(self.full_system_upgrade_without_snapshots)
        self.button_cancel.clicked.connect(self.cancel)

    def full_system_upgrade(self):
        """Upgrades the system doing snapshots.

        """
        # The main window will upgrade the system
        self.upgrade_system.emit()

        # Closes the window
        self.cancel()

    def full_system_upgrade_without_snapshots(self):
        """Upgrades the system without doing snapshots.

        """
        # The main window will upgrade the system
        self.upgrade_system_without_snanpshots.emit()

        # Closes the window
        self.cancel()

    def cancel(self):
        """Closes the window.

        """
        self.close()


class ProblemsFoundWindow(QMainWindow):
    """Window to display problems found.

    Those problems will cause the application exits.
    """

    # Constructor
    def __init__(self, parent, information):
        QMainWindow.__init__(self, parent)
        self.setWindowFlags(
            QtCore.Qt.Window |
            QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.WindowTitleHint |
            QtCore.Qt.WindowStaysOnTopHint
        )
        self.parent = parent

        # UI elements
        self.__ui_elements = []

        # Initializing the window
        self.init_ui(information)

    def init_ui(self, information):
        """Initializes the Graphic User Interface.

        """
        # Loading User Interface
        uic.loadUi("ui/ProblemsFoundWindow.ui", self)

        # Setting the window icon
        self.setWindowIcon(QIcon('images/buttermanager50.png'))

        # Adjusting font scale
        # UI elements
        self.__ui_elements = [self.label_info, self.button_ok]
        util.utils.scale_fonts(self.__ui_elements)
        # Tooltips
        self.setStyleSheet(" QToolTip{font: " + str(util.settings.base_font_size) + "pt}")

        # Setting maximum and minimum  size for the main window
        self.setMinimumHeight(285)
        self.setMinimumWidth(420)
        self.setMaximumHeight(285)
        self.setMaximumWidth(420)

        # Centering the window
        qt_rectangle = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        qt_rectangle.moveCenter(center_point)
        self.move(qt_rectangle.topLeft())

        # Setting information
        self.label_info.setText(information)

        # Button events
        self.button_ok.clicked.connect(self.exit)

    def exit(self):
        """Exits the application.

        """
        self.close()
        sys.exit()


class LogViewWindow(QMainWindow):
    """Window display a log.

    """
    # Constructor
    def __init__(self, parent, log_path):
        """ Constructor.

        Arguments:
            log_path (string): Path of the log that the user wants to see.
        """
        QMainWindow.__init__(self, parent)
        self.parent = parent
        # UI elements
        self.__ui_elements = []
        # Logger
        self.__logger = util.utils.Logger(self.__class__.__name__).get()

        # Command line text
        self.__log_path = log_path

        # Initializing the window
        self.init_ui()

    def init_ui(self):
        """Initializes the Graphic User Interface.

        """
        # Loading User Interface
        uic.loadUi("ui/LogViewWindow.ui", self)

        # Setting the window icon
        self.setWindowIcon(QIcon('images/buttermanager50.png'))

        # Adjusting font scale
        # UI elements
        self.__ui_elements = [self.label_log, self.text_log]
        util.utils.scale_fonts(self.__ui_elements)
        # Tooltips
        self.setStyleSheet(" QToolTip{font: " + str(util.settings.base_font_size) + "pt}")

        # Setting maximum and minimum  size for the main window
        self.setMinimumHeight(442)
        self.setMinimumWidth(767)
        self.setMaximumHeight(442)
        self.setMaximumWidth(767)

        # Centering the window
        qt_rectangle = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        qt_rectangle.moveCenter(center_point)
        self.move(qt_rectangle.topLeft())

        # Displaying the log
        log_file = open(self.__log_path, 'r')

        for line in log_file:
            self.text_log.moveCursor(QTextCursor.End)
            self.text_log.insertHtml(line + '<br>')
            self.text_log.moveCursor(QTextCursor.End)