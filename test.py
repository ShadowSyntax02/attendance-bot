name: Attendance Bot

on:
  schedule:
    - cron: '0 4 * * 1-5'   # 9:30 AM IST
    - cron: '0 13 * * 1-5'  # 6:30 PM IST
  workflow_dispatch:

jobs:
  run-bot:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repo
        uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          pip install playwright
          playwright install

      - name: Run bot
        run: python test.py
