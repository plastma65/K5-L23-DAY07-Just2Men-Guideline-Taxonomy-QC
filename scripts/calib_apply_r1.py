"""Áp quyết định calibration R1: occluded_level lấy theo nhãn Lâm (2A202603227) đã tự gán.

Nền: bản export CVAT của Task calibration (submission/qc/labels_calibrated_flagged.json).
Mỗi box nền được ghép 1-1 (IoU >= 0.5, cùng lớp, không phải ignore_region) với box của Lâm
trong cùng ảnh; nếu ghép được thì occluded_level := giá trị của Lâm. Không đổi box, lớp hay thuộc tính khác.
Ra: work/calib/consensus_flagged_R1.json (nạp lại vào CVAT) + work/calib/r1_changes.csv (nhật ký).
"""
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from common import iou, load_coco, load_taxonomy, xywh_to_xyxy  # noqa: E402

LAM = ROOT / "submission/labels/2A202603227_DoanTungLam.json"
BASE = ROOT / "submission/qc/labels_calibrated_flagged.json"
OUT = ROOT / "work/calib/consensus_flagged_R1.json"
LOG = ROOT / "work/calib/r1_changes.csv"

tax = load_taxonomy()
lam = load_coco(LAM, tax)
data = json.loads(BASE.read_text(encoding="utf8"))
cats = {c["id"]: c["name"] for c in data["categories"]}
imgs = {i["id"]: Path(i["file_name"]).name for i in data["images"]}

by_img = {}
for a in data["annotations"]:
    by_img.setdefault(imgs[a["image_id"]], []).append(a)

log, n_match, n_change = [], 0, 0
for img, anns in by_img.items():
    cands = []
    for a in anns:
        cls = cats[a["category_id"]]
        if cls == tax.ignore:
            continue
        for j, o in enumerate(lam.objects.get(img, [])):
            if o.cls == cls:
                v = iou(xywh_to_xyxy(a["bbox"]), o.box)
                if v >= 0.5:
                    cands.append((v, id(a), j, a, o))
    used_a, used_l = set(), set()
    for v, aid, j, a, o in sorted(cands, key=lambda t: -t[0]):  # ghép tham lam theo IoU giảm dần
        if aid in used_a or j in used_l:
            continue
        used_a.add(aid); used_l.add(j); n_match += 1
        attrs = a.setdefault("attributes", {})
        old = str(attrs.get("occluded_level", tax.default("occluded_level")))
        new = o.attrs["occluded_level"]
        if old != new:
            attrs["occluded_level"] = new
            n_change += 1
            log.append({"image": img, "class": cats[a["category_id"]], "bbox_xywh": [round(x) for x in a["bbox"]],
                        "occluded_level_cu": old, "occluded_level_moi_theo_Lam": new, "iou_voi_box_Lam": round(v, 2)})

OUT.write_text(json.dumps(data, ensure_ascii=False), encoding="utf8")
with open(LOG, "w", encoding="utf8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(log[0].keys()) if log else ["image"])
    w.writeheader(); w.writerows(log)
n_obj = sum(1 for a in data["annotations"] if cats[a["category_id"]] != tax.ignore)
print(f"Box vật trong nền: {n_obj}; ghép được với box Lâm: {n_match}; đổi occluded_level: {n_change}")
print(f"Ghi: {OUT.relative_to(ROOT)}, {LOG.relative_to(ROOT)}")
