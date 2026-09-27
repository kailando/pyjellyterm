Pixel=tuple[int, int, int]
Row=list[Pixel]
Image=list[Row]
PreprocessedRow=list[tuple[tuple[Pixel, bool], tuple[Pixel, bool]]]
PreprocessedImage=list[PreprocessedRow]

def preprocess(image: Image) -> PreprocessedImage:
    preim=[]

    for n in range(0, len(image), 2):
        lastt=None
        lastb=None
        top = image[n]
        bottom = image[n + 1] if n + 1 < len(image) else [(0, 0, 0)] * len(top)

        preim.append([])
        for N in range(len(top)):
            preim[-1].append(
                (
                    (top[N], top[N]==lastt),
                    (bottom[N], bottom[N]==lastb)
                )
            )
            lastt=top[N]
            lastb=bottom[N]

    return preim

def render(image: PreprocessedImage) -> str:
    out=[]
    for row in image:
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
    scale=4

    sep=[(0,0,0)]*round(256/scale)
    image=[]

    for r in range(0,256,scale):
        image.append([])
        for b in range(0,256,scale):
            image[-1].append((r,0,b))
            
    image.append(sep)
    image.append(sep)

    for r in range(0,256,scale):
        image.append([])
        for g in range(0,256,scale):
            image[-1].append((r,g,0))

    image.append(sep)
    image.append(sep)

    for b in range(0,256,scale):
        image.append([])
        for g in range(0,256,scale):
            image[-1].append((0,g,b))
            
    print(render(preprocess(image)),flush=False)
    print("",flush=True)