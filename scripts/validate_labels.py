"""Kiểm tra file nhãn COCO (export từ CVAT) TRƯỚC KHI nộp.

    python scripts/validate_labels.py --all
    python scripts/validate_labels.py submission/labels/123_NguyenVanA.json

Kiểm: tên file, tên lớp, giá trị thuộc tính, box trong ảnh, box quá nhỏ, ảnh đủ/thừa so với danh sách được giao.
Exit code 1 nếu có ERROR.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

from common import IMAGES_DIR, ROOT, Taxonomy, list_label_files, load_assignment, load_coco, load_taxonomy, rel

# MSHV có thể chứa chữ cái (VD 2A202603230): cho phép chữ + số, bắt đầu bằng chữ số.
NAME_RE = re.compile(r"^(\d[0-9A-Za-z]*)_([A-Za-z0-9_\-]+)\.json$")


def validate(path: Path, tax: Taxonomy, assignment) -> tuple:
    errs, warns = [], []
    m = NAME_RE.match(path.name)
    if not m:
        errs.append("Tên file phải dạng <MSHV>_<HoTen>.json, MSHV là chữ số (có thể kèm chữ cái), HoTen viết liền không dấu "
                    "(VD: 20001_NguyenVanA.json). Hãy đổi tên file.")
    try:
        lf = load_coco(path, tax)
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        return [f"Không đọc được file như COCO JSON ({e}). Export lại từ CVAT: Actions -> Export task dataset -> COCO 1.0."], [], Counter()
    warns += [f"{p}" for p in lf.problems]
    counts = Counter()
    missing_attr = Counter()
    for img, objs in lf.objects.items():
        w, h = lf.images[img]
        if not (IMAGES_DIR / img).exists():
            errs.append(f"{img}: không có trong data/images/ (tên ảnh trong file không khớp ảnh gốc).")
        for o in objs:
            tag = f"{img} (annotation id={o.id}, lớp {o.cls})"
            if o.cls not in tax.classes:
                errs.append(f"{tag}: lớp '{o.cls}' KHÔNG thuộc taxonomy {tax.classes}. Sửa tên lớp trong CVAT.")
                continue
            counts[o.cls] += 1
            x1, y1, x2, y2 = o.box
            if x2 - x1 <= 0 or y2 - y1 <= 0:
                errs.append(f"{tag}: box có chiều rộng/cao <= 0.")
                continue
            if w and h and (x1 < -1 or y1 < -1 or x2 > w + 1 or y2 > h + 1):
                errs.append(f"{tag}: box [{x1:.0f},{y1:.0f},{x2:.0f},{y2:.0f}] vượt ra ngoài ảnh {w}x{h}.")
            if o.cls != tax.ignore and (y2 - y1) < tax.rules["min_box_height_px"]:
                warns.append(f"{tag}: cao {y2 - y1:.0f}px < {tax.rules['min_box_height_px']}px -> theo quy tắc nên "
                             f"gộp vào một vùng {tax.ignore}.")
            if o.cls != tax.ignore:
                for n in tax.attrs:
                    if n not in o.raw_attrs:
                        missing_attr[n] += 1
                    elif not tax.valid(n, o.attrs[n]):
                        errs.append(f"{tag}: thuộc tính {n}='{o.raw_attrs[n]}' không hợp lệ "
                                    f"(chỉ nhận {tax.attrs[n].get('values') or 'true/false'}).")
    for n, c in missing_attr.items():
        warns.append(f"{c} đối tượng thiếu thuộc tính '{n}' (coi như giá trị mặc định '{tax.attrs[n].get('default')}'). "
                     f"Kiểm tra lại khi export / đã khai báo thuộc tính trong CVAT chưa.")
    if assignment is not None and m:
        mshv = m.group(1)
        mine = {i for i, a in assignment.items() if mshv in a}
        if not mine:
            errs.append(f"MSHV {mshv} không có trong assignment.csv. Kiểm tra lại tên file / danh sách --members.")
        else:
            have = set(lf.images)
            miss, extra = sorted(mine - have), sorted(have - mine)
            if miss:
                errs.append(f"Thiếu {len(miss)} ảnh được giao: {', '.join(miss[:8])}{' ...' if len(miss) > 8 else ''}. "
                            "Gán nốt rồi export lại (ảnh không có vật vẫn phải nằm trong task).")
            if extra:
                warns.append(f"Có {len(extra)} ảnh KHÔNG được giao cho bạn: {', '.join(extra[:8])}"
                             f"{' ...' if len(extra) > 8 else ''} (sẽ bị bỏ qua khi QC).")
    return errs, warns, counts


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="*", help="File nhãn cần kiểm")
    ap.add_argument("--all", action="store_true", help="Kiểm mọi file trong submission/labels/")
    args = ap.parse_args()
    tax = load_taxonomy()
    files = [Path(f) for f in args.files] or (list_label_files() if args.all else [])
    if not files:
        ap.error("Chưa chỉ định file. Dùng --all hoặc truyền đường dẫn file nhãn.")
    assignment = load_assignment()
    if assignment is None:
        print("(Chưa có submission/qc/assignment.csv -> bỏ qua kiểm ảnh đủ/thừa. Chạy split_assign.py trước.)\n")
    total_err = 0
    for p in files:
        errs, warns, counts = validate(p, tax, assignment)
        total_err += len(errs)
        print(f"=== {rel(p.resolve())}: {len(errs)} lỗi, {len(warns)} cảnh báo")
        for e in errs:
            print(f"  [ERROR] {e}")
        for w in warns:
            print(f"  [WARN]  {w}")
        if counts:
            print("  Số box theo lớp: " + ", ".join(f"{c}={n}" for c, n in sorted(counts.items())))
    print("\n" + ("KẾT QUẢ: có lỗi, hãy sửa và export lại trước khi nộp." if total_err else "KẾT QUẢ: không có ERROR."))
    print("LƯU Ý: script này chỉ kiểm định dạng/quy tắc máy kiểm được. Script KHÔNG biết box có ôm sát vật hay không, "
          "lớp có đúng thực tế không, có bỏ sót vật hay không - phần đó cần mắt người (QC).")
    sys.exit(1 if total_err else 0)


if __name__ == "__main__":
    main()
