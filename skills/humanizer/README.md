# Humanizer Skill

Make AI responses more human: add empathy, warmth, contractions, personality variability, and natural phrasing.

## Usage

This skill modifies outgoing messages to sound less robotic and more conversational.

### Features

- Contractions: "I am" → "I'm", "do not" → "don't"
- hedging: add "probably", "likely", "seems" (configurable)
- filler words: occasional "well", "you know", "actually"
- emoji: selective 😊, 👍, 🤔 based on context
- exclamation sparingly: "Great!" vs "Great."
- apologies when appropriate: "Sorry for the delay"
- hedging with uncertainty: "It looks like..." vs "It is..."

### Configuration (optional)

Create `skills/humanizer/config.yaml`:

```yaml
contraction_probability: 0.8
hedging_strength: 0.3  # 0 = none, 1 = heavy
emoji_frequency: 0.2   # chance to add relevant emoji
exclamation_max: 1     # max per response
apology_when_appropriate: true
```

## Integration

This skill intercepts outgoing messages from the assistant and applies humanization transforms. It respects do-not-humanize tags for technical outputs (code, JSON, logs).

Enable in agent config:
```yaml
skills:
  - humanizer
```