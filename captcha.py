from PIL import Image, ImageFont, ImageDraw
import random


def generate_captcha_from_text(input_text: str, Line_Chars: int) -> Image:
    sImg = "base.png"  # source image
    sFont = "AdwaitaMono-Regular.ttf"  # font file
    sSize = random.randint(28, 32)  # font size
    sColor = (1, 1, 1)  # text color
    sPos = (random.randint(0, 30), random.randint(0, 30))  # write text at this position
    ind = 0
    nls = 0
    sText = ""
    for i in input_text:
        ind += 1
        sText += i
        if ind % Line_Chars == 0:
            sText += "\n"
            nls += 1
            if nls > 6:
                raise ValueError("Text too long")

    iOpen = Image.open(sImg)
    pixels = iOpen.load()
    width, height = iOpen.size
    for h in range(height):
        for w in range(width):
            pixels[w, h] = (
                random.randint(0, 100),
                random.randint(0, 100),
                random.randint(0, 150),
            )
    shape = 2
    chunk = 0
    cCol = (
        random.randint(75, 230),
        random.randint(75, 230),
        random.randint(100, 255),
    )
    b = False
    while shape > 0:
        for he in range(height):
            h = min(height, he + 100)
            for w in range(width):
                if random.randrange(0, 100) < 1:
                    shape -= 1
                    if shape < 0:
                        b = True
                    if not b:
                        for p in range(random.randint(20, 60)):
                            for wp in range(random.randint(0, width - w - 1)):
                                if chunk > 100:
                                    chunk = 0
                                    cCol = (
                                        random.randint(75, 230),
                                        random.randint(75, 230),
                                        random.randint(100, 255),
                                    )
                                """print(width)
                                print(height)
                                print(w + wp)
                                print(h + p)
                                print(shape)
                                print()"""
                                pixels[w + wp, h + p] = cCol
                                chunk += 1
                        h += p
    iDraw = ImageDraw.Draw(iOpen)
    iFont = ImageFont.truetype(sFont, sSize)
    iDraw.text(
        sPos,
        sText,
        fill=sColor,
        font=iFont,
        # stroke_width=2,
        # stroke_fill=(254, 254, 254),
    )
    pixels = iOpen.load()
    chunk = 0
    cCol = (
        random.randint(80, 255),
                        random.randint(120, 255),
                        random.randint(80, 255),
    )
    for h in range(height):
        for w in range(width):
            if is_similar(pixels[w, h], sColor, THRESHOLD):
                if chunk > 30:
                    chunk = 0
                    cCol = (
                        random.randint(80, 255),
                        random.randint(120, 255),
                        random.randint(80, 255),
                    )
                pixels[w, h] = cCol
                chunk += 1
            """if is_similar(pixels[w, h], (254, 254, 254), THRESHOLD):
                pixels[w, h] = (
                    random.randint(100, 255),
                    random.randint(100, 255),
                    random.randint(100, 255),
                )"""
    for i in range(int((w * h) * (random.randint(5, 30) / 75))):
        pixels[random.randint(0, w), random.randint(0, h)] = (
            random.randint(150, 255),
            random.randint(150, 255),
            random.randint(150, 255),
        )
    return iOpen


def read_challenges_from_file(CHALLENGES_FILE: str) -> dict[str : set[str]]:
    challenges: dict[str : set[str]] = {}
    with open(CHALLENGES_FILE, "r") as f:
        for l in f.readlines():
            l = l.split(":")
            question = l[0].strip()
            answers = l[1].split(",")
            for a in answers:
                answers[answers.index(a)] = a.strip().strip("\n")
            answers = set(answers)
            challenges[question] = answers
    return challenges


def luminance(pixel):
    return 0.299 * pixel[0] + 0.587 * pixel[1] + 0.114 * pixel[2]


def is_similar(pixel_a, pixel_b, threshold):
    return abs(luminance(pixel_a) - luminance(pixel_b)) < threshold


THRESHOLD = 30


def get_challenge_questions(challenges):
    listkeys = []
    for k in challenges.keys():
        listkeys.append(k)
    return listkeys


if __name__ == "__main__":
    challenges = read_challenges_from_file(r"challenges.txt")
    generate_captcha_from_text(random.choice(get_challenge_questions(challenges)))
