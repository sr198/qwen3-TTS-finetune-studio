"""Nepali number, date and time verbalization.

Spellings for 0-99 follow the forms most frequent in the OpenSLR 43/54
transcripts. 54 (चवन्न) does not occur there and needs native review.
The same module must back the inference-time text normalizer, so training
text and runtime text stay spelled identically.
"""

ONES = (
    "शून्य एक दुई तीन चार पाँच छ सात आठ नौ "
    "दश एघार बाह्र तेह्र चौध पन्ध्र सोह्र सत्र अठार उन्नाइस "
    "बीस एक्काइस बाइस तेइस चौबीस पच्चीस छब्बीस सत्ताइस अट्ठाइस उनन्तीस "
    "तीस एकत्तीस बत्तीस तेत्तीस चौँतीस पैँतीस छत्तीस सैँतीस अठतीस उनन्चालीस "
    "चालीस एकचालीस बयालीस त्रिचालीस चवालीस पैँतालीस छयालीस सच्चालीस अठचालीस उनन्चास "
    "पचास एकाउन्न बाउन्न त्रिपन्न चवन्न पचपन्न छपन्न सन्ताउन्न अन्ठाउन्न उनान्साठी "
    "साठी एकसट्ठी बयसट्ठी त्रिसट्ठी चौंसट्ठी पैंसट्ठी छयसट्ठी सतसट्ठी अठसट्ठी उनन्सत्तरी "
    "सत्तरी एकहत्तर बहत्तर त्रिहत्तर चौहत्तर पचहत्तर छयहत्तर सतहत्तर अठहत्तर उनासी "
    "अस्सी एकासी बयासी त्रियासी चौरासी पचासी छयासी सतासी अठासी उनान्नब्बे "
    "नब्बे एकान्नब्बे बयान्नब्बे त्रियान्नब्बे चौरान्नब्बे पन्चान्नब्बे छयान्नब्बे सन्तान्नब्बे अन्ठान्नब्बे उनान्सय"
).split()
assert len(ONES) == 100

# Nepali grouping: ... करोड | लाख | हजार | सय | ones
SCALES = [(10**9, "अर्ब"), (10**7, "करोड"), (10**5, "लाख"), (10**3, "हजार"), (100, "सय")]

BS_MONTHS = ["बैशाख", "जेठ", "असार", "साउन", "भदौ", "असोज",
             "कात्तिक", "मंसिर", "पुस", "माघ", "फागुन", "चैत"]

CURRENCY = "रुपैयाँ"  # corpus also has रूपैयाँ; the normalizer must use the same form


def num_to_words(n: int) -> str:
    if n < 0:
        return "माइनस " + num_to_words(-n)
    if n < 100:
        return ONES[n]
    parts = []
    for value, word in SCALES:
        if n >= value:
            q, n = divmod(n, value)
            parts.append(f"{num_to_words(q)} {word}")
    if n:
        parts.append(ONES[n])
    return " ".join(parts)


def digits_to_words(s: str) -> str:
    """Read a digit string one digit at a time (phone, account, OTP)."""
    return " ".join(ONES[int(c)] for c in s if c.isdigit())


def amount_to_words(rupees: int, paisa: int = 0) -> str:
    out = f"{num_to_words(rupees)} {CURRENCY}"
    if paisa:
        out += f" {num_to_words(paisa)} पैसा"
    return out


def bs_date_to_words(year: int, month: int, day: int, with_year: bool = True) -> str:
    """Bikram Sambat date, e.g. 2081-07-15 -> दुई हजार एकासी साल कात्तिक पन्ध्र गते."""
    d = f"{BS_MONTHS[month - 1]} {num_to_words(day)} गते"
    return f"{num_to_words(year)} साल {d}" if with_year else d


def time_to_words(hour: int, minute: int = 0) -> str:
    """12-hour clock with day-part prefix; quarter/half forms like a speaker says them."""
    part = ("बिहान" if 4 <= hour < 12 else "दिउँसो" if 12 <= hour < 16
            else "बेलुका" if 16 <= hour < 20 else "राति")
    h = hour % 12 or 12
    if minute == 0:
        return f"{part} {num_to_words(h)} बजे"
    if minute == 15:
        return f"{part} सवा {num_to_words(h)} बजे"
    if minute == 30:
        return f"{part} साढे {num_to_words(h)} बजे"
    if minute == 45:
        return f"{part} पौने {num_to_words(h % 12 + 1)} बजे"
    return f"{part} {num_to_words(h)} बजेर {num_to_words(minute)} मिनेट"


if __name__ == "__main__":
    for n in [0, 7, 54, 100, 105, 1250, 125450, 10000000, 2081]:
        print(n, num_to_words(n))
    print(amount_to_words(125450, 50))
    print(digits_to_words("9841234567"))
    print(bs_date_to_words(2081, 7, 15))
    for h, m in [(10, 0), (15, 30), (17, 45), (9, 15), (11, 20)]:
        print(h, m, time_to_words(h, m))
