<table align="center">
  <tr>
    <td>
<pre>
 ██████╗ ██╗ ██████╗ ███████╗
 ██╔══██╗██║ ██╔══██╗██╔════╝
 ██║  ██║██║ ██████╔╝███████╗
 ██║  ██║██║ ██╔══██╗╚════██║
 ██████╔╝██║ ██████╔╝███████║
 ╚═════╝ ╚═╝ ╚═════╝ ╚══════╝
</pre>
    </td>
  </tr>
</table>

<p align="center"><strong>Get an email the moment a company you care about posts a new internship, before the pile-up, instead of refreshing a job board.</strong></p>

---

Dibs watches the [SimplifyJobs Summer2026](https://github.com/SimplifyJobs/Summer2026-Internships)
listings every 15 minutes, keeps only the ones matching your watchlist, and
emails you the new ones. It runs entirely on GitHub Actions for free. Your
computer is only needed if you want to test things locally.

**vs. SWEList:** SWEList emails every new posting, batched once a day. Dibs adds
per-company filtering, so you only hear about roles you'd actually apply to, and
it checks every 15 minutes instead of daily. Think of it as the filtered,
near-real-time version of the same idea.

## How it works

On each run Dibs downloads the listings, keeps the ones that are active and
visible, matches them against your `config.yaml`, emails you anything new, and
records the IDs it sent in `state.json` so it never emails the same role twice.
Matching is keyed on each listing's stable ID, so edits to a posting never
re-notify you. The first run records everything currently open without emailing,
so you don't get one giant backlog message. Every run after that emails only
genuinely new roles.

## Setup

The whole thing takes about five minutes in the browser. No local install
required.

1. **Make your own copy.** Click
   **"Use this template" → Create a new repository**. Use this template, not
   Fork. Your copy holds your watchlist, your email secrets, and your state,
   all separate from the original. Make it private if you want.
2. **Turn on Actions.** Open the **Actions** tab in your copy and click the
   button to enable workflows.
3. **Pick your companies.** Open `config.yaml` (the pencil icon edits it right
   in the browser) and list the companies you care about:

   ```yaml
   companies:
     - Stripe                    # every Stripe role
     - name: Google
       roles: [software, swe]    # only titles containing these words
   ```

   Names are matched loosely, so `Jane Street` finds `Jane Street Capital`.
   If a company you expect never shows up, run `python companies.py` locally
   to print the exact names in the data and paste one in.
4. **Add your email secrets.** Go to
   **Settings → Secrets and variables → Actions** and add three repository
   secrets:

   | Secret | Value |
   | --- | --- |
   | `GMAIL_USER` | the Gmail address you send from |
   | `GMAIL_APP_PASSWORD` | a 16-character [app password](https://support.google.com/accounts/answer/185833) (your account needs 2-step verification on) |
   | `RECIPIENT` | where alerts go. Optional; defaults to `GMAIL_USER` |

5. **Kick off the first run.** Back in the **Actions** tab, open the
   **dibs poll** workflow and click **Run workflow**. This records what's
   currently open without emailing you. From here on the schedule takes over
   and you get an email whenever a matching role appears.

That's it. Everything runs on GitHub's servers on a timer. You can close the tab.

## Adjusting the watchlist later

Edit `config.yaml` and commit. Changes apply on the next scheduled run. A company
with no `roles:` list matches all of its postings; add `roles:` to narrow it to
titles containing those words. Matching ignores case and punctuation and drops
Inc/LLC/Corp, so exact capitalization doesn't matter. One caveat: it's a
substring match, so very short names can catch extras (`meta` also matches
"Metabase"). Paste the exact name from `companies.py` if you see noise.

## Changing how often it checks

The schedule lives in `.github/workflows/poll.yml`, in the `cron:` line, not in
`config.yaml`. GitHub reads the timer from the workflow file. The shortest
interval GitHub allows is 5 minutes, and scheduled runs can drift or be skipped
when GitHub is busy.

## Good to know

- `state.json` is committed back to your repo whenever it changes. Stateless
runners have no other memory between runs.
- If a download fails, Dibs stays quiet and tries again next run. There's no
failure email.
- If nothing matches for about 60 days, GitHub pauses the schedule on quiet
repos. It emails you first, and one click re-enables it.