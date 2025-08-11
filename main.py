import os
from fastapi import FastAPI, Query, HTTPException
from match3_generator import generate_new_grid_html, load_grid_from_json, generate_grid_html_from_existing
from grid_db import init_db

app = FastAPI()


# Initialize DB on startup
@app.on_event("startup")
def startup_event():
    init_db()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/generate_grid")
def generate_grid(normal_tile_count: int = Query(40, ge=1, le=81), style: str = Query("auto")):
    """
    Generate a new grid.
    - normal_tile_count: number of normal tiles (1-81)
    - style: one of "auto", "vertical", "horizontal", "diagonal"
    """
    valid_styles = {"auto", "vertical", "horizontal", "diagonal"}
    if style not in valid_styles:
        raise HTTPException(status_code=400, detail=f"Invalid style. Choose one of {valid_styles}")

    html = generate_new_grid_html(normal_tile_count=normal_tile_count, style=style, save_files=False)
    return {"html": html}


@app.get("/load_grid")
def load_latest_grid():
    """
    Load latest grid from JSON and return HTML.
    """
    grid = load_grid_from_json()
    if not grid:
        raise HTTPException(status_code=404, detail="No saved grid found.")

    html = generate_grid_html_from_existing(grid, save_file=False)
    return {"html": html}
