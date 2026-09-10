# The Barnsely Fern is generated using the "chaos game".
# at each step we pick one of 4 affine transformations (chosen with fixed
# probabilities that mimic how real ferns branch and grow) and apply it
# to the current point. Repeating this tens of thousands of times traces
# out a self-similar fern shape, purely from simple linear algebra.


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import LinearSegmentedColormap


# 1. Generate the fern points via the chaos game


# Each transformation is an affine map: (x, y) -> (a*x + b*y + e, c*x + d*y + f)
# probabilities sum to 1.0 and are tuned so the fern looks "right"
#   f1: stem                     (prob 1%)
#   f2: successively smaller leaflets (prob 85%)
#   f3: left leaflet              (prob 7%)
#   f4: right leaflet             (prob 7%)


TRANSFORMS = [
    # a,     b,     c,    d,     e,    f
    (0.00,  0.00,  0.00, 0.16,  0.00, 0.00),   # f1 - stem
    (0.85,  0.04, -0.04, 0.85,  0.00, 1.60),   # f2 - main leaflets
    (0.20, -0.26,  0.23, 0.22,  0.00, 1.60),   # f3 - left leaflet
    (-0.15, 0.28,  0.26, 0.24,  0.00, 0.44),   # f4 - right leaflet
]
PROBABILITIES = [0.01, 0.85, 0.07, 0.07]


def generate_fern(n_points: int = 60_000, seed: int = 42) -> np.ndarray:
    """Generate n_points (x, y) coordinates that trace out a Barnsley Fern."""
    rng = np.random.default_rng(seed)
    choices = rng.choice(len(TRANSFORMS), size=n_points, p=PROBABILITIES)

    points = np.zeros((n_points, 2), dtype=np.float64)
    x, y = 0.0, 0.0
    for i, t_idx in enumerate(choices):
        a, b, c, d, e, f = TRANSFORMS[t_idx]
        x, y = a * x + b * y + e, c * x + d * y + f
        points[i] = (x, y)
    return points



# 2. Colour mapping — gradient from deep forest green (base) to bright
#    lime tips, driven by each point's height (y value)


FERN_CMAP = LinearSegmentedColormap.from_list(
    "fern", ["#0b3d0b", "#2e8b2e", "#7ed957", "#c6ff4d"]
)


def colours_for(points: np.ndarray) -> np.ndarray:
    y = points[:, 1]
    norm = (y - y.min()) / (y.max() - y.min())
    return FERN_CMAP(norm)



# 3. Static render 

def render_static(points: np.ndarray, colours: np.ndarray, out_path: str) -> None:
    fig, ax = plt.subplots(figsize=(7, 9), facecolor="black")
    ax.set_facecolor("black")
    ax.scatter(points[:, 0], points[:, 1], s=0.2, c=colours, marker=".")
    ax.set_xlim(points[:, 0].min() - 1, points[:, 0].max() + 1)
    ax.set_ylim(points[:, 1].min() - 1, points[:, 1].max() + 1)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.tight_layout(pad=0)
    fig.savefig(out_path, dpi=200, facecolor="black")
    plt.close(fig)



# 4. Animated growth render 


def render_animation(
    points: np.ndarray,
    colours: np.ndarray,
    out_path_mp4: str,
    out_path_gif: str | None = None,
    points_per_frame: int = 600,
    fps: int = 30,
) -> None:
    fig, ax = plt.subplots(figsize=(7, 9), facecolor="black")
    ax.set_facecolor("black")
    ax.set_xlim(points[:, 0].min() - 1, points[:, 0].max() + 1)
    ax.set_ylim(points[:, 1].min() - 1, points[:, 1].max() + 1)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.tight_layout(pad=0)

    scat = ax.scatter([], [], s=0.2, marker=".")
    n_frames = int(np.ceil(len(points) / points_per_frame))

    def update(frame):
        end = min((frame + 1) * points_per_frame, len(points))
        scat.set_offsets(points[:end])
        scat.set_color(colours[:end])
        return (scat,)

    anim = animation.FuncAnimation(
        fig, update, frames=n_frames, interval=1000 / fps, blit=True
    )

    anim.save(out_path_mp4, writer=animation.FFMpegWriter(fps=fps, bitrate=2400))
    if out_path_gif:
        # Fewer frames for a lighter-weight gif (README preview only)
        anim.save(out_path_gif, writer=animation.PillowWriter(fps=fps // 2))
    plt.close(fig)


if __name__ == "__main__":
    N_POINTS = 60_000
    pts = generate_fern(N_POINTS)
    cols = colours_for(pts)

    render_static(pts, cols, "fern_static.png")
    render_animation(pts, cols, "fern_growth.mp4", "fern_growth.gif")

    print(f"Generated {N_POINTS} points.")
    print("Saved: fern_static.png, fern_growth.mp4, fern_growth.gif")
