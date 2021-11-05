import logging
import traceback
from dataclasses import dataclass, asdict, field
from typing import Optional


class StatusDescription(object):

    def __init__(self):
        self.__is_status_manual_changed = False

    def __set__(self, instance, value):
        if not self.__is_status_manual_changed:
            instance.__status = value
            self.__is_status_manual_changed = True

    def __get__(self, instance, owner):
        return instance.__status


@dataclass(eq=False, order=False)
class ReplyData(object):
    status: StatusDescription = field(default_factory=StatusDescription)
    code: Optional[int] = None
    exception: Optional[Exception] = None
    message: Optional[str] = None
    exc_message: Optional[str] = None
    exc_traceback: Optional[str] = None
    extra_data: dict = field(default_factory=dict)

    def delete(self, key):
        del self.extra_data[key]

    def clear(self):
        self.extra_data.clear()

    def update(self, extra_dict: dict):
        if isinstance(extra_dict, dict):
            self.extra_data.update(extra_dict)
        else:
            self.logger.warning(
                f"Replay data cannot be update, because expected dict parameter, but got {type(extra_dict)}"
            )

    def as_dict(self):
        self_dict = asdict(self)
        self_dict.pop("exception")
        extra_data = self_dict.pop("extra_data")
        return {**self_dict, **extra_data}

    def _format_exception_traceback(self, exception, default_formatted=False, inline=True):
        _traceback = traceback.extract_tb(exception.__traceback__).format()
        if default_formatted:
            return _traceback
        _traceback_inline = " ".join(_traceback)
        if inline:
            return _traceback_inline
        else:
            return _traceback_inline.replace("\\n", "\\n")

    def __post_init__(self):
        if isinstance(self.exception, Exception):
            self.exc_message = str(self.exception)
            self.exc_traceback = self._format_exception_traceback(self.exception, inline=False)
        self.logger = logging.getLogger("scrapy")
