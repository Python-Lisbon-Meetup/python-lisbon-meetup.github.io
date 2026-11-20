---
name: python-lisbon-announcements
description: Write all the announcement copy and event images for a Python Lisbon Meetup (PyLM) event — the bilingual Meetup.com "Details" text, the LinkedIn version with Unicode bold, a LinkedIn post, X/Twitter and Mastodon posts, a Discord announcement, the square and 16:9 event images from the group's own image builder, and the new event card on the group's website (python-lisbon-meetup.github.io). Use this whenever the user is organizing, announcing or promoting a Python Lisbon meetup, mentions a new PyLM event, a talk or speaker for the next meetup, a venue like Gapstars, or asks for any one of these posts, the event image or the website's meetup history, even if they only ask for one channel.
---

# Python Lisbon Meetup announcements

Every Python Lisbon Meetup needs the same set of announcements in about six formats, plus a card on the group's website. The facts are the same everywhere; what changes is each platform's formatting rules and length limits. This skill keeps the house style and the lessons from earlier events, so the organizer only has to supply the event facts.

## 1. Collect the event facts

Get these from the user's message or earlier in the conversation. Ask only for what's missing and actually matters, in one short question:

- **Event number** (e.g. #15). If unknown, check the group's past events at https://www.meetup.com/python-lisbon-meetup/events/ or ask.
- **Date and start time.** The group meets on the first non-holiday Thursday of the month. Portugal has public holidays on 1 and 8 December, among others, so check the date. Default start time: 18:30.
- **Venue.** See `references/venues.md` for known venues and their exact wording. For a new venue, ask for the name, building and floor.
- **Talks:** title and speaker for each. Add a link on a speaker's name only if the user gives you the URL. Don't search for profiles and don't leave placeholders, because a wrong or empty link is worse than none.
- **Extras:** food or drinks from the host, a joint event with another group (like PyData Lisbon), filming or photography, a hard end time.
- **Meetup event URL**, for the social posts. Remove tracking parameters like `?isFirstPublish=true` or `?eventOrigin=...`.

If the user points to an earlier event page as a model, fetch it and follow its structure.

## 2. Write the copy

Templates for every format, with a complete worked example, are in `references/templates.md`. Read it before writing. These are the house rules, and why:

- **Meetup details are bilingual**: English first, then 🇵🇹 and a European Portuguese version (not Brazilian Portuguese: "convívio", "palestra", "petiscos", "11º andar"). Talk titles stay in English in both versions.
- **Only promise what's confirmed.** Write "One or more lightning talks ⚡" without "if time allows". Leave out the end time unless the user gives one. Mention food or drinks only if the host has confirmed them, and add 🍻 or 🍕 to the opening line when they have. Include the image-consent paragraph only if the event will be filmed or photographed.
- **LinkedIn has no Markdown.** For LinkedIn, convert bold to Unicode sans-serif bold with `scripts/unicode_bold.py`, and use "•" for bullets. Bold only the venue, times and speaker names. Screen readers and LinkedIn search handle Unicode bold badly, so keep talk titles plain. Accented letters like í and º have no bold version and stay regular weight. That's expected.
- **The LinkedIn post puts the link in the first comment.** LinkedIn shows posts with outside links to fewer people. End the post with "RSVP link in the comments 👇" and give the comment text separately. Suggest @-tagging the speaker and the host.
- **X and Mastodon get the link in the post itself**, with no Unicode bold. Check lengths with `scripts/check_lengths.py`: X allows 280, and URLs count as 23 and emoji as 2. Mastodon allows 500, and URLs count as 23. On X, the full talk title usually doesn't fit, so use a hook question and the speaker's name. Suggest alt text for the image on Mastodon.
- **Discord uses real Markdown**: an `##` header, **bold**, and a masked link `[RSVP on Meetup](url)`. Mention that they can add `@everyone` or a role ping, and that wrapping the URL in `<...>` hides the preview card.

Put each piece of copy in its own code block so it's easy to copy without the chat's formatting getting in the way. Give a short note after each one only for things the organizer has to act on.

When the user asks for one change later, such as removing a line, give just the changed lines. When several changes have piled up, or they're about to paste the whole thing, give the full updated text.

## 3. Make the event images

Run `scripts/render_images.py`. It clones the group's site repo (github.com/python-lisbon-meetup/python-lisbon-meetup.github.io), serves the image builder from `/sharing/` locally, fills in the form with Playwright, and saves the canvas as PNG files. This gives exactly the same look as the public builder at https://python-lisbon-meetup.github.io/sharing/.

```bash
python3 scripts/render_images.py event.json /mnt/user-data/outputs
```

`event.json` holds `title`, `date` (YYYY-MM-DD), `time`, `location`, `description`, and optional per-format overrides. The script's docstring describes them. By default it makes the 16:9 widescreen image (1920×1080, for the Meetup banner) and the square one (1080×1080, for LinkedIn, Mastodon and Discord).

**Always look at every image afterwards** with the view tool. The builder wraps text automatically and often leaves one word alone on the last line. Fix this with manual `\n` breaks in the description, which the builder keeps. The location is a single-line field that drops `\n`, so for the square image use a shorter location string instead, e.g. "Gapstars, Atrium Saldanha, 11th floor". Re-render until no line ends with a single orphaned word, then share the files.

Default image text: title "#N Python Lisbon Meetup at <Venue>". Description: talk title, then "by <Speaker>", a blank line, and "Plus lightning talks, networking and socializing!". Leave out emoji, because the headless browser may not have an emoji font.

## 4. Update the website

The group's site (https://python-lisbon-meetup.github.io, repo github.com/python-lisbon-meetup/python-lisbon-meetup.github.io) has a "Meetup History" grid in `index.html`. Every event gets a card there as soon as the Meetup page is published, so do this step every time, even when the user only asked for the posts. If you're not working in a checkout of the repo, clone it. Then:

1. **Add the new card first in `<div class="event-grid">`.** Copy the existing card markup exactly. Use the snippet in `references/website.md`.
2. **Mark it upcoming:** add `event-card--upcoming` to the `<article>` and the badge `<p class="event-badge event-badge--upcoming">Upcoming · RSVP</p>`. Then remove both from the previous event's card, because only one card should say "Upcoming".
3. **Link the title to the Meetup event page.** Use the URL without tracking parameters and with a trailing slash. The `event-link` class makes the whole card clickable. Every card that has a Meetup page should be linked. #00–#03 and #12 have no Meetup page, so they stay unlinked.
4. **Pick the tile** from `references/venues.md`. Each venue has its own medallion in `assets/tiles/`. A new venue needs a new tile: ask the user what it should show. Until one exists, use `snakes-medallion.webp` as a placeholder and say so.
5. **Fill in the details** with the same facts as the announcements: date (e.g. "December 3, 2026"), main talk and speaker (or "Talks" and "Speakers" for several), host and location. A joint event (e.g. with PyData Lisbon) or a special event uses `event-card--special` with a yellow badge instead of the upcoming one once it's over.
6. **Check the date against the Meetup page.** If a holiday moves the meetup to the second Thursday, the card must show the real date.

Preview the page locally (`python3 -m http.server` in the repo) and check the new card in light and dark mode. Then commit on a branch and open a PR, if the user wants that. Don't push to `main` directly.

This skill lives in the same repo, in `.claude/skills/python-lisbon-announcements/`. When you learn a new lesson (a new venue, tile or house rule), update it there in the same PR.
