import asyncio
import time
from typing import Callable, Dict, Any

class TaskScheduler:
    def __init__(self):
        self.tasks = []
        self.running = False

    def add_interval(self, func: Callable, seconds: float, args: Dict[str, Any] = None):
        self.tasks.append({
            "type": "interval",
            "func": func,
            "seconds": seconds,
            "args": args or {},
            "last_run": 0
        })

    def add_cron(self, func: Callable, cron_rule: Dict[str, Any], args: Dict[str, Any] = None):
        self.tasks.append({
            "type": "cron",
            "func": func,
            "cron": cron_rule,
            "args": args or {},
            "last_match": None
        })

    async def start(self):
        self.running = True
        while self.running:
            now = time.time()
            for t in self.tasks:
                if t["type"] == "interval":
                    if now - t["last_run"] >= t["seconds"]:
                        await self._exec(t)
                        t["last_run"] = now
                elif t["type"] == "cron":
                    if self._cron_match(t["cron"]):
                        if t["last_match"] != self._cron_stamp():
                            await self._exec(t)
                            t["last_match"] = self._cron_stamp()
            await asyncio.sleep(0.1)

    async def _exec(self, task):
        f = task["func"]
        args = task["args"]
        if asyncio.iscoroutinefunction(f):
            await f(**args)
        else:
            f(**args)

    def stop(self):
        self.running = False

    def _cron_stamp(self):
        t = time.localtime()
        return (t.tm_min, t.tm_hour, t.tm_mday, t.tm_mon, t.tm_wday)

    def _cron_match(self, rule):
        t = time.localtime()
        return (
            (rule["minute"] in [t.tm_min, "*"]) and
            (rule["hour"] in [t.tm_hour, "*"]) and
            (rule["day"] in [t.tm_mday, "*"]) and
            (rule["month"] in [t.tm_mon, "*"]) and
            (rule["weekday"] in [t.tm_wday, "*"])
        )
