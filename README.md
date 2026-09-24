# iTalki Language Availability Checker

A small Python script that checks whether a language is open for new teacher applications on [iTalki](https://www.italki.com) and sends a Discord notification when it opens.

iTalki publishes a weekly table of which languages are open or closed for Professional Teacher and Community Tutor applications ([the article is here](https://support.italki.com/hc/en-us/articles/115001499873)). Popular languages like Spanish are often closed, and they can open and close again within the same week. This script checks the table so you don't have to.

## How it works

1. Downloads the article from iTalki's Zendesk Help Center API as JSON.
2. Parses the HTML table inside the article with BeautifulSoup.
3. Finds the row for your language and reads its two statuses.
4. If Community Tutor applications are open, posts a message to a Discord channel through a webhook.

The script uses the Help Center API rather than the regular web page because the page blocks scripted requests (HTTP 403), while the API returns the same content without needing a browser.

Note that iTalki's article says languages *not* listed in the table are open, so if your language disappears from the table, that also means it's open.

## Project structure

```
.
├── check_italki.py            # the checker script
├── test_checker.py            # pytest tests for the API response
├── requirements.txt
├── .env                       # your Discord webhook (not committed)
└── .github/
    └── workflows/
        └── tests.yml          # runs the tests on GitHub Actions
```

## Setup

Clone the repo and install the dependencies:

```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
pip install -r requirements.txt
```

Create a Discord webhook in your server (Channel Settings → Integrations → Webhooks → New Webhook) and copy its URL. Then create a file named `.env` in the project folder:

```
webhook=https://discord.com/api/webhooks/your-webhook-url
```

Make sure `.env` is listed in your `.gitignore`. Anyone with the webhook URL can post to your channel, so it should never be committed.

## Usage

```bash
python check_italki.py
```

It prints the current statuses and sends a Discord message only if the language is open. To check a different language, change `LANGUAGE` at the top of the script to match the name in iTalki's table exactly (for example `"Polish"` or `"Persian (Farsi)"`).

The table updates every Monday, but languages can close at any time once enough people apply, so checking every hour or two is plenty. You can schedule it with cron on macOS/Linux or Task Scheduler on Windows.

## Tests

`test_checker.py` makes a real request to the API and checks that the response still has the shape the script depends on:

- the API returns HTTP 200
- the table's header row is `Language | Professional Teacher | Community Tutor`
- every row has exactly three cells
- every status is either `Open` or `Closed`

If iTalki changes the article's layout, these tests fail and tell you the checker needs updating, rather than the checker silently reading the wrong thing.

Run them with:

```bash
pytest test_checker.py -v
```

## GitHub Actions

The workflow in `.github/workflows/tests.yml` runs the tests automatically whenever you push a change to `check_italki.py`, `test_checker.py`, or `requirements.txt`, and on pull requests that touch those files. Edits to other files, like this README, don't trigger it. You can also run it by hand from the **Actions** tab → **Tests** → **Run workflow**.

To set it up, commit the `.github/workflows/tests.yml` file and push. GitHub picks it up automatically, and results appear under the repo's **Actions** tab, with a green check or red X next to each commit.

The tests don't use the Discord webhook, so no secrets are needed for the workflow.

If the tests pass locally but fail on GitHub with a 403, iTalki is probably blocking GitHub's servers. That's a limit of running from GitHub, not a bug in the script.

## Built with

- [requests](https://requests.readthedocs.io/)
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/)
- [python-dotenv](https://github.com/theskumar/python-dotenv)
- [pytest](https://docs.pytest.org/)
