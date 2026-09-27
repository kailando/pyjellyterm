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