Pixel=tuple[int, int, int]
Row=list[Pixel]
Image=list[Row]
PreprocessedRow=list[tuple[Pixel, Pixel]]
PreprocessedImage=list[PreprocessedRow]

def preprocess(image: Image) -> PreprocessedImage:
    preim=[]
    for n in range(0, len(image), 2):
        top = image[n]
        bottom = image[n + 1] if n + 1 < len(image) else [(0, 0, 0)] * len(top)

        preim.append([
            (top[N], bottom[N])
            for N in range(len(top))
        ])
    return preim

def render(image: PreprocessedImage) -> str:
    out=[]
    for row in image:
        orow=[]
        for ca, cb in row:
            orow.append(f"\033[38;2;{ca[0]};{ca[1]};{ca[2]}m") # Top pixel
            orow.append(f"\033[48;2;{cb[0]};{cb[1]};{cb[2]}m") # Bottom pixel
            orow.append("▀"                                  ) # The pixel itself
            orow.append("\033[0m"                            ) # Reset color
        out.append("".join(orow))
    return "\n".join(out)

if __name__=="__main__":
    L,M,H,=0,128,255
    image=[
        [
            (
                L,
                L,
                L,
            ),
            (
                M if n&4 else L,
                M if n&2 else L,
                M if n&1 else L,
            ),
            (
                H if n&4 else L,
                H if n&2 else L,
                H if n&1 else L,
            ),
        ] for n in range(0, 8)
    ]
    print(render(preprocess(image)))