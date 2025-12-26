import numpy as np

def tiled_process(
        img: np.ndarray,
        process_tile_fn,
        tile_size: int = 256,
        overlap: int = 32,
) -> np.ndarray:
    # img: H*W*C (uint8)
    h,w,c = img.shape
    assert c in (3, 4)

    step = tile_size - overlap
    xs = list(range(0, max(w-tile_size, 0)+1, step))
    ys = list(range(0, max(h-tile_size, 0)+1, step))

    if xs[-1] != w - tile_size:
        xs.append(max(w - tile_size, 0))
    if ys[-1] != h - tile_size:
        ys.append(max(h - tile_size, 0))
    
    out = None
    weight = None

    for y in ys:
        for x in xs:
            tile = img[y:y+tile_size, x:x+tile_size]
            out_tile = process_tile_fn(tile)

            if out is None:
                oh, ow, oc = out_tile.shape
                out = np.zeros(( (h*oh)//tile.shape[0], (w*ow)//tile.shape[1], oc), dtype=np.float32)
                weight = np.zeros_like(out, dtype=np.float32)

            oy = int(y * out_tile.shape[0] / tile.shape[0])
            ox = int(x * out_tile.shape[1] / tile.shape[1])

            wh, ww = out_tile.shape[:2]
            wy = np.ones((wh, 1), dtype=np.float32)
            wx = np.ones((1, ww), dtype=np.float32)

            ramp = min(overlap, tile_size // 2)
            if ramp > 0:
                r = np.linspace(0, 1, ramp, dtype=np.float32)
                wy[:ramp] *= r[:,None]
                wy[-ramp:] *= r[::-1, None]
                wx[:, :ramp] *= r[None, :]
                wx[:, -ramp:] *= [None, ::-1]

            wmap = wy @ wx
            wmap = np.repeat(wmap[:, :, None], out.shape[2], axis=2)

            out[oy:oy+wh, ox:ox+ww] += wmap

    out = out/ np.maximum(weight, 1e-6)
    return np.clip(out, 0, 255).astype(np.uint8)