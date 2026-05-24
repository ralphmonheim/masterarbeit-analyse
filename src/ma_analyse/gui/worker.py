"""GUI-Worker-Helfer fuer Hintergrundausgaben."""

from __future__ import annotations


class QueueLogWriter:
    """Leitet stdout/stderr aus dem Worker-Thread in die Tk-Queue."""

    def __init__(self, output_queue):
        self.output_queue = output_queue

    def write(self, text):
        if text:
            self.output_queue.put(("log", text))
        return len(text)

    def flush(self):
        return None
