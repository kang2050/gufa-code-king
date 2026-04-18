"""
Gen 6 new illustrations via OpenRouter + google/gemini-3-pro-image-preview.
Protagonist reference image + shared style anchor baked into every prompt.
"""
import base64
import json
import sys
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import urllib.request

API_KEY = "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"
ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "google/gemini-3-pro-image-preview"
PROXY = "http://127.0.0.1:10808"

ROOT = Path(__file__).resolve().parent.parent
REF_IMG = ROOT / "web" / "images" / "protagonist_reference.jpg"
OUT_DIR = ROOT / "web" / "images" / "extra"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Shared style anchor — extracted from docs/illustration_style_guide.md
STYLE_ANCHOR = """
Cinematic near-future urban realism. Muted, cold blue-grey palette. 35mm film grain. Subtle cold screen glow where screens appear. Photographic, NOT cartoon, NOT anime. Realistic human proportions. Emotion conveyed through posture, gaze and environment, NOT through exaggerated facial expression. 16:9 cinematic framing.
""".strip()

# Character anchor — must be repeated every time to keep consistency
CHAR_ANCHOR = """
The man in the attached reference image is GU CHENZHOU. Keep his identity consistent: black short hair (slightly messy in earlier life, neater later), deep-set brows, quiet reserved demeanor, slim build.
""".strip()

SCENES = [
    {
        "id": "ch06_panic_night",
        "age_hint": "around 25 years old, haggard, unshaven, clothes wrinkled",
        "scene": "A dim cramped rental room at night. GU CHENZHOU is curled up against the wall in a corner, knees to chest, hands covering his ears. A single thin beam of moonlight crosses the ceiling. On the small bedside table there is only a glass of cold water. The room is otherwise empty and in half-darkness. No other characters. His face is not crying — his eyes are open and fixed on nothing. The whole composition conveys a panic attack that no one sees.",
        "mood": "Cold blue-grey. Shadow occupies 70% of the frame. Silent. Oppressive ceiling. PTSD origin point."
    },
    {
        "id": "ch10_cafe_read_alone",
        "age_hint": "around 40 years old, clean-shaven but visibly exhausted, a thin shaven old scar on the suit cuff edge",
        "scene": "A small 24-hour cafe, very late afternoon cold grey light through the window. GU CHENZHOU sits alone at a two-person table by the window, wearing a plain dark grey old suit that has clearly been ironed carefully but whose cuffs have been slightly frayed. A plain black coffee cup sits in front of him. On the table, 30 pages of handwritten typed speech manuscript are spread open. His right index finger rests on the first line of the first page. His head is slightly tilted down. He is reading the manuscript to himself, alone. The background is out of focus — empty cafe, a couple of empty chairs. The mood is not sad, not angry, only quietly ceremonial.",
        "mood": "Cool muted light. Solitary. Ceremonial quietness. Middle-aged composure."
    },
    {
        "id": "ch14_linwanqiao_window",
        "age_hint": "NOT the protagonist — focus on a different character, a composed woman in her mid-30s named LIN WANQIAO",
        "scene": "Floor-to-ceiling window of the 31st floor of a city office tower, late morning under heavy overcast sky. A composed elegant Chinese woman in her mid-30s, wavy shoulder-length hair, beige trench coat, pale gold earrings, stands with her back turned to the viewer, facing the window. In her hand she holds a cup of coffee, faint steam rising. On a wall-mounted flat TV to her right, the screen shows ONLY a silent footage: a dim gray narrow city alley, an unmarked black van parked at the alley entrance, a thin-shouldered Chinese man in a plain worn dark coat walking past the van carrying a plain black canvas shoulder bag. The TV screen shows NO NEWS BANNER, NO ENGLISH TEXT, NO HEADLINE, NO SUBTITLE — the entire screen is just the alley footage with cinematic film grain. The open-plan office behind her is chaotic — out-of-focus colleagues crowded around a projector in a distant glass-walled meeting room. She herself stands still, not moving. Camera framed from slightly behind her shoulder. Her face cannot be seen clearly.",
        "mood": "Cold blue-white. The city in the background is in disarray, stillness in the foreground. A look across time, regret without tears. ABSOLUTELY NO TEXT ANYWHERE ON THE TV OR IN THE SCENE."
    },
    {
        "id": "ch16_victory_night_alone",
        "age_hint": "around 50 years old, eyes bloodshot, face exhausted",
        "scene": "A temporary small emergency centre rest room at night, door locked. GU CHENZHOU sits on the floor with his back against the door. Next to him on the floor is a premium glass liquor bottle with its neck snapped off — glass shards around it. His palm has a thin red cut but he does not tend to it. A small framed mirror on the opposite wall shows his own reflection — bloodshot eyes, dry eyelids, stubble. He is not crying. His hand rests on his forehead. There is no one else in the room. Cold fluorescent ceiling light. Outside the door (implied faintly through sound lines, not visible) people are celebrating — but he is silent. Ultra quiet composition.",
        "mood": "The emptiness of victory. Cold overhead light. More unsettling than any defeat scene."
    },
    {
        "id": "ring_classroom_10yrs_later",
        "age_hint": "NOT the protagonist — a new young professor in his early 40s, different face, carrying GU CHENZHOU's legacy",
        "scene": "A university lecture hall for freshmen, first class of the semester, bright practical fluorescent light, about 100 first-year students visible at the back of frame, heads slightly turned up. At the front a young professor in his early 40s, thin, intense, wearing a simple dark sweater. He has set an old worn canvas bag on the lecturer's desk — the side of the bag reads the faded handwriting 'GUIXU · 2038'. On the large blackboard behind him he has just finished writing three Chinese characters in chalk: '写 代 码' (very prominent, centered, large). He stands still, chalk in hand, turning to face the students. An old worn hand-bound notebook lies open on the desk in front of him — the first page visible. Mood: warm respect, a new generation inheriting.",
        "mood": "Warm but restrained light. A ring closes — echoing back to Ch 1 graduation recruiting banner but inverted meaning."
    },
    {
        "id": "s2_blank_second_page",
        "age_hint": "around 64 years old — NOT older, NOT 70+. Hair is salt-and-pepper with roughly equal black and grey strands, still thick and neatly combed, NOT bald, NOT thinning on top. Face remains the same person as in the reference image — just aged by about 20 years. Slim but upright posture. Still composed and sharp.",
        "scene": "A clean simple home study by a wide river window at dusk. Warm golden horizontal sunset light cutting in across a worn wooden desk. GU CHENZHOU, same face as the reference image but about 64 years old, hair still thick but now half black half grey, sits alone at the desk. On the desk, in the foreground: an old worn canvas shoulder bag with the faded handwritten text 'GUIXU · 2038' on its side — the bag lies open. A very old small hand-bound notebook lies open on the desk — the first page shows one line of small hand-written Chinese characters; the second page is completely blank. His hand with slightly prominent veins rests lightly on the blank second page. His eyes are fixed on the empty page, a silent expression of doubt. To his right, a slim modern laptop sits — its screen glowing faintly — on the laptop screen is a nearly-empty minimal text editor, and at the top of the editor three large Chinese characters are clearly readable: '我 怕 的——' followed by a blinking cursor. The laptop screen is positioned and framed so the viewer can clearly read those three Chinese characters. No other person in the room. Absolute stillness.",
        "mood": "Quiet, ceremonial, doubt. An old hero facing a second choice. Open ending. Warm golden light against the cold blue river outside."
    },
]


def build_prompt(scene: dict) -> str:
    return "\n\n".join([
        "GENERATE ONE cinematic illustration.",
        f"STYLE: {STYLE_ANCHOR}",
        f"CHARACTER: {CHAR_ANCHOR}",
        f"AGE/APPEARANCE: {scene['age_hint']}",
        f"SCENE: {scene['scene']}",
        f"MOOD: {scene['mood']}",
        "IMPORTANT: no visible text overlays beyond what is described in SCENE. No watermarks. Output a single full 16:9 image only."
    ])


def encode_ref_image() -> str:
    with open(REF_IMG, "rb") as f:
        return "data:image/jpeg;base64," + base64.b64encode(f.read()).decode()


def call_api(scene: dict, ref_data_url: str) -> bytes:
    body = {
        "model": MODEL,
        "modalities": ["image", "text"],
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": ref_data_url}},
                    {"type": "text", "text": build_prompt(scene)}
                ]
            }
        ]
    }
    req = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(body).encode(),
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://gufa-code.kang-kang.com",
            "X-Title": "Gufa Code King Illustrations",
        },
        method="POST"
    )
    proxy_handler = urllib.request.ProxyHandler({"http": PROXY, "https": PROXY})
    opener = urllib.request.build_opener(proxy_handler)
    with opener.open(req, timeout=180) as resp:
        data = json.loads(resp.read())
    if "error" in data:
        raise RuntimeError(f"{scene['id']}: {data['error']}")
    msg = data["choices"][0]["message"]
    imgs = msg.get("images", [])
    if not imgs:
        raise RuntimeError(f"{scene['id']}: no images in response — msg keys {list(msg.keys())}")
    url = imgs[0]["image_url"]["url"]
    if not url.startswith("data:image"):
        raise RuntimeError(f"{scene['id']}: unexpected url format")
    b64 = url.split(",", 1)[1]
    cost = data.get("usage", {}).get("cost", 0)
    print(f"  ✓ {scene['id']}  cost=${cost:.4f}  size={len(b64) // 1024} KB b64", flush=True)
    return base64.b64decode(b64)


def generate_one(scene: dict, ref_data_url: str) -> tuple[str, Path | None, str | None]:
    t0 = time.time()
    try:
        png = call_api(scene, ref_data_url)
        out = OUT_DIR / f"{scene['id']}.png"
        out.write_bytes(png)
        dt = time.time() - t0
        print(f"  saved {out.name}  ({dt:.1f}s, {len(png) // 1024}KB)", flush=True)
        return scene["id"], out, None
    except Exception as e:
        dt = time.time() - t0
        print(f"  ✗ {scene['id']}  FAILED after {dt:.1f}s: {e}", flush=True)
        return scene["id"], None, str(e)


def main():
    only = sys.argv[1:] if len(sys.argv) > 1 else None
    scenes = [s for s in SCENES if not only or s["id"] in only]
    print(f"=== gen {len(scenes)} images ===")
    if only:
        print(f"filter: {only}")
    print(f"ref image: {REF_IMG} ({REF_IMG.stat().st_size // 1024}KB)")
    ref_url = encode_ref_image()
    print(f"ref base64 len: {len(ref_url) // 1024}KB")
    print(f"out dir: {OUT_DIR}")
    print()
    print("scenes:")
    for s in scenes:
        print(f"  - {s['id']}")
    print()

    results = []
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = [pool.submit(generate_one, s, ref_url) for s in scenes]
        for f in as_completed(futures):
            results.append(f.result())

    print()
    print("=== summary ===")
    ok = [r for r in results if r[1]]
    fail = [r for r in results if not r[1]]
    print(f"  ok: {len(ok)}  fail: {len(fail)}")
    if fail:
        for sid, _, err in fail:
            print(f"  fail {sid}: {err}")
        sys.exit(1)


if __name__ == "__main__":
    main()
