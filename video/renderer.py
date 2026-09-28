"""An image renderer."""

from typing import TypeAlias

Pixel: TypeAlias            =tuple[int, int, int]
Row: TypeAlias              =list[Pixel]
Image: TypeAlias            =list[Row]
PreprocessedPixel: TypeAlias=tuple[Pixel, bool]
PreprocessedChar: TypeAlias =tuple[PreprocessedPixel, PreprocessedPixel]
PreprocessedRow: TypeAlias  =list[PreprocessedChar]
PreprocessedImage: TypeAlias=list[PreprocessedRow]

def preprocess(img: Image) -> PreprocessedImage:
    """Preprocesses an Image.

    Args:
        img (Image): The Image to preprocess.

    Returns:
        PreprocessedImage: The result, to feed into a renderer.
    """
    preim=[]

    for n in range(0, len(img), 2):
        lastt=None
        lastb=None
        top = img[n]
        bottom = img[n + 1] if n + 1 < len(img) else [(0, 0, 0)] * len(top)

        preim.append([])
        for n2, it in enumerate(top):
            bit=bottom[n2]
            preim[-1].append(
                (
                    (it, it==lastt),
                    (bit, bit==lastb)
                )
            )
            lastt=it
            lastb=bit

    return preim

def render_term(img: PreprocessedImage) -> str:
    """A renderer (terminal). Renders PreprocessedImage into 24-bit truecolor ANSI.

    Args:
        img (PreprocessedImage): The image, from preprocess(), to show.

    Returns:
        str: The string to print.
    """
    out=[]
    for row in img:
        orow=[]
        for ca, cb in row:
            cac, cab = ca
            cbc, cbb = cb

            if not cab:
                orow.append(f"\033[38;2;{cac[0]};{cac[1]};{cac[2]}m") # Top pixel
            if not cbb:
                orow.append(f"\033[48;2;{cbc[0]};{cbc[1]};{cbc[2]}m") # Bottom pixel

            orow.append("▀")
        out.append("".join(orow))                                     # The pixel itself

    return "\033[0m\n".join(out) + "\033[0m"                          # Reset


if __name__=="__main__":
    SCALE=4

    sep=[(0,0,0)]*round(256/SCALE)
    image=[]

    for r in range(0,256,SCALE):
        image.append([])
        for b in range(0,256,SCALE):
            image[-1].append((r,0,b))

    image.append(sep)
    image.append(sep)

    for r in range(0,256,SCALE):
        image.append([])
        for g in range(0,256,SCALE):
            image[-1].append((r,g,0))

    image.append(sep)
    image.append(sep)

    for b in range(0,256,SCALE):
        image.append([])
        for g in range(0,256,SCALE):
            image[-1].append((0,g,b))

    print(render_term(preprocess(image)),flush=False)
    print("",flush=True)
