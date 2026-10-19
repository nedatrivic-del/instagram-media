# Instagram-Agent · Zahnärztin Altstadt (@dentistry.oldtown)

Instructions for the scheduled Claude sessions that run Dr. Neda Trivić's practice Instagram.
Nothing is ever published without Neda's explicit OK.

## Fixed facts
- Practice: Zahnärztin Altstadt · Dr. med. dent. Neda Trivić · Kapitelgasse 9, 5020 Salzburg · Alle Kassen & Privat · Tel. 0662 843 106
- Online booking: https://termine.softdent.at/zahnaerztin-altstadt (in the Instagram bio; captions say "Link in der Bio")
- Metricool brand (blogId): **7264951**, timezone Europe/Vienna. Instagram is connected. LinkedIn and Facebook are NOT connected – post Instagram only.
- Neda's email (approval channel): **nedatrivic@gmail.com**
- Preview page (optional to update): https://claude.ai/artifact/SYowyke9zyuT7WzJZrRnYg
- This repo is public. Media is served to Metricool from
  `https://raw.githubusercontent.com/nedatrivic-del/instagram-media/main/<path>`

## Posting rhythm
| Slot | Time | Format | Prepared by |
|---|---|---|---|
| Monday "Wissen" | Mon 10:00 | Reel (text on screen, Neda's photo) | Tuesday-evening run (for the NEXT Monday) |
| Wednesday "Wussten Sie schon?" | Wed 10:00 | Alternating: reel one week, carousel the next (see `plan/redaktionsplan.md`) | Sunday-evening run (for the coming Wednesday) |

Neda approves on Monday and Wednesday mornings. The approval-check run (3×/day) schedules approved posts.

## Content rules (from Neda – non-negotiable)
- On-screen text German, formal "Sie". Tone: calm, warm, professional, informative. No promises, no "we solve everything", no magic wand.
- Captions: German first, then English, then BKS (Bosnian/Croatian/Serbian), separated by a line with "—". **No flag emojis.** End block:
  ```
  📍 Zahnärztin Altstadt · Kapitelgasse 9, Salzburg
  🗓️ Terminvereinbarung online – Link in der Bio
  ☎️ 0662 843 106
  Alle Kassen & Privat
  ```
  then 10–15 relevant hashtags (German + Salzburg local tags).
- Only methods recognised in Austria (silver diamine fluoride/SDF was rejected for this reason). Check before proposing.
- Only services the practice actually offers. The practice does NOT offer nutrition counselling (Ernährungsberatung) – never offer advice/consultation on nutrition. No bleaching promotion. No children "play/acclimatisation" appointments.
- The practice has too many child patients: children's topics at most ~1 in 8 posts, purely preventive, never a call to book children.
- Highlight: periodontology/gum health, fixed and removable prosthetics (crowns, bridges, dentures, implant prosthetics), prophylaxis. Target groups: women 40+, adults 50+ with prosthetic needs, periodontitis risk.
- Studies: state associations honestly ("Studien zeigen einen Zusammenhang", never "verursacht"). Cite the source (authors, journal, year) in the caption. Open the source page; never rely on a snippet. Prefer studies from the last ~12 months for "Wussten Sie schon?".
- Austrian dental advertising rules (WR-ÖZÄK): factual and informative, no prices, no vouchers/promotions, no comparisons with other practices, no before/after images, no patient images.
- Closing slide: a gentle line, never a hard sell. Good: "Es lohnt sich, …", "Fragen Sie uns." only if the practice really does it.
- Do not repeat a topic within 4 weeks. Reserved for December: "Mythos oder Wahrheit? Bei Zahnfleischbluten lieber nicht putzen?" (reel already rendered in Neda's chat; re-render from a spec if needed).

## How to build a post
1. Pick the topic from `plan/redaktionsplan.md` (Wednesday: research a fresh study first; you may replace the planned topic if you find a better, recent, Austria-appropriate one).
2. Create `posts/<YYYY-MM-DD>_<slot>_<slug>/spec.json` – copy the structure of `posts/2026-10-21_wussten-sie_naschen/spec.json`. Scene types: `hook` (Neda's photo + headline + sub), `statement` (optional kicker, headline lines, body), `tips` (headline + exactly 3 items), `close` (headline + body + practice card). Keep every headline line short enough to fit (Oswald, ~900 px width; use smaller `size` or `maxw` to force clean breaks).
3. Render (from `template/`):
   - Reel: `python3 make_media.py ../posts/<folder>/spec.json reel ../posts/<folder>/reel.mp4` (~2 min)
   - Carousel: `python3 make_media.py ../posts/<folder>/spec.json carousel ../posts/<folder>/` → `slide_1.jpg … slide_5.jpg`
   - Look at the stills (`preview` mode or the slides) with the Read tool before publishing anything: no overlapping text, no orphan words, nothing cut off. Fix the spec and re-render if needed.
4. Write `caption.txt` in the folder (rules above).
5. `git add`, commit (end message with the attribution lines your session gives you), `git push`. Verify the raw URL returns HTTP 200 (`curl -sI`).
6. Create the Metricool post as a **draft** (`draft: true`, `autoPublish: true`) at the target date 10:00 Europe/Vienna, provider instagram, `instagramData.type` = `REEL` (video) or `POST` (carousel: list all slide URLs in `media`), `isAiGenerated: false` (true only if an AI image of Neda is used). For reels set `videoCoverMilliseconds: 2500`.
7. Write `status.json` in the folder: `{"date": ..., "slot": ..., "title": ..., "format": ..., "status": "awaiting_approval", "metricool_id": ..., "metricool_uuid": ..., "email_thread_id": ..., "media": [...]}`.
8. Email Neda (Gmail send_message to nedatrivic@gmail.com), subject: `[Insta-Freigabe] <Wochentag DD.MM.> – <Titel>`. Body in BKS, short: what, when, why this topic (1–2 lines, with study source), the media link(s) (raw GitHub URLs – they open in the browser), the full caption, and: "Odgovori sa **OK** i post ide u <dan> u 10:00. Ako želiš promjenu, samo napiši šta." Start the body with the marker line `[Insta-Agent]`.
9. Optionally update the preview page (Artifact tool, `url` above): read it first, add the post (upload media as asset), mark it "wait".

## Approval check (runs 3×/day)
For every `posts/*/status.json` with `status: "awaiting_approval"` or `"changes_requested"`:
1. Read the Gmail thread (`email_thread_id`). Neda's replies are messages that do NOT start with `[Insta-Agent]`.
2. Reply contains OK / ok / Okay / passt / ja / da / može / super (approval, no change request) → update the Metricool post with `draft: false` (keep everything else) via updateScheduledPost; set `status: "scheduled"`; reply in the thread "[Insta-Agent] Zakazano za <dan> u 10:00 ✅".
3. Reply asks for changes → apply them (spec/caption), re-render, push, update the Metricool draft media/text, reply in the thread with the new links and ask for OK again; `status: "awaiting_approval"`.
4. No reply and the post is less than 20 hours away → send one short reminder in the thread (only once: set `"reminded": true`). If still no OK at publish time, it stays a draft and is NOT published. Never publish without OK.
5. Commit and push the status changes.

## Monthly report (first Sunday run of each month)
Use Metricool analytics for the previous month (reach, views, saves, shares, follower change, best post, link clicks if available, best posting times). Email Neda a short BKS summary (5–8 lines + one concrete recommendation). After 3 months, check whether Mon/Wed 10:00 is still best and suggest changes.

## If something fails
Tell Neda by email in one or two plain BKS sentences what failed and what she needs to do (e.g. reconnect Instagram in Metricool). Never retry endlessly; never publish without OK.
