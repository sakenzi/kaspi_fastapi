import uvicorn


if __name__ == "__main__":
    uvicorn.run("main:app", host="loclahost", port=8000, reload=True)