import sys, pymupdf
src, dst = sys.argv[1], sys.argv[2]
IT = {"lado izquierdo": "lato sinistro", "frente y atrás": "fronte e retro",
      "lado derecho": "lato destro", "base": "base", "techo": "tetto"}
doc = pymupdf.open(src)
for page in doc:
    spans = []
    for b in page.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            for s in l["spans"]:
                if s["text"].strip():
                    spans.append(s)
    for s in spans:
        page.add_redact_annot(pymupdf.Rect(s["bbox"]), fill=(1, 1, 1))
    page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE)
    for s in spans:
        t = IT.get(s["text"].strip(), s["text"])
        page.insert_text(s["origin"], t, fontsize=s["size"], fontname="helv")
        print(repr(s["text"]), "->", t, round(s["size"], 1))
doc.save(dst)
