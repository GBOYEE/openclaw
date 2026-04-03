"""Humanizer skill: make AI output more human-like."""

import random
import re
from pathlib import Path
from typing import Dict, Any
import yaml


class Humanizer:
    """Transform robotic text into conversational human style."""

    def __init__(self, config_path: str = None):
        self.config = self._load_config(config_path)
        self.contractions = self._load_contractions()
        self.hedging_phrases = ["probably", "likely", "it seems", "it looks like", "I think", "maybe"]
        self.filler_words = ["well", "you know", "actually", "I mean"]
        self.emoji_map = {
            "happy": ["😊", "🙂", "🤗"],
            "thinking": ["🤔", "🤷", "🧐"],
            "approval": ["👍", "✅", "👌"],
            "celebration": ["🎉", "🚀", "🔥"],
            "sad": ["😔", "🙁", "😞"],
        }

    def _load_config(self, path: str) -> Dict[str, Any]:
        default = {
            "contraction_probability": 0.8,
            "hedging_strength": 0.3,
            "emoji_frequency": 0.2,
            "exclamation_max": 1,
            "apology_when_appropriate": True,
        }
        if path and Path(path).exists():
            with open(path) as f:
                user = yaml.safe_load(f) or {}
                default.update(user)
        return default

    def _load_contractions(self) -> Dict[str, str]:
        return {
            r"\bI am\b": "I'm",
            r"\bI'm\b": "I'm",  # keep
            r"\bYou are\b": "You're",
            r"\byou're\b": "you're",
            r"\bIt is\b": "It's",
            r"\bIt's\b": "It's",
            r"\bWe are\b": "We're",
            r"\bwe're\b": "we're",
            r"\bThey are\b": "They're",
            r"\bthey're\b": "they're",
            r"\bdo not\b": "don't",
            r"\bdon't\b": "don't",
            r"\bDo not\b": "Don't",
            r"\bDon't\b": "Don't",
            r"\bdoes not\b": "doesn't",
            r"\bdoesn't\b": "doesn't",
            r"\bDid not\b": "Didn't",
            r"\bdid not\b": "didn't",
            r"\bcan not\b": "can't",
            r"\bcannot\b": "can't",
            r"\bI will\b": "I'll",
            r"\bI'll\b": "I'll",
            r"\bI have\b": "I've",
            r"\bI've\b": "I've",
            r"\bI had\b": "I'd",
            r"\bI'd\b": "I'd",
            r"\bwe will\b": "we'll",
            r"\bwe'll\b": "we'll",
        }

    def humanize(self, text: str) -> str:
        # Skip code blocks, JSON, technical content
        if self._is_technical(text):
            return text

        result = text

        # Contractions
        if random.random() < self.config["contraction_probability"]:
            for pattern, repl in self.contractions.items():
                result = re.sub(pattern, repl, result)

        # Hedging (insert sparingly)
        if random.random() < self.config["hedging_strength"]:
            # Insert at beginning of a sentence occasionally
            if random.random() < 0.3 and not result.startswith(("Sure", "Yes", "No", "Here")):
                phrase = random.choice(self.hedging_phrases)
                result = f"{phrase}, {result[0].lower()}{result[1:]}"

        # Filler words at start of some sentences
        if random.random() < 0.15 and "." in result:
            parts = result.split(". ")
            if len(parts) > 1 and random.random() < 0.4:
                filler = random.choice(self.filler_words)
                parts[1] = f"{filler}, {parts[1][0].lower()}{parts[1][1:]}"
                result = ". ".join(parts)

        # Apology for delays/errors if appropriate
        if self.config["apology_when_appropriate"] and any(
            word in result.lower() for word in ["sorry", "apologies", "my bad"]
        ):
            pass  # already has apology
        elif any(word in result.lower() for word in ["error", "failed", "issue", "problem"]):
            if random.random() < 0.5:
                result = "Sorry about that. " + result

        # Exclamation limit
        excls = result.count("!")
        if excls > self.config["exclamation_max"]:
            # Replace extras with period
            count = 0
            new_chars = []
            for c in result:
                if c == "!" and count >= self.config["exclamation_max"]:
                    new_chars.append(".")
                elif c == "!":
                    count += 1
                    new_chars.append(c)
                else:
                    new_chars.append(c)
            result = "".join(new_chars)

        # Emoji (once)
        if random.random() < self.config["emoji_frequency"]:
            emoji_type = random.choice(["happy", "approval"])
            emoji = random.choice(self.emoji_map[emoji_type])
            # Append at end if positive sentiment, else maybe avoid
            result = result.rstrip(" .!") + " " + emoji

        return result

    def _is_technical(self, text: str) -> bool:
        """Heuristically detect code, JSON, logs, CLI output."""
        signals = [
            text.startswith("```"),
            "{" in text and "}" in text and ":" in text and '"' in text,
            re.search(r"at line \d+", text),
            re.search(r"\b(import|def|class|function|var|let|const)\b", text),
            re.search(r"\b\d+\s+\d+\s+\d+", text),  # numbers like file stats
            text.count("\n") > 5 and all(line.startswith((" ", "\t", "  ")) for line in text.split("\n")[:3]),
        ]
        return any(signals)


# Global instance (lazy)
_instance: Humanizer = None


def get_humanizer() -> Humanizer:
    global _instance
    if _instance is None:
        _instance = Humanizer()
    return _instance


def humanize(text: str) -> str:
    return get_humanizer().humanize(text)
