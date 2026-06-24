"""GUI-Singleton- und Refresh-Koordination."""

from __future__ import annotations

import contextlib
import os
import socket
import threading
import time

GUI_SINGLETON_HOST = "127.0.0.1"
GUI_SINGLETON_PORT = 47683
GUI_SINGLETON_TIMEOUT = 0.35
GUI_REFRESH_TIMEOUT_SECONDS = 20
GUI_REPLACE_TIMEOUT_SECONDS = 10


class GuiInstanceController:
    """Verwaltet die einzelne aktive GUI-Instanz und Fokus-Signale."""

    def __init__(self, host=GUI_SINGLETON_HOST, port=GUI_SINGLETON_PORT):
        self.host = host
        self.port = port
        self.server_socket = None
        self.listener_thread = None
        self.stop_event = threading.Event()
        self.message_handler = None

    def acquire(self):
        if self.server_socket is not None:
            return True

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._set_exclusive_bind(server_socket)
        try:
            server_socket.bind((self.host, self.port))
            server_socket.listen(5)
            server_socket.settimeout(0.5)
        except OSError:
            server_socket.close()
            return False

        self.server_socket = server_socket
        self.stop_event.clear()
        return True

    def _set_exclusive_bind(self, server_socket):
        if os.name == "nt" and hasattr(socket, "SO_EXCLUSIVEADDRUSE"):
            with contextlib.suppress(OSError):
                server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
            return

        with contextlib.suppress(OSError):
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def start_listener(self, message_handler):
        self.message_handler = message_handler
        if self.server_socket is None:
            raise RuntimeError("Listener kann nur nach erfolgreicher Singleton-Akquise gestartet werden.")

        if self.listener_thread is not None and self.listener_thread.is_alive():
            return

        self.listener_thread = threading.Thread(target=self._serve, daemon=True)
        self.listener_thread.start()

    def _serve(self):
        while not self.stop_event.is_set() and self.server_socket is not None:
            try:
                connection, _address = self.server_socket.accept()
            except socket.timeout:
                continue
            except OSError:
                break

            with connection:
                try:
                    payload = connection.recv(1024).decode("utf-8").strip()
                except OSError:
                    payload = ""
                if self.message_handler is not None and payload:
                    try:
                        response = self.message_handler(payload)
                    except Exception:
                        response = "ERROR"
                else:
                    response = "IGNORED"
                try:
                    connection.sendall((response or "OK").encode("utf-8"))
                except OSError:
                    pass

    def stop(self):
        self.stop_event.set()
        if self.server_socket is not None:
            try:
                self.server_socket.close()
            except OSError:
                pass
            self.server_socket = None

    @classmethod
    def send_message(cls, message, host=GUI_SINGLETON_HOST, port=GUI_SINGLETON_PORT, timeout=GUI_SINGLETON_TIMEOUT):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(timeout)
        try:
            client.connect((host, port))
            client.sendall(message.encode("utf-8"))
            response = client.recv(1024).decode("utf-8").strip()
            return response or None
        finally:
            client.close()


class GuiRefreshCoordinator:
    """Koordiniert den sicheren Übergang von alter zu neuer GUI-Instanz."""

    def __init__(self, gui):
        self.gui = gui
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((GUI_SINGLETON_HOST, 0))
        self.server_socket.listen(5)
        self.server_socket.settimeout(0.5)
        self.port = self.server_socket.getsockname()[1]
        self.stop_event = threading.Event()
        self.listener_thread = threading.Thread(target=self._serve, daemon=True)
        self.released_singleton = False
        self.completed = False

    def start(self):
        self.listener_thread.start()
        return self.port

    def _serve(self):
        while not self.stop_event.is_set():
            try:
                connection, _address = self.server_socket.accept()
            except socket.timeout:
                continue
            except OSError:
                break

            with connection:
                try:
                    payload = connection.recv(1024).decode("utf-8").strip()
                except OSError:
                    payload = ""
                response = self._handle_message(payload)
                try:
                    connection.sendall(response.encode("utf-8"))
                except OSError:
                    pass

    def _handle_message(self, payload):
        if payload == "REQUEST_RELEASE":
            released = self.gui.root.after(0, self.gui._release_singleton_for_refresh)
            del released
            deadline = time.time() + 5
            while time.time() < deadline:
                if self.released_singleton:
                    self.gui.root.after(0, self.gui._schedule_refresh_timeout_recovery)
                    return "RELEASED"
                time.sleep(0.05)
            return "FAILED"

        if payload == "NEW_GUI_ACTIVE":
            self.completed = True
            self.gui.root.after(0, self.gui._finalize_refresh_shutdown)
            return "ACK"

        return "IGNORED"

    def mark_released(self):
        self.released_singleton = True

    def close(self):
        self.stop_event.set()
        if self.server_socket is not None:
            try:
                self.server_socket.close()
            except OSError:
                pass
            self.server_socket = None


def send_refresh_message(port, message, timeout=5):
    """Sendet eine Steuerungsnachricht an den temporären GUI-Refresh-Server."""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(timeout)
    try:
        client.connect((GUI_SINGLETON_HOST, port))
        client.sendall(message.encode("utf-8"))
        return client.recv(1024).decode("utf-8").strip()
    finally:
        client.close()
