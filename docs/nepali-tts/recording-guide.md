# Nepali TTS — Recording Guide for Voice Contributors

Oct 12, 2026 · Markdown snapshot of the [live doc](https://claude.ai/code/artifact/3b0e7c20-5952-43ca-95d2-cfce2432352e); if they differ, the live doc wins.

## Why we're recording

We are teaching a speech model (Qwen3-TTS) to speak Nepali in the voice of a call-center agent. Public Nepali data gives us at most about 17 minutes from any one speaker, and almost no male speech, so we need our own recordings.

Your recordings are used in two ways:

- **To teach pronunciation.** Every clip helps the model learn how written Nepali sounds, especially numbers, dates, amounts and the English words we use on calls.
- **To build a voice.** If you are a voice talent (next section), the model will learn to sound like you. Callers will hear a synthetic voice based on yours, so we ask for written consent before you start (see "What to send us").

The model copies everything it hears: background hum, echo, mouth clicks, a rushed tone. Clean, consistent audio matters more than the number of hours.

## Two roles: voice talent or contributor

We need **one female and one male voice talent**, plus as many contributors as are willing. A voice must come from one person: ten people recording 20 minutes each gives ten weak voices, not one strong one.

|  | Voice talent | Contributor |
| --- | --- | --- |
| How many people | 1 female, 1 male | 5–15, mixed gender and region |
| Target audio | 2–4 hours of finished clips (minimum 1 hour) | 20–60 minutes |
| Prompts | \~1,500–2,500 | \~250–700 |
| Time needed | 8–15 sessions of about 1.5 hours | 1–3 sessions |
| Equipment | USB or XLR microphone, quiet treated room | Microphone preferred; a phone is acceptable |
| Consistency | Same mic, room, position and style every session | Consistent within your own sessions |
| What it trains | The voice callers will hear | Nepali pronunciation and call-center vocabulary |

Voice talent profile: clear standard Nepali (Kathmandu-style or widely understood), a warm and steady speaking voice, no strong regional accent, and the time to finish all sessions within about 2–3 weeks. Call-center experience helps.

Rough timing: one finished hour of clips takes about 3–4 hours in the room, including retakes and breaks.

## What you will read, and how

You read from a prompt list we give you. Each prompt has an ID (for example `cc_0123`) and one sentence in Devanagari. **The prompt text is the transcript**, so you do not write anything down. You only need to say exactly what is on the screen.

The list mixes four kinds of prompt:

- **Call-center phrases**: greetings, verification, balances, payments, complaints, holds, transfers, closings.
- **Numbers and dates spelled out in words**: amounts, phone and account numbers, dates and times.
- **English words as said on calls**, written in Devanagari (ओटीपी, ब्यालेन्स, केवाईसी).
- **General sentences** chosen so every Nepali sound and letter combination appears several times.

### Accuracy rules

1. Read every word as written. Do not add हजुर, अँ, ल, or anything else that is not on the screen.
2. If you stumble, pause, then re-read the **whole** sentence. Never patch the middle of a sentence.
3. If a prompt looks wrong, or you would never say it that way, **skip it and note the ID**. Do not quietly change the words; we fix the text and re-issue it.
4. Numbers are spelled out on purpose. Read एक लाख पच्चीस हजार as words, the way you would say them to a customer.

### Speaking style

- Speak like a calm, friendly agent on a good day: warm, clear, never rushed.
- Keep a moderate pace. Numbers and account details should be slightly slower and very clear.
- Questions should rise like real questions. Apologies should sound sincere, not dramatic.
- Keep the same energy and distance from the mic in the last prompt of the day as in the first. If you notice yourself drifting, take a break.
- Use your natural voice. Do not put on a "radio" voice that you cannot keep up for hours.

## Equipment and room

A quiet, dead-sounding room matters more than an expensive microphone. A small bedroom with a bed, curtains and a wardrobe beats a large empty office.

### Microphone

| Option | Examples | Use for |
| --- | --- | --- |
| USB dynamic or condenser mic (preferred) | Shure MV7, Rode NT-USB, Audio-Technica AT2020USB, Samson Q2U | Voice talents and contributors |
| XLR mic + audio interface | Any studio mic into a Focusrite or similar interface | Voice talents, if available |
| Smartphone (fallback) | Recent iPhone or Android, held on a stand | Contributors only |
| **Do not use** | Laptop built-in mic, Bluetooth headsets or earbuds, conference speakerphones | — |

Bluetooth audio is compressed before it reaches the computer, so it is never acceptable.

### Placement

- Mouth 15–20 cm (a hand-span) from the mic, slightly off to one side so breaths do not hit it directly.
- Use a pop filter or foam windscreen. A thin sock over the mic works in a pinch.
- Mark your chair and mic positions with tape so every session matches.
- Sit upright. Do not hold the mic or the phone in your hand.

### Room

- Turn off fans, air conditioning, fridges nearby and anything that hums. Close windows.
- Avoid echo: soft furnishings, curtains drawn, a blanket behind the mic if the wall is bare. Clap once; you should hear no ringing tail.
- Silence your phone and notifications. No one else talking nearby.
- Record at the same time of day if you can. Voices sound different in the morning.

### Software

- **Turn off all audio processing**: noise suppression, echo cancellation, automatic gain control, "voice isolation", Krisp, and Windows or macOS sound enhancements.
- We will share a simple prompt-by-prompt recorder. Until then, Audacity works (record each prompt as a separate take and export it with its ID as the filename).
- Phone fallback: use a recorder app that saves **WAV**, not the default voice memo app, which saves compressed audio.

## Recording settings and file format

Record one WAV file per prompt at 48 kHz, mono, 24-bit, with the prompt ID as the filename.

| Setting | Value | Why |
| --- | --- | --- |
| File format | WAV (uncompressed PCM) | MP3, M4A, AAC and OGG throw away detail the model would copy |
| Sample rate | 48,000 Hz (44,100 Hz acceptable) | We downsample to 24 kHz ourselves |
| Bit depth | 24-bit (16-bit acceptable) | More headroom for quiet speech |
| Channels | Mono | A stereo file from a single mic is fine; we take one channel |
| Level | Peaks between −12 and −6 dBFS | Loud enough to be clean, never clipping |
| Clipping | Never touch 0 dBFS | A clipped clip is unusable and must be re-recorded |
| Background noise | Below −60 dBFS in silence | Check by recording 5 seconds of room tone |
| Silence at each end | 0.3–0.5 seconds before and after speech | We trim; the model needs clean start and end points |
| Processing | None: no EQ, compression, denoise or normalize | We process everything the same way centrally |

### File naming

`<speakerID>_<promptID>.wav`, for example `F01_cc_0123.wav`. For a retake, record again and overwrite the same name; send only the take you want us to use.

Speaker IDs: voice talents get `F01` and `M01`; contributors get `C01`, `C02`, and so on. We assign them; do not use names in filenames.

### Room-tone file

At the start of each session record 10 seconds of silence, sitting in position, and name it `<speakerID>_roomtone_<date>.wav`. This lets us measure the noise in each session.

## Session workflow

A session is about 90 minutes and produces roughly 150–250 usable prompts.

1. **Set up (10 min).** Check that the tape marks line up, processing is off and the level peaks between −12 and −6 dBFS on a test sentence. Record the room-tone file.
2. **Warm up (5 min).** Read 5–10 prompts aloud without recording. Have water at room temperature nearby; avoid milk, coffee and fizzy drinks just before.
3. **Record in blocks of 20–25 minutes.** Read the prompt silently first, then say it. Leave half a second of silence before you start and after you finish.
4. **Retake immediately** if you stumble, mispronounce, cough, clip, or hear a noise (door, vehicle horn, phone). Overwrite the take with the same filename.
5. **Break for 5 minutes** between blocks. Stand up, drink water, rest your voice.
6. **Stop for the day** if your voice is tired, hoarse or noticeably different. Tired-voice clips teach the model to sound tired.
7. **Upload at the end of each session** (next section), so we can check quality before the next one.

### Keep sessions consistent (voice talents)

- Same mic, same settings, same chair position, same room.
- Listen to 3 clips from your previous session before you start, and match that sound and energy.
- Do not record with a cold or sore throat; reschedule instead.
- Avoid clothing or jewelry that rustles. Keep your hands still.

## What to send us

After each session, upload a folder named `<speakerID>_<YYYY-MM-DD>` containing the WAV files, the room-tone file and a short notes file. Upload location: to be confirmed.

### Notes file (one per session)

A plain text file `notes.txt` with:

- Prompt IDs you skipped because the text looked wrong, with a word about why.
- Anything unusual: a noise you could not avoid, a change of mic or room, feeling unwell.

### Speaker sheet (once, before your first session)

| Field | Example |
| --- | --- |
| Speaker ID (we assign) | F01 |
| Gender | Female |
| Age range | 25–34 |
| First language | Nepali |
| Region where you grew up | Kathmandu valley |
| Microphone and interface (model names) | Rode NT-USB, direct USB |
| Recording software and settings | Audacity 3.x, 48 kHz, 24-bit, mono |
| Room description | Bedroom, curtains drawn, blanket behind mic |

### Consent (required before any recording is used)

Everyone signs a consent form; voice talents sign a fuller agreement because a synthetic copy of their voice will speak to customers. It should state:

- What the recordings are used for: training speech models, and for voice talents, a synthetic voice used on customer calls.
- Who owns the recordings and the resulting voice model, and for how long they may be used.
- Compensation, if any.
- How to withdraw consent, and what happens to models already trained on the data.
- That the synthetic voice will not be used to impersonate the speaker or say things outside the agreed use.

Open question: legal review of the consent wording before the first session.

## Quality checks we run

We check every session within a day and send back the IDs of any clips to re-record.

| Check | Fails when |
| --- | --- |
| Format | Not WAV, wrong sample rate, or wrong filename |
| Clipping | Any samples at or near 0 dBFS |
| Noise | Room tone louder than −60 dBFS, or SNR below 30 dB |
| Silence | Speech starts or ends within 0.1 s of the file edge (cut off) |
| Speaking rate | Clip is far too long or too short for its text (pauses, skipped words) |
| Text match | A Nepali speech recognizer's transcript differs noticeably from the prompt |
| Listening | A native speaker spot-checks about 1 in 20 clips for pronunciation, tone and noises |

The first session from each voice talent gets a full review before they continue, so problems are caught after 90 minutes rather than after 15 hours.

## Checklist

Before the first session:

- [ ] Consent form signed
- [ ] Speaker sheet sent; speaker ID received
- [ ] Mic is USB/XLR (not laptop or Bluetooth); pop filter fitted
- [ ] All noise suppression, echo cancellation and auto-gain turned off

Every session:

- [ ] Fans and AC off, windows closed, phone silenced
- [ ] Same chair and mic position as last time (tape marks)
- [ ] Recorder set to WAV, 48 kHz, 24-bit, mono
- [ ] Test sentence peaks between −12 and −6 dBFS
- [ ] 10 s room-tone file recorded
- [ ] Read exactly what is written; retake the whole sentence on any slip
- [ ] Half a second of silence before and after each prompt
- [ ] 5-minute break every 20–25 minutes
- [ ] Skipped IDs and anything unusual noted in `notes.txt`
- [ ] Session folder uploaded the same day
