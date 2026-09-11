#!/usr/bin/env python3
"""Deterministic, publication-sized vector figures. Run from any directory.

Requires matplotlib 3.10.9. PDFs embed TrueType fonts; SVGs outline glyphs,
so rendering does not depend on the viewer's installed fonts.
Coordinates and type sizes are in points at the final placement size.
"""
from pathlib import Path
import os
os.environ.setdefault("SOURCE_DATE_EPOCH", "1788739200")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch, Circle, Polygon, Ellipse, PathPatch
from matplotlib.path import Path as MPath

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "figures"
PREVIEW = ROOT / "build" / "figure-preview"
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 8,
    "mathtext.fontset": "dejavusans", "pdf.fonttype": 42,
    "svg.fonttype": "path", "svg.hashsalt": "cid-figures-v1",
})
INK = "#253246"
MUTED = "#536278"
RULE = "#D7DFE9"
BLUE = "#286B9A"
PURPLE = "#6950A1"
TEAL = "#21796C"
AMBER = "#A36621"
PALE = {BLUE: "#EDF5FA", PURPLE: "#F1EDF8", TEAL: "#EDF7F3", AMBER: "#FBF3E6", INK: "#F3F5F8"}

class Drawing:
    def __init__(self, name, w, h):
        self.name, self.w, self.h = name, w, h
        self.fig = plt.figure(figsize=(w/72, h/72))
        self.ax = self.fig.add_axes([0, 0, 1, 1])
        self.ax.set(xlim=(0,w), ylim=(h,0))
        self.ax.axis("off")
        self.texts = []
    def text(self,x,y,s,size=8,color=INK,weight="normal",ha="left",**kw):
        t=self.ax.text(x,y,s,fontsize=size,color=color,weight=weight,
                      ha=ha,va="center",linespacing=1.35,**kw)
        self.texts.append(t)
        return t
    def rect(self,x,y,w,h,fill="white",edge=RULE,lw=.7):
        self.ax.add_patch(Rectangle((x,y),w,h,facecolor=fill,edgecolor=edge,linewidth=lw))
    def line(self,points,color=RULE,lw=.8,dash=False):
        self.ax.plot(*zip(*points),color=color,lw=lw,ls=(0,(3,2)) if dash else "-",solid_capstyle="round")
    def arrow(self,points,color=INK,dash=False,lw=.9):
        path=MPath(points,[MPath.MOVETO]+[MPath.LINETO]*(len(points)-1))
        self.ax.add_patch(FancyArrowPatch(path=path,arrowstyle="-|>",mutation_scale=7,
                       linewidth=lw,color=color,linestyle=(0,(3,2)) if dash else "-",
                       capstyle="round",joinstyle="round"))
    def box(self,x,y,w,h,title,color=PURPLE,sub=None,size=8):
        self.rect(x,y,w,h,PALE[color],color,.65)
        if sub:
            self.text(x+w/2,y+h/2-6,title,size,color,"bold",ha="center")
            self.text(x+w/2,y+h/2+7,sub,7,ha="center")
        else:
            self.text(x+w/2,y+h/2,title,size,ha="center")
    def label(self,x,y,s,color=MUTED,ha="center"):
        self.text(x,y,s,7,color,ha=ha,bbox=dict(facecolor="white",edgecolor="none",pad=1.1))
    def dot(self,x,y,color=PURPLE,r=2.7):
        self.ax.add_patch(Circle((x,y),r,facecolor=color,edgecolor="white",lw=.6))
    def save(self):
        self.fig.canvas.draw()
        renderer=self.fig.canvas.get_renderer()
        frame=self.fig.bbox
        for t in self.texts:
            b=t.get_window_extent(renderer)
            if b.x0<frame.x0 or b.x1>frame.x1 or b.y0<frame.y0 or b.y1>frame.y1:
                raise ValueError(f"{self.name}: clipped text {t.get_text()!r}")
        OUT.mkdir(exist_ok=True)
        PREVIEW.mkdir(parents=True,exist_ok=True)
        self.fig.savefig(OUT/f"{self.name}.pdf",metadata={"Title":self.name,"Creator":"CID vector figure generator","CreationDate":None,"ModDate":None})
        self.fig.savefig(OUT/f"{self.name}.svg",metadata={"Date":None})
        svg_path = OUT/f"{self.name}.svg"
        svg_path.write_text("\n".join(line.rstrip() for line in svg_path.read_text().splitlines())+"\n")
        self.fig.savefig(PREVIEW/f"{self.name}.png",dpi=220)
        plt.close(self.fig)

def timing():
    d=Drawing("interface-timing",484,190)
    d.text(5,12,"a",10,PURPLE,"bold")
    d.text(19,12,"Turn-based AR",9,INK,"bold")
    d.text(479,12,"Discrete call / observation boundaries",7,MUTED,ha="right")
    xs=[5,85,170,247,333,411]
    ws=[61,67,59,68,60,68]
    labels=["Reason","Explicit call","Wait","Observation","Done?","Response"]
    colors=[PURPLE,AMBER,INK,BLUE,INK,TEAL]
    for x,w,l,c in zip(xs,ws,labels,colors): d.box(x,45,w,24,l,c)
    for i in range(5): d.arrow([(xs[i]+ws[i],57),(xs[i+1],57)])
    d.arrow([(363,45),(363,30),(35,30),(35,45)])
    d.label(378,32,"no")
    d.text(402,50,"yes",7,MUTED,ha="center")
    d.line([(5,84),(479,84)])
    d.text(5,98,"b",10,PURPLE,"bold")
    d.text(19,98,"CID on a dLLM",9,INK,"bold")
    d.text(479,98,"One evolving, revisable trajectory",7,MUTED,ha="right")
    for x,w,s in [(40,38,r"$s_i$"),(105,43,r"$s_{i+1}$"),(222,38,r"$s_j$"),(289,43,r"$s_{j+1}$")]:
        d.box(x,125,w,23,s)
    for a,b in [(5,40),(78,105),(148,222),(260,289),(332,362)]:
        d.arrow([(a,136.5),(b,136.5)],PURPLE)
    for x in [17,183,349]: d.label(x,136.5,r"$\cdots$",PURPLE)
    d.box(362,125,65,23,"Converged?",INK,size=7)
    d.box(442,125,37,23,"Final",TEAL,size=7.5)
    d.arrow([(427,136.5),(442,136.5)])
    d.text(434.5,129.5,"yes",7,MUTED,ha="center")
    d.arrow([(397,148),(397,164),(349,164),(349,144)],PURPLE)
    d.label(410,158,"no")
    d.label(59,116,"need emerges")
    d.label(241,116,"assimilate result")
    d.box(26,165,66,21,"Bind + launch",AMBER,size=7)
    d.box(119,165,87,21,"External read in flight",BLUE,size=7)
    d.arrow([(59,148),(59,165)],AMBER)
    d.arrow([(92,175.5),(119,175.5)],AMBER)
    d.arrow([(206,175.5),(241,175.5),(241,148)],BLUE)
    d.save()

def overview():
    d=Drawing("cid-overview",484,252)
    # Three channel bands with structural contents, not generic flowchart nodes.
    for x,w,c,title,sub in [
        (5,132,BLUE,"FACT  "+r"$F_s$","External write authority"),
        (176,132,PURPLE,"THOUGHT  "+r"$T_s$","Typed Cognitive Tensor"),
        (347,132,TEAL,"DISPLAY  "+r"$Y_s$","User-visible token canvas")]:
        d.rect(x,45,w,92,PALE[c],edge="none")
        d.line([(x,45),(x+w,45)],c,2)
        d.text(x+9,57,title,9,c,"bold")
        d.text(x+9,73,sub,7)
    d.text(13,94,"value",7,BLUE,"bold")
    d.text(60,94,"version",7,BLUE,"bold")
    d.text(13,111,"source + provenance",7.5)
    # Each row is a cell with semantics and illustrative dominant soft roles.
    for row,role in enumerate(["plan", "need", "claim"]):
        y=87+row*11
        d.text(184,y+3,rf"$c_{row+1}$",6.5,PURPLE)
        for col in range(5):
            d.rect(200+col*7,y,5.5,6,
                   ["#B9A3D9","#E2D8EE","#9274BA"][(row+col)%3],edge="none")
        d.rect(239,y-1,20,8,"white",edge="none")
        d.rect(240,y, [13,8,16][row],6,PALE[PURPLE],edge="none")
        d.rect(240,y, [8,5,11][row],6,PURPLE,edge="none")
        d.text(264,y+3,role,6.5)
    d.line([(297,90),(303,90),(303,112),(297,112)],PURPLE,.6)
    d.dot(297,90,PURPLE,1.8)
    d.dot(297,112,PURPLE,1.8)
    for row,length in enumerate([111,93,105]):
        for col in range(length//13):
            d.rect(356+col*13,88+row*10,10,5,
                   "#8AB8AC" if (row+col)%4 else "#D6E9E2",edge="none")
    d.arrow([(137,89),(176,89)],BLUE)
    d.label(156.5,101,"condition",BLUE)
    d.arrow([(308,89),(347,89)],PURPLE)
    d.label(327.5,101,"realize",PURPLE)
    d.arrow([(413,45),(413,22),(242,22),(242,45)],TEAL)
    d.label(327,12,"format / length feedback",TEAL)
    d.text(71,127,"Model-read-only",7,BLUE,ha="center")
    d.text(242,127,"Revisable cells",7,PURPLE,ha="center")
    d.text(413,127,"Revisable tokens",7,TEAL,ha="center")
    # Read-only sources and runtime are independent participants.
    d.rect(5,195,132,51,"white",BLUE)
    d.text(14,207,"TOOLS / SOURCES",8,BLUE,"bold")
    d.text(14,224,"Search  /  files  /  state",7.5)
    d.text(14,236,"Calculators",7.5)
    d.rect(176,195,190,51,PALE[AMBER],AMBER)
    d.text(186,207,"CID RUNTIME",8,AMBER,"bold")
    d.text(186,224,"Intent readout  /  persistent bindings",7.5)
    d.text(186,237,"Cache  /  refresh  /  event handling",7.5)
    d.arrow([(34,195),(34,137)],BLUE)
    d.label(36,157,"external",BLUE,ha="left")
    d.label(36,167,"updates",BLUE,ha="left")
    d.arrow([(242,137),(242,195)],PURPLE)
    d.label(248,179,"latent needs",PURPLE,ha="left")
    d.arrow([(176,222),(137,222)],AMBER)
    d.label(156,207,"bind /",AMBER)
    d.label(156,216,"refresh",AMBER)
    d.arrow([(117,195),(117,176),(209,176),(209,137)],BLUE,True)
    d.text(117,155,"perceptual",7,BLUE)
    d.text(117,165,"projections",7,BLUE)
    d.save()

def anatomy():
    """A single bounded cell contains all fields; positions are schematic."""
    d=Drawing("tct-anatomy",232,289)
    d.text(6,11,"Typed Cognitive Tensor",10,PURPLE,"bold")
    d.text(44,29,r"$H_s$: semantic vectors",7,PURPLE)
    d.text(154,29,"aligned fields",7,MUTED)
    for row in range(3):
        y=40+row*12
        if row==1:
            d.rect(5,y-2,222,12,PALE[PURPLE],edge="none")
        d.text(11,y+3,rf"$c_{{s,{['1','i','N'][row]}}}$",7,PURPLE)
        for col in range(12):
            d.rect(45+col*8,y,6,6,["#C3B0DF","#E0D5EE","#9274BA"][(col+row)%3],edge="none")
        for col,symbol in enumerate(["r","a","q","u",r"\tau",r"\ell"]):
            d.text(159+col*12,y+3,"$"+symbol+"$",6.5,MUTED,ha="center")
    d.line([(227,56),(230,56),(230,83),(186,98)],PURPLE,.7,True)
    d.text(6,85,r"One cognitive cell $c_{s,i}$",8,PURPLE,"bold")
    # One enclosing, gently curved contour. Internal locations do not imply
    # physical compartments or neural architecture.
    verts=[(30,99),(73,93),(159,93),(201,99),
           (220,102),(225,128),(225,162),
           (225,203),(219,242),(205,260),
           (184,284),(57,284),(28,266),
           (9,254),(7,220),(7,175),
           (7,130),(10,104),(30,99)]
    codes=[MPath.MOVETO]+[MPath.CURVE4]*18
    d.ax.add_patch(PathPatch(MPath(verts,codes),facecolor="#F7F4FB",edgecolor=PURPLE,lw=1.1))
    # A semantic nucleus, surrounded by compact visual encodings of its
    # aligned typed attributes. All seven fields stay inside the same outline.
    d.ax.add_patch(Ellipse((116,181),96,64,facecolor="white",edgecolor="#B9A3D9",lw=.9))
    d.text(116,167,r"$h_{s,i}\in\mathbb{R}^d$",10,PURPLE,ha="center")
    d.text(116,183,"semantic core",8,INK,"bold",ha="center")
    for row in range(2):
        for col in range(9):
            d.rect(86+col*7,194+row*6,5,4,
                   ["#C3B0DF","#E0D5EE","#9274BA"][(row+col)%3],edge="none")
    # Soft roles: a mixture, not a single categorical label.
    d.text(116,111,r"soft roles $r$",7,PURPLE,ha="center")
    for x,h,c in [(97,9,"#9274BA"),(108,16,"#B9A3D9"),(119,6,"#D5C8E7"),(130,12,"#A990C9")]:
        d.rect(x,139-h,7,h,c,edge="none")
    # Exact symbolic anchors represented by a tag with an immutable token.
    d.text(43,151,r"anchors $a$",7,BLUE,ha="center")
    d.ax.add_patch(Polygon([(21,162),(54,162),(63,172),(54,182),(21,182)],
                          closed=True,facecolor=PALE[BLUE],edgecolor=BLUE,lw=.7))
    d.text(39,172,"#42",7,BLUE,"bold",ha="center")
    d.ax.add_patch(Circle((56,172),1.6,facecolor="white",edgecolor=BLUE,lw=.6))
    # Source/cell links are relationships rather than another vector.
    d.text(189,151,r"links $q$",7,BLUE,ha="center")
    d.line([(180,170),(201,163),(200,183),(180,170)],BLUE,.7)
    for x,y in [(180,170),(201,163),(200,183)]: d.dot(x,y,BLUE,3.2)
    # Distinct encodings avoid turning the lower half into another field list.
    d.text(49,219,r"uncertainty $u$",7,AMBER,ha="center")
    for j in range(5):
        d.rect(27+j*9,229,7,7,AMBER if j<3 else "#EBD9C1",edge="none")
    d.text(183,219,r"lifecycle $\ell$",7,TEAL,ha="center")
    d.ax.add_patch(Circle((167,235),4,facecolor=PALE[TEAL],edgecolor=TEAL,lw=.7))
    d.dot(167,235,TEAL,2.4)
    d.text(176,235,"active",7,TEAL)
    d.text(116,248,r"editability $\tau$",7,AMBER,ha="center")
    d.line([(87,261),(145,261)],"#D6C5AC",2)
    d.line([(87,261),(121,261)],AMBER,2)
    d.ax.add_patch(Circle((121,261),3.4,facecolor="white",edgecolor=AMBER,lw=1,zorder=3))
    d.save()

def binding():
    d=Drawing("binding-lifecycle",484,163)
    d.text(5,11,"Persistent binding",10,AMBER,"bold")
    d.text(479,11,"Reuse the value as cognition evolves",7,MUTED,ha="right")
    xs=[5,103,201,299,397]
    for x,title,sub,c in [
        (5,"Active need","information request",PURPLE),
        (103,"Binding",r"$b_j$",AMBER),
        (201,"Cached value","version + provenance",BLUE),
        (299,"Projection",r"$P_j^s$",PURPLE),
        (397,"Evolving state","thought + display",TEAL)]:
        d.box(x,54,82,35,title,c,sub,8)
    for a,b in zip(xs,xs[1:]): d.arrow([(a+82,71.5),(b,71.5)])
    d.arrow([(438,54),(438,34),(340,34),(340,54)],PURPLE,True)
    d.label(388,25,"active need: re-project",PURPLE)
    d.box(103,125,82,27,"Retire binding",INK,size=8)
    d.arrow([(144,89),(144,125)],INK)
    d.label(144,107,"need inactive")
    d.box(201,125,108,27,"External read / refresh",BLUE,size=7.5)
    d.arrow([(242,125),(242,89)],BLUE)
    d.label(251,103,"first fetch or",BLUE,ha="left")
    d.label(251,114,"source-version change",BLUE,ha="left")
    d.save()

def runtime():
    d=Drawing("runtime-loop",484,184)
    for y,title,color in [(51,"MODEL",PURPLE),(106,"RUNTIME",AMBER),(161,"SOURCES",BLUE)]:
        d.rect(5,y-17,474,34,PALE[color],edge="none")
        d.text(11,y,title,7,color,"bold")
    d.box(72,37,77,28,"Denoise "+r"$T,Y$",PURPLE,size=8)
    d.box(165,37,82,28,"Expose needs "+r"$I$",PURPLE,size=7.5)
    d.box(279,37,91,28,"Assimilate arrivals",PURPLE,size=7.5)
    d.box(396,37,78,28,"Adjust local noise",PURPLE,size=7.2)
    d.arrow([(149,51),(165,51)],PURPLE)
    d.arrow([(370,51),(396,51)],PURPLE)
    d.arrow([(435,37),(435,16),(110,16),(110,37)],PURPLE)
    d.label(271,7,"next active update",PURPLE)
    d.box(165,92,82,28,"Match / update\nbinding",AMBER,size=7.5)
    d.box(279,92,91,28,"Reuse, refresh,\nor launch",AMBER,size=7.5)
    d.box(396,92,78,28,"Consume events",AMBER,size=7.5)
    d.arrow([(206,65),(206,92)],PURPLE)
    d.arrow([(247,106),(279,106)],AMBER)
    d.arrow([(309,92),(309,65)],BLUE,True)
    d.label(300,78,"cached re-projection",BLUE,ha="right")
    d.arrow([(435,92),(435,78),(351,78),(351,65)],BLUE)
    d.box(279,147,91,28,"Read-only external\nwork",BLUE,size=7.5)
    d.arrow([(324,120),(324,147)],BLUE,True)
    d.label(333,134,"async",BLUE,ha="left")
    d.arrow([(370,161),(435,161),(435,120)],BLUE,True)
    d.text(402.5,169,"completion event",7,BLUE,ha="center")
    d.save()


def selective_revision():
    """Conceptual running example, not a measured model trajectory."""
    d=Drawing("selective-revision",484,218)
    d.text(5,12,"Evidence changes linked regions",10,PURPLE,"bold")
    d.text(479,12,"Illustrative state transition",7,MUTED,ha="right")
    d.text(5,36,"Before arrival",9,INK,"bold")
    d.text(190,36,"New evidence",9,BLUE,"bold")
    d.text(330,36,"After assimilation",9,INK,"bold")
    for x in [5,330]:
        d.text(x,56,"TCT cells",7,PURPLE,"bold")
    for y,left,right,c in [
        (67,"plan: comparison structure","plan: unchanged",TEAL),
        (101,"hypothesis: latency < 30 ms","hypothesis: reopen",AMBER),
        (135,"claim: latency unresolved","claim: grounded in 37 ms",BLUE)]:
        d.rect(5,y,149,25,PALE[c],edge=c,lw=.6)
        d.text(11,y+12.5,left,7,c)
        d.rect(330,y,149,25,PALE[c],edge=c,lw=.6)
        d.text(336,y+12.5,right,7,c)
    d.rect(183,97,108,53,PALE[BLUE],BLUE,.7)
    d.text(192,109,"Documentation",7,BLUE,"bold")
    d.text(192,126,"37 ms",12,BLUE,"bold")
    d.text(192,140,"value + provenance",6.8,BLUE)
    d.line([(291,124),(313,124)],BLUE,.8)
    d.arrow([(313,124),(313,113.5),(330,113.5)],BLUE)
    d.arrow([(313,124),(313,147.5),(330,147.5)],BLUE)
    d.text(238,170,r"route via $\chi_j$",7,BLUE,ha="center")
    d.arrow([(154,79.5),(330,79.5)],TEAL)
    d.label(239,70,"preserve unrelated state",TEAL)
    d.text(5,178,"Display",7,TEAL,"bold")
    d.rect(5,187,149,24,PALE[TEAL],edge="none")
    d.text(12,199,"Latency:  [unresolved]",7.5,TEAL)
    d.rect(330,187,149,24,PALE[TEAL],edge="none")
    d.text(337,199,"Latency:  37 ms",7.5,TEAL)
    d.arrow([(154,199),(330,199)],TEAL)
    d.label(239,190,"revise linked output",TEAL)
    d.save()

if __name__=="__main__":
    for draw in (timing,overview,anatomy,binding,runtime,selective_revision):
        draw()
    print("Wrote six vector PDF/SVG pairs and 220 dpi previews.")
