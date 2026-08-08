"""Asset prep for the Boom Pots page. No third-party imaging deps here, so PNG
read/write is done by hand.

Three jobs, one shared trick: flood fill inward from the border. Only pixels
*connected to the edge* count as background, which is what lets us key white out
of art that also contains white on the inside (the ice letters of BOOM, the
cream bands on a pot).

  deglow  strip the baked-in white selection glow off a pot render
  cutout  lift the BOOM POTS wordmark off its white plate
  unkey   key a solid background colour out of the Sokando logo
  unkeygrad  same, but for a background that is a gradient
"""
import struct
import zlib
import sys
from collections import deque


def read_png(path):
    b = open(path, "rb").read()
    i, idat, w, h, ct = 8, b"", 0, 0, 0
    while i < len(b):
        ln = struct.unpack(">I", b[i:i + 4])[0]
        typ = b[i + 4:i + 8]
        data = b[i + 8:i + 8 + ln]
        if typ == b"IHDR":
            w, h, _bd, ct = struct.unpack(">IIBB", data[:10])
        elif typ == b"IDAT":
            idat += data
        i += 8 + ln + 4
    raw = zlib.decompress(idat)
    ch = {0: 1, 2: 3, 4: 2, 6: 4}[ct]
    stride = w * ch
    px = bytearray(w * h * 4)
    prev, o = bytearray(stride), 0
    for y in range(h):
        f = raw[o]
        o += 1
        line = bytearray(raw[o:o + stride])
        o += stride
        if f:
            for x in range(stride):
                a = line[x - ch] if x >= ch else 0
                bb = prev[x]
                c = prev[x - ch] if x >= ch else 0
                if f == 1:
                    line[x] = (line[x] + a) & 255
                elif f == 2:
                    line[x] = (line[x] + bb) & 255
                elif f == 3:
                    line[x] = (line[x] + (a + bb) // 2) & 255
                else:
                    p = a + bb - c
                    pa, pb, pc = abs(p - a), abs(p - bb), abs(p - c)
                    pr = a if (pa <= pb and pa <= pc) else (bb if pb <= pc else c)
                    line[x] = (line[x] + pr) & 255
        base = y * w * 4
        for x in range(w):
            s = x * ch
            if ch == 4:
                px[base + x * 4:base + x * 4 + 4] = line[s:s + 4]
            elif ch == 3:
                px[base + x * 4:base + x * 4 + 3] = line[s:s + 3]
                px[base + x * 4 + 3] = 255
            elif ch == 2:
                v = line[s]
                px[base + x * 4:base + x * 4 + 4] = bytes((v, v, v, line[s + 1]))
            else:
                v = line[s]
                px[base + x * 4:base + x * 4 + 4] = bytes((v, v, v, 255))
        prev = line
    return w, h, px


def write_png(path, w, h, px):
    raw = b"".join(b"\x00" + bytes(px[y * w * 4:(y + 1) * w * 4]) for y in range(h))

    def chunk(t, d):
        return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xFFFFFFFF)

    open(path, "wb").write(
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(raw, 9))
        + chunk(b"IEND", b"")
    )


def crop_to_content(w, h, px, keep):
    x0, y0, x1, y1 = w, h, -1, -1
    for y in range(h):
        row = y * w
        for x in range(w):
            if keep(row + x):
                if x < x0: x0 = x
                if x > x1: x1 = x
                if y < y0: y0 = y
                if y > y1: y1 = y
    if x1 < 0:
        raise SystemExit("nothing left after keying")
    pad = 8
    x0, y0 = max(0, x0 - pad), max(0, y0 - pad)
    x1, y1 = min(w - 1, x1 + pad), min(h - 1, y1 + pad)
    cw, ch = x1 - x0 + 1, y1 - y0 + 1
    out = bytearray(cw * ch * 4)
    for y in range(ch):
        src = ((y + y0) * w + x0) * 4
        out[y * cw * 4:(y + 1) * cw * 4] = px[src:src + cw * 4]
    return cw, ch, out


def flood_border(w, h, matches):
    flag = bytearray(w * h)
    q = deque()
    for x in range(w):
        q.append(x)
        q.append((h - 1) * w + x)
    for y in range(h):
        q.append(y * w)
        q.append(y * w + w - 1)
    while q:
        i = q.popleft()
        if flag[i] or not matches(i):
            continue
        flag[i] = 1
        x, y = i % w, i // w
        if x > 0: q.append(i - 1)
        if x < w - 1: q.append(i + 1)
        if y > 0: q.append(i - w)
        if y < h - 1: q.append(i + w)
    return flag


cmd, src, dst = sys.argv[1], sys.argv[2], sys.argv[3]
W, H, PX = read_png(src)

if cmd == "deglow":
    def glowish(i):
        o = i * 4
        r, g, b, a = PX[o], PX[o + 1], PX[o + 2], PX[o + 3]
        if a == 0:
            return True
        mn, mx = min(r, g, b), max(r, g, b)
        if mn > 202 and mx - mn < 46:
            return True
        return a < 250 and mn > 168 and mx - mn < 62

    flag = flood_border(W, H, glowish)
    n = 0
    for i in range(W * H):
        if flag[i] and PX[i * 4 + 3]:
            PX[i * 4:i * 4 + 4] = b"\x00\x00\x00\x00"
            n += 1
    cw, ch, out = crop_to_content(W, H, PX, lambda i: PX[i * 4 + 3] > 8)
    write_png(dst, cw, ch, out)
    print(f"deglow {src.split('/')[-1]}: cleared {n}px -> {dst.split('/')[-1]} {cw}x{ch}")

elif cmd == "cutout":
    def platey(i):
        o = i * 4
        return 255 - min(PX[o], PX[o + 1], PX[o + 2]) <= 34

    flag = flood_border(W, H, platey)
    for i in range(W * H):
        o = i * 4
        if flag[i]:
            a = 255 - max(PX[o], PX[o + 1], PX[o + 2])
            PX[o:o + 4] = bytes((0, 0, 0, 0 if a < 6 else a))
    cw, ch, out = crop_to_content(W, H, PX, lambda i: PX[i * 4 + 3] > 24)
    write_png(dst, cw, ch, out)
    print(f"cutout -> {dst.split('/')[-1]} {cw}x{ch}")

elif cmd == "unkeygrad":
    # Background is a grey radial gradient with a warm glow baked over it, so a
    # single sampled colour will not do. Estimate the ground per row from the
    # outer columns and lerp across, then treat distance from that estimate as
    # alpha. The glow survives as translucent orange; the grey does not.
    EDGE = 40
    T = 96.0
    FLOOR = 15          # below this the difference is just gradient curvature

    def med(vals):
        v = sorted(vals)
        return v[len(v) // 2]

    for y in range(H):
        row = y * W
        lo = [[PX[(row + x) * 4 + c] for x in range(EDGE)] for c in range(3)]
        hi = [[PX[(row + W - 1 - x) * 4 + c] for x in range(EDGE)] for c in range(3)]
        L = [med(lo[c]) for c in range(3)]
        R = [med(hi[c]) for c in range(3)]
        for x in range(W):
            t = x / (W - 1)
            o = (row + x) * 4
            est = [L[c] + (R[c] - L[c]) * t for c in range(3)]
            d = max(abs(PX[o + c] - est[c]) for c in range(3))
            if d <= FLOOR:
                PX[o:o + 4] = b"\x00\x00\x00\x00"
                continue
            a = min(1.0, (d - FLOOR) / T)
            if a >= 0.88:
                PX[o + 3] = 255
            else:
                inv = 1.0 / a
                for c in range(3):
                    PX[o + c] = min(255, max(0, int(est[c] + (PX[o + c] - est[c]) * inv)))
                PX[o + 3] = int(a * 255)
    # A baked glow cannot be recovered by this method. Its distance from the grey
    # ground overlaps the logo's own mid-tones (terracotta sits ~95 away, the hot
    # core of the glow ~70), so no threshold separates them: cut low enough to
    # kill the haze and it starts eating pot bodies. Anything faint and reachable
    # from the border is dropped, and the page draws its own glow in CSS.
    faint = flood_border(W, H, lambda i: PX[i * 4 + 3] < 140)
    for i in range(W * H):
        if faint[i]:
            PX[i * 4:i * 4 + 4] = b"\x00\x00\x00\x00"

    cw, ch, out = crop_to_content(W, H, PX, lambda i: PX[i * 4 + 3] > 30)
    write_png(dst, cw, ch, out)
    print(f"unkeygrad -> {dst.split('/')[-1]} {cw}x{ch}")

elif cmd == "unkey":
    BR, BG_, BB = PX[0], PX[1], PX[2]
    T = 100.0
    print(f"background sampled: rgb({BR},{BG_},{BB})")
    for i in range(W * H):
        o = i * 4
        r, g, b = PX[o], PX[o + 1], PX[o + 2]
        d = max(abs(r - BR), abs(g - BG_), abs(b - BB))
        if d <= 6:
            PX[o:o + 4] = b"\x00\x00\x00\x00"
            continue
        a = d / T
        if a >= 0.85:
            PX[o + 3] = 255
        else:
            inv = 1.0 / a
            PX[o] = min(255, max(0, int(BR + (r - BR) * inv)))
            PX[o + 1] = min(255, max(0, int(BG_ + (g - BG_) * inv)))
            PX[o + 2] = min(255, max(0, int(BB + (b - BB) * inv)))
            PX[o + 3] = int(a * 255)
    cw, ch, out = crop_to_content(W, H, PX, lambda i: PX[i * 4 + 3] > 28)
    write_png(dst, cw, ch, out)
    print(f"unkey -> {dst.split('/')[-1]} {cw}x{ch}")
