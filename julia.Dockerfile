FROM julia

RUN julia install.jl

WORKDIR /app
COPY . .
