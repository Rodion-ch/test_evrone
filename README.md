# test_evrone

## Как запустить
```bash
Make docker-build
Make docker-run
```

## Как передать 
```bash
curl -X POST http://localhost:8000/api/transcribe \
  -H "Content-Type: multipart/form-data" \
  -F "file=@path/to/your/audiofile.wav"
```