# ── Base Image ──────────────────────────────────────────────────
FROM python:3.13-slim

# ── Environment Variables ────────────────────────────────────────
# Prevents Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
# Prevents Python from buffering stdout/stderr (important for logging)
ENV PYTHONUNBUFFERED=1

# ── Set Working Directory ────────────────────────────────────────
WORKDIR /app

# ── Install uv (package manager) ────────────────────────────────
RUN pip install uv

# ── Copy Dependency Files First ──────────────────────────────────
# Copy these before the rest of the code so Docker can cache the
# dependency layer — only reinstalls if toml/lock files change
COPY pyproject.toml uv.lock ./

# ── Install Dependencies ─────────────────────────────────────────
RUN uv sync --frozen

# ── Copy Rest of the Project ─────────────────────────────────────
COPY . .

# ── Expose Port (FastAPI runs on 8000) ───────────────────────────
EXPOSE 8000

# ── Entry Point ──────────────────────────────────────────────────
CMD ["uv", "run", "python", "main.py"]