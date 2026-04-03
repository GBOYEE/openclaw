# Contributing to OpenClaw

Thank you for contributing! Please follow these guidelines.

## Getting Started

1. Fork the repo
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/openclaw.git`
3. Create a branch: `git checkout -b my-feature-branch`
4. Make changes and test
5. Commit: `git commit -am 'Add feature'`
6. Push: `git push origin my-feature-branch`
7. Open a Pull Request

## Development Setup

- Install dependencies: `pip install -r requirements.txt` (if present)
- Install Node dependencies if needed: `npm install`
- Copy `.env.example` to `.env` and configure
- Run the gateway: `python -m openclaw.gateway` or see README

## Code Style

- Python: PEP 8, use `black` and `ruff`
- YAML: 2-space indent, no tabs
- Commit messages: conventional commits

## Pull Request Process

- CI must pass (lint, tests, markdown lint)
- PR must be reviewed by at least one maintainer
- Squash merge preferred

## Branch Protection

`main` is protected. Direct pushes are prohibited. All changes via PRs.

## Code of Conduct

This project adheres to the [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you agree to uphold it.

## Questions?

Open an issue with the `question` template or start a discussion.

Thank you for improving OpenClaw!