import numpy as np
import asyncio

class SentimentManager:
    def __init__(self, cfg, model, news, twitter, reddit):
        self.cfg = cfg
        self.model = model
        self.news = news
        self.twitter = twitter
        self.reddit = reddit
        self.state = {"score": 0, "volume": 0, "trend": 0}

    async def update(self):
        texts = []

        n = await self.news.fetch()
        t = await self.twitter.fetch()
        r = await self.reddit.fetch()

        for a in n:
            texts.append(a.get("title", ""))
        for tw in t:
            texts.append(tw.get("text", ""))
        for rd in r:
            texts.append(rd.get("title", ""))

        if not texts:
            return self.state

        scores = []
        confs = []

        for tx in texts[: self.cfg.get("max_items", 40)]:
            s, c = self.model.score(tx)
            scores.append(s)
            confs.append(c)

        s_avg = float(np.mean(scores))
        c_avg = float(np.mean(confs))
        t = self._trend(scores)

        self.state = {
            "score": s_avg * c_avg,
            "volume": len(texts),
            "trend": t
        }
        return self.state

    def _trend(self, arr):
        x = np.array(arr)
        if len(x) < 3:
            return 0
        return float(np.polyfit(range(len(x)), x, 1)[0])

    def snapshot(self):
        return self.state
