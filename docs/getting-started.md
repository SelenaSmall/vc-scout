# Getting started

Prerequisites:
- [asdf](https://asdf-vm.com/) with the Python plugin
- An [Anthropic API key](https://console.anthropic.com/settings/keys) exported in your shell profile

## 1. Clone repo

```bash
  git clone git@github.com:SelenaSmall/vc-scout.git
```

## 2. Install Python

```bash
  asdf install
```

## 3. Set up API key

Add to your shell profile (`~/.zshrc` or `~/.bashrc`):

```bash
  export ANTHROPIC_API_KEY=sk-ant-...
```

Then restart your terminal or `source` the profile.

## 4. Install dependencies

```bash
  make setup
```

## 5. Run the agent

```bash
  make run
```

By default, `make run` runs in **test mode** — output goes to gitignored files under `test/`, keeping production data clean.

To run against production data:

```bash
  VC_SCOUT_MODE=production make run
```

GitHub Actions sets `VC_SCOUT_MODE=production` automatically.
