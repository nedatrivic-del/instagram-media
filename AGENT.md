# Marketing-Agent · Zahnärztin Altstadt

Instructions for the ONE scheduled Claude task ("Marketing-Agent Zahnärztin Altstadt") that runs Dr. Neda Trivić's practice marketing: Instagram @dentistry.oldtown and the Google Business Profile. It follows the marketing strategy (Claude doc "Marketingstrategie Zahnärztin Altstadt": https://claude.ai/code/artifact/00c99ad4-cadb-499a-ab94-f536f3116c0c) and `plan/redaktionsplan.md`.
Nothing is ever published without Neda's explicit OK.

## Fixed facts
- Practice: Zahnärztin Altstadt · Dr. med. dent. Neda Trivić · Kapitelgasse 9, 5020 Salzburg · Alle Kassen & Privat · Tel. 0662 843 106
- Online booking: https://termine.softdent.at/zahnaerztin-altstadt (in the Instagram bio; captions say "Link in der Bio")
- Metricool brand (blogId): **7264951**, timezone Europe/Vienna. Instagram and Google Business Profile (gmb) are connected. LinkedIn (needs a paid Metricool upgrade) and Facebook (page not connectable yet) are paused – do not post there.
- Neda's email (approval channel): **nedatrivic@gmail.com**
- Preview page (optional to update): https://claude.ai/artifact/SYowyke9zyuT7WzJZrRnYg
- This repo is public. Media is served to Metricool from
  `https://raw.githubusercontent.com/nedatrivic-del/instagram-media/main/<path>`

## Posting rhythm (from the strategy)
| Slot | Time | Format | Prepared in run |
|---|---|---|---|
| Instagram Monday "Wissen" | Mon 10:00 | Reel 12–17 s (text on screen, Neda's photo, hook in first frame) | Tuesday 19:07 (for the NEXT Monday) |
| Instagram Wednesday "Wussten Sie schon?" | Wed 10:00 | Alternating reel / carousel (see plan) | Sunday 19:07 (for the coming Wednesday) |
| Google Business Profile (**PAUSED** – see below) | Thu 10:00 | Text post (publication) with ONE image, German only | Sunday 19:07, together with the Wednesday post |
| Google reviews | – | Reply suggestions by email, never posted by the agent | Monday 9:07 |
| Monthly report | – | Instagram + Google figures, one recommendation | First Sunday of the month, 19:07 |

Neda approves on Monday and Wednesday mornings by replying OK to the approval email. One OK in a thread approves everything in that email.

## Google posting PAUSED (since 20.10.2026)
Google removed the post "Prophylaxe – warum sie sich lohnt" (20.10.2026) and turned off posting for the Business Profile. Until Neda writes that posting works again: do NOT prepare new Google posts, do NOT include Google drafts in approval emails, and do NOT switch any gmb draft to draft:false. Existing gmb drafts stay drafts. Instagram continues normally.

## Run schedule – what to do in each run (task fires daily 9:07, 13:07, 19:07 Europe/Vienna)
Determine the current local date/time in Europe/Vienna first.
1. **Every run:** approval check (section "Approval check"). If nothing is pending, this step is a no-op.
2. **Sunday 19:07 run:** prepare the coming Wednesday's Instagram post AND the coming Thursday's Google post; send ONE approval email for both. If it is the first Sunday of the month, also send the monthly report.
3. **Tuesday 19:07 run:** prepare next Monday's Instagram post; send the approval email.
4. **Monday 9:07 run:** Google reviews (section "Google reviews").
5. Any other run: only step 1. Do not send any email when there is nothing to report.
6. Idempotency: before preparing, check posts/*/status.json and Metricool (getScheduledPosts) – never create a second post for a slot that already has one.

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

## Attention rules (since 20.10.2026 – from Neda's reel insights: ~50 % of viewers left in the first second)
- **Reels: 12–17 seconds, max 4 scenes**: hook → 1 statement (or tips) → optional tips → close. One idea per reel. Never more than 4 scenes.
- **Scene timing (Neda-approved 20.10.2026):** set `"duration"` on every scene: hook 2.6 s, statement 4.2 s, tips 5.6 s, close 3.8 s (≈16 s total). Use `videoCoverMilliseconds: 1500` (the hook frame; 2500 falls into the crossfade).
- **The hook is the whole game.** It is visible in the very first frame (the template does this automatically). Max ~6 words, speaks to the viewer directly, as a question or surprising fact: "Blutet Ihr Zahnfleisch beim Putzen?", "Das wissen die wenigsten:", "3 Zeichen, dass …", "Stimmt das?". Never a generic title like "Zahnfleischbluten" or "Wussten Sie schon?" on its own – for "Wussten Sie schon?" put the surprising fact itself in the hook (e.g. "Zahnfleisch und Herz hängen zusammen?").
- Hook `sub` is optional and very short (max 5 words).
- Headlines max 3 lines, body max 2 short lines per scene – people read fast.
- Close: prefer a save/share line ("Speichern Sie sich diesen Tipp.", "Teilen Sie das mit jemandem, der es wissen sollte.") or a gentle "Es lohnt sich, …". Still no hard sell.
- Carousels: slide 1 = the same kind of hook (question/number), last slide = save line + practice card. 5–7 slides.
- Caption: the FIRST line repeats the hook (it is what people see under the reel), then the content. End the German part with one save/share line.
- Approval email: add one line reminding Neda she can add a trending sound in the Instagram app after publishing (Reel → ⋯ → Audio) – optional, ~30 seconds.

## Monthly series „Ziemlich sympathisch, wenn …“ (episode 1: Fri 30.10.2026; episode 2: Fri 27.11.2026 10:00 Advent edition; then first Wednesday of each month from January 2027)
Idea from Neda (inspired by an orthodontist's "kinda chic to …" carousel – adapt, never copy). Values, not teeth: time, listening, explaining, trust.
- Carousel, 5–6 slides. Every slide (Neda-approved look): the whole slide is an analog photo print – the practice photo full size with the text ON the photo ("Ziemlich sympathisch," Fira italic + the "wenn …" line in Oswald, cream, centred), framed by a cream paper border; "ZAHNÄRZTIN ALTSTADT" + handle on the bottom strip of the frame. Only brand fonts. Last slide: `close` with "So arbeiten wir in der Altstadt." + practice card.
- Lines are from the patient's perspective (never self-praise). Examples Neda liked: "wenn sich jemand Zeit nimmt für noch eine Frage." · "wenn erst erklärt und dann behandelt wird." · "wenn Angst ernst genommen wird." · "wenn man in drei Sprachen zuhört." · "wenn Zahnfleisch genauso wichtig ist wie Zähne." Write new lines each month; no promises.
- Photos: only Neda, team, hands, instruments, rooms, details. NEVER patients (WR-ÖZÄK). Never reuse the same photo two months in a row.
- Neda still has to take the photos. If `photos/praxis/` has fewer than 5 photos, do NOT build the series: use a normal „Wussten Sie schon?“ post and add one line to the approval email reminding her to send practice photos.
- Any carousel scene accepts `"frame": true` (same paper frame); in the series the closing `close` slide is always framed.
- Scene type `photo` exists: `{"type":"photo","photo":"photos/praxis/<file>.jpg","text":"wenn …","focus":[x,y],"shade":120}` (framed analog print, text on photo; "Ziemlich sympathisch," added automatically; optional "dy", "shade", "size"). Last slide: `close`. Neda's approved look: `drafts/_demo_sympathisch/` (5 photos + close).
- Episode 1 (Fri 30.10.2026, posts/2026-10-30_serie_ziemlich-sympathisch) is done and scheduled and used all five current photos (wartezimmer, globus, voegel, blumen_1, blumen_2). Episode 2 (Fri 27.11.2026 10:00) is an ADVENT edition: Neda puts 5 Advent photos from the practice into her Google Drive folder "Insta Praxisfotos" (search Drive by that folder title, download with download_file_content, store as photos/praxis/advent_*.jpg); write calm Advent-flavoured "wenn …" lines (no promotions, no gifts/vouchers).
  Neda-approved plan for episode 2: SAME framed analog look as episode 1 with `"frame_ink": "gold"` (gold brand text on the frame + gold "Ziemlich sympathisch," – Neda approved gold). Do NOT use the `polaroid` scene type for this series (Neda compared it and chose the framed look with text on the photo) – sample: `drafts/sympathisch_advent_probe/`. Photo ideas she got: fairy lights/Advent wreath at reception, fir sprig or star on the counter, a cup of tea in the waiting room, window with old-town view at dusk, candle/light bokeh. Line ideas (adapt to the actual photos): "wenn es in der Praxis schon nach Advent aussieht." · "wenn man in der hektischen Zeit kurz durchatmen darf." · "wenn jemand fragt: Und wie geht's Ihnen eigentlich?" · "wenn man auch im Dezember nicht hetzen muss." · "wenn sich ein Termin wie eine kleine Pause anfühlt." Neda already sent 3 Advent photos (photos/praxis/advent_kranz.jpg, advent_fenster.jpg, advent_kekse.jpg) – test carousel she saw: drafts/sympathisch_advent_probe/ (lines Neda saw: wreath "wenn die Vorfreude mit jeder Kerze wächst." · window "wenn draußen die Altstadt leuchtet und drinnen jemand Zeit für Sie hat." · cookies "wenn auch die Zahnärztin Kekse bäckt." – lines must match what the photo shows and make sense on their own). Use these plus any new ones from Drive; 3 photos are enough if no more arrive. Closing slide (framed): "Eine ruhige Adventszeit!" + "Ihr Team der Zahnärztin Altstadt." + practice card. From then on ask Neda (in the approval email) for new photos so the series does not look repetitive.

## Adventskalender 2026 (Neda-approved 20.10.2026) – 24 Türchen, 1.–24.12., daily 18:00
- Spec: `"theme": "advent"` and `"door": <n>` (dark green Advent look, gold door badge). Approved sample: `drafts/advent_muster/` (Türchen 1). Alternate formats: odd doors = REEL (12–17 s, attention rules apply), even doors = carousel (5–6 slides). Close slide body: "Morgen öffnen wir Türchen Nummer <n+1>." (door 24 different, see below).
- **Always positive (Neda: "keine Adventspielverderber")**: never forbid or scold. Every door says what people CAN do and ends on a light, warm note ("Genießen Sie …, mit diesem kleinen Trick bleibt es zahnfreundlich."). No "verzichten Sie", no warnings as headline; the hook may be curious, never alarming.
- Same content rules as always (Sie, calm, no promises, WR-ÖZÄK, only services offered, no nutrition counselling, no bleaching promo). Every fact must be checked against a reputable source (open the page); drop or replace a door if a fact cannot be verified. Caption DE → EN → BKS + end block; first line = hook; hashtag #adventskalender + #zahnärztinaltstadt.
- Doors (mix approved by Neda – food/drink only in a few, keep the mix):
  1 Glühwein: Zucker, Säure & Wärme · 2 Kurios: Zahnschmelz härtestes Material, trotzdem verletzlich · 3 Quiz: Wie lange putzen Sie wirklich? · 4 Feiertagsstress & Zähneknirschen – Anzeichen · 5 Nüsse mit den Zähnen knacken? Lieber nicht · 6 Nikolaus-Special: Woher kommt die Zahnbürste? · 7 Mythos oder Wahrheit: Harte Zahnbürsten putzen besser? · 8 Zahnfleisch & Herz – was Studien zeigen · 9 Alkohol & trockener Mund – Wasser zwischendurch · 10 Hinter den Kulissen: So läuft eine Prophylaxe bei uns · 11 Kälte & empfindliche Zähne · 12 Zahnersatz in der Festzeit pflegen · 13 Kurios: 700+ Bakterienarten im Mund, die meisten Freunde · 14 Mythos: Zimt & Nelken gut für Zähne? · 15 Frauen 40+: warum sich das Zahnfleisch verändert · 16 Rauchen + Alkohol: doppelte Belastung fürs Zahnfleisch · 17 Quiz: Zahnseide oder Bürstchen? · 18 Füllung/Krone abgebrochen – was tun? · 19 Stress, Schlaf & Zahnfleisch · 20 Lebkuchen & Zuckerstangen: Kleben & Lutschen · 21 Zeitreise: Zahnpflege vor 200 Jahren · 22 Zahnpflege im Reisegepäck – Checkliste · 23 Nach dem Festessen: 3 Schritte · 24 (carousel, sample drafts/advent_24_muster/ – 5 slides: Frohe Weihnachten · Danke für Ihr Vertrauen 2026 · Pause 24.12.–10.01., ab Mo 11. Jänner wieder da (Neda confirmed: online booking via softdent stays open during the holiday) · Notdienst · Bis bald im neuen Jahr) Frohe Weihnachten & gutes neues Jahr + Praxisurlaub 24.12.2026–10.01.2027 (wieder da ab Mo 11.01.2027) + Notdienst: Neda's source is the Notdienstzentrum Salzburg, https://www.ndz.at (weekends/holidays; in Oct 2026 the site said 14:00–17:00, register in person, no phone booking, info line +43 662 870022). Re-open ndz.at when building and use the current hours; on the slide say "Notdienstzentrum Salzburg … ndz.at". Same for door 18.
- Neda's photo (template/neda.jpg) may appear in hooks; no patients.
- Timeline: Sun 15.11.2026 19:07 run – email Neda (BKS, short): reminder to put 5 Advent photos into the Drive folder "Insta Praxisfotos" by Sat 21.11. Mon 16.11.–Fri 20.11. 19:07 runs – build 5–6 doors per run (render, check stills, push), plus the New Year post (01.01.2027 11:00, short greeting, back on 11.01.). Sat 21.11. 19:07 – build „Ziemlich sympathisch“ Advent (if photos are there; otherwise tell Neda in the email). Sun 22.11.2026 19:07 – create ALL as Metricool DRAFTS (Türchen at 18:00 on 1.–24.12., Neujahr 01.01. 11:00, Sympathisch 27.11. 10:00) and send ONE approval email: subject "[Insta-Freigabe] Adventskalender 1–24 + Sympathisch 27.11. + Neujahr", list every door (date, format, title, media link, first caption line), plus a link to a contact-sheet image of all doors (render one overview JPG into drafts/advent_2026/ and push). One OK approves all of them (draft:false for every post in that email). Changes → fix only the doors mentioned, re-send.
- Store each door in `posts/2026-12-<DD>_advent_<n>_<slug>/` with status.json like every post (email_thread_id = the one approval email).
- During the Advent calendar and the practice holiday (1.12.2026–10.01.2027) do NOT prepare normal Mo/Mi or Google posts. Normal preparation resumes with the Tuesday 05.01.2027 19:07 run (prepares Mo 11.01.2027); then the usual rhythm. Doors 8 and 15 overlap with November topics – Neda approved that; write them as short new angles, not repeats.

## How to build a post
1. Pick the topic from `plan/redaktionsplan.md` (Wednesday: research a fresh study first; you may replace the planned topic if you find a better, recent, Austria-appropriate one).
2. Create `posts/<YYYY-MM-DD>_<slot>_<slug>/spec.json` – copy the structure of `posts/2026-10-21_wussten-sie_naschen/spec.json`. Scene types: `hook` (Neda's photo + headline + sub), `statement` (optional kicker, headline lines, body), `tips` (headline + exactly 3 items), `close` (headline + body + practice card). Keep every headline line short enough to fit (Oswald, ~900 px width; use smaller `size` or `maxw` to force clean breaks).
3. Render (from `template/`):
   - Reel: `python3 make_media.py ../posts/<folder>/spec.json reel ../posts/<folder>/reel.mp4` (~2 min)
   - Carousel: `python3 make_media.py ../posts/<folder>/spec.json carousel ../posts/<folder>/` → `slide_1.jpg … slide_5.jpg`
   - Look at the stills (`preview` mode or the slides) with the Read tool before publishing anything: no overlapping text, no orphan words, nothing cut off. Fix the spec and re-render if needed.
4. Write `caption.txt` in the folder (rules above).
5. `git add`, commit (end message with the attribution lines your session gives you), `git push`. Verify the raw URL returns HTTP 200 (`curl -sI`).
6. Create the Metricool post as a **draft** (`draft: true`, `autoPublish: true`) at the target date 10:00 Europe/Vienna, provider instagram, `instagramData.type` = `REEL` (video) or `POST` (carousel: list all slide URLs in `media`), `isAiGenerated: false` (true only if an AI image of Neda is used). For reels set `videoCoverMilliseconds: 1500`.
6b. **Google post (Sunday run only, for Thursday 10:00):** topic from the plan's Google column (practice-oriented: prophylaxis, periodontology, crowns/bridges/dentures, online booking, team). Create a Metricool DRAFT: providers `[{"network":"gmb"}]`, `gmbData: {"type":"publication"}`, German only, 600–1200 characters, no hashtags, no emojis, factual (same advertising rules), ending with "Termin online: termine.softdent.at/zahnaerztin-altstadt". **Never put a phone number in Google post text** (Google removed the 20.10.2026 post and turned off posting for the profile; phone numbers in the post body are a known rejection reason – the profile already has a call button). Attach one image: build a small 2–3-scene spec (hook + statement or close) and render `carousel` mode, use `slide_1.jpg` (push it first). Folder `posts/<date>_google_<slug>/` with its own status.json. Include it in the same approval email as the Wednesday post.
7. Write `status.json` in the folder: `{"date": ..., "slot": ..., "title": ..., "format": ..., "status": "awaiting_approval", "metricool_id": ..., "metricool_uuid": ..., "email_thread_id": ..., "media": [...]}`.
8. Email Neda (Gmail send_message to nedatrivic@gmail.com), subject: `[Insta-Freigabe] <Wochentag DD.MM.> – <Titel>`. Body in BKS, short: what, when, why this topic (1–2 lines, with study source), the media link(s) (raw GitHub URLs – they open in the browser), the full caption, and: "Odgovori sa **OK** i post ide u <dan> u 10:00. Ako želiš promjenu, samo napiši šta." Start the body with the marker line `[Insta-Agent]`.
9. Optionally update the preview page (Artifact tool, `url` above): read it first, add the post (upload media as asset), mark it "wait".

## Approval check (runs 3×/day)
For every `posts/*/status.json` with `status: "awaiting_approval"` or `"changes_requested"`:
1. Read the Gmail thread (`email_thread_id`). Neda's replies are messages that do NOT start with `[Insta-Agent]`.
2. Reply contains OK / ok / Okay / passt / ja / da / može / super (approval, no change request) → update every Metricool post in that email (Instagram and/or Google) with `draft: false` (keep everything else) via updateScheduledPost; set `status: "scheduled"`; reply in the thread "[Insta-Agent] Zakazano za <dan> u 10:00 ✅".
3. Reply asks for changes → apply them (spec/caption), re-render, push, update the Metricool draft media/text, reply in the thread with the new links and ask for OK again; `status: "awaiting_approval"`.
4. No reply and the post is less than 20 hours away → send one short reminder in the thread (only once: set `"reminded": true`). If still no OK at publish time, it stays a draft and is NOT published. Never publish without OK.
5. Commit and push the status changes.

## Monthly report (first Sunday run of each month)
Use Metricool analytics for the previous month: Instagram (reach, views, saves, shares, follower change, best post, link clicks if available, best posting times) and Google Business Profile (getAnalyticsDataByMetrics: GMEV18 search views, GMEV19 maps views, GMEV21 website clicks, GMEV22 calls, GMEV23 directions, GMEV12 rating; keywords GMKW01/GMKW02 – top 5), each compared with the month before in %. Email Neda a short BKS summary (5–8 lines + one concrete recommendation). After 3 months, check whether Mon/Wed 10:00 is still best and suggest changes.

## If something fails
Tell Neda by email (subject starting "[Insta-Agent]") in one or two plain BKS sentences what failed and what she needs to do (e.g. reconnect Instagram in Metricool). Never retry endlessly; never publish without OK.

## Google reviews (Monday 9:07 run)
1. getAnalyticsDataByMetrics(brandId 7264951, last 8 days) with GMRE02 (date), GMRE06 (name), GMRE09 (stars), GMRE04 (replied), GMRE08 (text).
2. For every review with replied = false write a reply suggestion in the review's language (no text → German): 2–3 sentences, warm, signed "Dr. Neda Trivić & Team". NEVER confirm the person is a patient, never mention treatment, diagnosis, appointment or details (zahnärztliche Schweigepflicht); no superlatives. Negative (1–3 stars): neutral, no argument, offer a conversation in the practice/by phone, and put a warning at the top of the email. Reviews from accounts linked to Neda (e.g. "Zubo Team", "Nada Trivic", "Marica Kicusic"): list only, no suggestion.
3. Email Neda (subject "Google profil – recenzije (D. M.)", BKS, ti-forma, plain text): name, stars, short quote, then "Prijedlog odgovora:" with copy-paste text; at the end: replies are published in Metricool → Inbox → Google Business Profile or directly on Google. No new reviews → no email.
4. Never reply to reviews yourself, never change the profile, never delete posts.
