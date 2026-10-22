# Büyücü efekt dokuları: Blender'daki tm_fx_flame.py / tm_fx_more.py gölgelendiricilerinin numpy karşılığı
# (Blender bu bağlantıda render sırasında çöktüğü için). Çıktı: fx_flame0/1.png, fx_boom.png (4x4 atlas), fx_frost.png.
import numpy as np, sys
from PIL import Image
OUT = sys.argv[1] if len(sys.argv) > 1 else '.'
rng = np.random.default_rng(7)
P = rng.permutation(256); P = np.concatenate([P, P])
G3 = rng.normal(size=(256, 3)); G3 /= np.linalg.norm(G3, axis=1, keepdims=True)

def perlin3(x, y, z):
    xi, yi, zi = np.floor(x).astype(int), np.floor(y).astype(int), np.floor(z).astype(int)
    xf, yf, zf = x - xi, y - yi, z - zi
    f = lambda t: t * t * t * (t * (t * 6 - 15) + 10)
    u, v, w = f(xf), f(yf), f(zf)
    xi &= 255; yi &= 255; zi &= 255
    def g(dx, dy, dz):
        h = P[P[P[xi + dx] + yi + dy] + zi + dz]
        gr = G3[h]
        return gr[..., 0] * (xf - dx) + gr[..., 1] * (yf - dy) + gr[..., 2] * (zf - dz)
    l = lambda a, b, t: a + (b - a) * t
    return l(l(l(g(0,0,0), g(1,0,0), u), l(g(0,1,0), g(1,1,0), u), v), l(l(g(0,0,1), g(1,0,1), u), l(g(0,1,1), g(1,1,1), u), v), w)

def fbm(x, y, z, oct=3, rough=0.55):
    s, a, tot = 0, 1.0, 0
    for o in range(oct):
        f = 2 ** o
        s = s + a * perlin3(x * f, y * f, z * f + o * 17.3); tot += a; a *= rough
    return 0.5 + 0.5 * s / tot * 1.6  # ~0..1 (Blender Noise Fac benzeri)

def hexc(h): return np.array([(h >> 16) & 255, (h >> 8) & 255, h & 255], np.float32) / 255

def ramp(v, stops):
    out = np.zeros(v.shape + (3,), np.float32) + hexc(stops[0][1])
    for p, c in stops[1:]:
        out[v >= p] = hexc(c)
    return out

def grid(n, ss=2):
    N = n * ss
    c = (np.arange(N) + 0.5) / N
    u, v = np.meshgrid(c, 1 - c)  # v: 0 alt, 1 üst
    return u, v

def finish(rgb, a, n, ss=2):
    img = np.concatenate([rgb * a[..., None], a[..., None]], -1)  # önceden çarpılmış ortalama → kenar yumuşatma
    img = img.reshape(n, ss, n, ss, 4).mean((1, 3))
    al = img[..., 3:4]; rgb = np.where(al > 0, img[..., :3] / np.maximum(al, 1e-6), 0)
    return np.concatenate([rgb, al], -1)

def flame(T, seed, n=128):
    u, v = grid(n)
    v = v * 1.18 + 0.02  # uç hücreye sığsın
    nz = fbm(u * 2.0 * 2.2, (v * 2.2 - T * 1.8) * 2.2, seed * 7.3 + T * 1.3) - 0.5
    env = min(T * 4.0, 1.0) * (1 - T ** 2.2)
    vv = v - max(T - 0.45, 0) * 0.9
    ax = np.abs(u - 0.5) * 2
    w = np.maximum(1 - vv, 0) ** 0.75 * env * 0.78
    d = w - ax + nz * (vv * 0.9 + 0.15) - np.maximum(0.10 - vv, 0) * 4.0
    rgb = ramp(d, [(-9, 0x000000), (0.0, 0x3a0800), (0.045, 0xd8280a), (0.12, 0xff6a14), (0.22, 0xffb030), (0.32, 0xffe680), (0.42, 0xfffbe8)])
    return finish(rgb, (d > 0).astype(np.float32), n)

def boom(T, n=128):
    u, v = grid(n)
    x, y = (u - 0.5) * 2, (v - 0.5) * 2
    r = np.sqrt(x * x + y * y)
    nz = fbm(x * 1.6, y * 1.6, T * 1.1) - 0.5
    n2 = fbm(x * 3.2, y * 3.2, T * 0.7 + 5.0)
    R = 0.16 + 0.74 * (1 - (1 - T) ** 3)
    d = R - r + nz * (0.18 + T * 0.3)
    d = d - max(T - 0.45, 0) * n2 * 2.4
    h = 0.9 - T * 1.2 + d * 0.9 - r * 0.55
    rgb = ramp(h, [(-9, 0x3b302c), (0.12, 0x6a5650), (0.22, 0xc42a0a), (0.38, 0xff6a14), (0.56, 0xffb836), (0.76, 0xfff2c8)])
    ol = hexc(0x3a0c02) if T < 0.5 else hexc(0x221a18)
    rgb[d < 0.04] = ol
    return finish(rgb, (d > 0).astype(np.float32), n)

def voronoi_edge(u, v, scale, seed):
    r = np.random.default_rng(seed)
    x, y = u * scale, v * scale
    ix, iy = np.floor(x).astype(int), np.floor(y).astype(int)
    S = int(np.ceil(scale)) + 3
    J = r.random((S + 2, S + 2, 2))
    pts = []
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            cx, cy = ix + dx, iy + dy
            j = J[np.clip(cx, 0, S + 1), np.clip(cy, 0, S + 1)]
            pts.append(np.stack([cx + j[..., 0], cy + j[..., 1]], -1))
    pts = np.stack(pts, 0)
    p = np.stack([x, y], -1)
    d = np.linalg.norm(pts - p[None], axis=-1)
    i1 = np.argmin(d, 0)
    p1 = np.take_along_axis(pts, i1[None, ..., None].repeat(2, -1), 0)[0]
    best = np.full(x.shape, 9.0)
    for k in range(9):  # bisector mesafesi (gerçek kenara uzaklık)
        pk = pts[k]; m = (p1 + pk) / 2; nrm = pk - p1; ln = np.linalg.norm(nrm, axis=-1)
        ok = ln > 1e-6
        dd = np.abs(((p - m) * nrm).sum(-1)) / np.maximum(ln, 1e-6)
        best = np.where(ok, np.minimum(best, dd), best)
    return best / scale

def frost(n=512):
    u, v = grid(n)
    x, y = (u - 0.5) * 2, (v - 0.5) * 2
    r = np.sqrt(x * x + y * y)
    nz = fbm(x * 2.6, y * 2.6, 1.7, oct=4) - 0.5
    d = 0.90 - r + nz * 0.16
    c1 = voronoi_edge(u, v, 5.0, 3) < 0.022 / 5 * 5 * 0.2
    c2 = voronoi_edge(u, v, 13.0, 5) < 0.012 / 13 * 13 * 0.1
    shade = r + fbm(x * 6, y * 6, 3.3) * 0.35
    rgb = ramp(shade, [(-9, 0xf2fbff), (0.42, 0xc4ecff), (0.70, 0x86d2ff), (0.95, 0x4aa6ee)])
    rgb[c2] = rgb[c2] * 0.4 + hexc(0x5a9fe0) * 0.6
    rgb[c1] = hexc(0x1d5fa8)
    rgb[d < 0.035] = hexc(0x123c7a)
    # parıltı: küçük beyaz yıldızlar
    gl = fbm(x * 22, y * 22, 9.1, oct=1) > 0.86
    rgb[gl & (d > 0.06)] = hexc(0xffffff)
    return finish(rgb, (d > 0).astype(np.float32), n)

def save(arr, path):
    Image.fromarray((np.clip(arr, 0, 1) * 255 + 0.5).astype(np.uint8), 'RGBA').save(path, optimize=True)

def atlas(frames, cols=4):
    n = frames[0].shape[0]; rows = (len(frames) + cols - 1) // cols
    A = np.zeros((rows * n, cols * n, 4), np.float32)
    for i, f in enumerate(frames):
        r, c = divmod(i, cols); A[r * n:(r + 1) * n, c * n:(c + 1) * n] = f
    return A

if __name__ == '__main__':
    for s in (0, 1):
        save(atlas([flame(i / 15, s) for i in range(16)]), f'{OUT}/fx_flame{s}.png')
    save(atlas([boom(i / 15) for i in range(16)]), f'{OUT}/fx_boom.png')
    save(frost(), f'{OUT}/fx_frost.png')
    print('ok')
