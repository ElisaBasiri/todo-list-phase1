if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "api":
        import uvicorn
        uvicorn.run("main_api:app", host="0.0.0.0", port=8000, reload=True)
    else:
        # Run CLI with warning
        print("WARNING: CLI is deprecated. Use 'python main.py api' for FastAPI server.")
        # Old CLI code