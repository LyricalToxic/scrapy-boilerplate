import logging
import traceback
from dataclasses import dataclass, asdict, fields, field
from typing import Optional


@dataclass(eq=False, order=False)
class ReplayData(object):
    status: int = 1
    exception: Optional[Exception] = None
    message: Optional[str] = None
    exc_message: Optional[str] = None
    exc_traceback: Optional[str] = None
    extra_data: dict = field(default_factory=dict)

    def _format_exception_traceback(self, exception, default_formatted=False, inline=True):
        _traceback = traceback.extract_tb(exception.__traceback__).format()
        if default_formatted:
            return _traceback
        _traceback_inline = " ".join(_traceback)
        if inline:
            return _traceback_inline
        else:
            return _traceback.replace("\\n", "\\n")

    def update(self, extra_dict: dict):
        if isinstance(extra_dict, dict):
            self.extra_data.update(extra_dict)
        else:
            logging.warning(
                f"Replay data cannot be update, because expected dict parameter, but got {type(extra_dict)}"
            )

    def delete(self, key):
        del self.extra_data[key]

    def __post_init__(self):
        if isinstance(self.exception, Exception):
            self.exc_message = str(self.exception)
            self.exc_traceback = self._format_exception_traceback(self.exception, inline=False)

    def as_dict(self):
        self_dict = asdict(self)
        extra_data = self_dict.pop("extra_data")
        return {**self_dict, **extra_data}
