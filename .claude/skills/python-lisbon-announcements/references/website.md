# Website card snippet

Paste this first in `<div class="event-grid">` in `index.html`. Escape `&` as `&amp;` in the text.

```html
                <article class="event-card event-card--upcoming">
                    <div class="event-head">
                        <img class="event-tile" src="assets/tiles/saldanha-medallion.webp" alt="" width="56" height="56" loading="lazy" />
                        <span class="event-number" aria-hidden="true">#15</span>
                    </div>
                    <p class="event-badge event-badge--upcoming">Upcoming · RSVP</p>
                    <h3><a class="event-link" href="https://www.meetup.com/python-lisbon-meetup/events/317505097/"><span class="visually-hidden">#15 - </span>Python Lisbon Meetup at Gapstars ✨</a></h3>
                    <dl class="event-details">
                        <div><dt>Date</dt><dd>December 3, 2026</dd></div>
                        <div><dt>Main talk</dt><dd>How I Learned to Stop Worrying and Love the Robot: How to tell if your AI builds slop without reading every line</dd></div>
                        <div><dt>Speaker</dt><dd>Ilya Dorman</dd></div>
                        <div><dt>Host</dt><dd>Gapstars</dd></div>
                        <div><dt>Location</dt><dd>Gapstars, Edifício Atrium Saldanha (11th floor)</dd></div>
                    </dl>
                </article>
```

The `<h3>` title is the Meetup event title. The visually hidden "#15 - " prefix is for screen readers, because the big number is `aria-hidden`.

For several talks, put each title in its own `<dd>`:

```html
                        <div><dt>Talks</dt><dd>First talk title</dd><dd>Second talk title</dd></div>
                        <div><dt>Speakers</dt><dd>First Speaker, Second Speaker</dd></div>
```

For a joint or special event, use `event-card--special` and a plain yellow badge such as `<p class="event-badge">Joint with PyData Lisbon</p>`.

When the next event is added, remove `event-card--upcoming` and the upcoming badge from this card. If it was a joint event, swap in the special class and badge.

The "Upcoming events" button in the hero and the Meetup.com link under "Get Involved" point to `https://www.meetup.com/python-lisbon-meetup/events/`. Never point them at a single event, because it goes stale.
